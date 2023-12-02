import re
from collections import OrderedDict

from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.utils import model_meta
from rest_framework.utils.field_mapping import (get_nested_relation_kwargs, )


########################################################################################################################
#
########################################################################################################################


class DeepSerializer(serializers.ModelSerializer):
    _serializers = {}
    _mode = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "Meta"):
            model = cls.Meta.model
            cls._serializers[cls._mode + model.__name__] = cls
            cls._nested_models = {f.name: f.related_model for f in model._meta.get_fields() if f.related_model}
            cls._prefetch_related = [p[2:] for p in cls.build_prefetch_related(model, [model])]
            cls.nested_prefetch = cls.nested_prefetch if hasattr(cls, 'nested_prefetch') else cls._prefetch_related
            cls.Meta.read_only_fields = tuple(model_meta.get_field_info(model).reverse_relations)

    @classmethod
    def build_prefetch_related(cls, parent_model, exclude_models):
        prefetch_related = []
        for field in parent_model._meta.get_fields():
            if (model := field.related_model) and model not in exclude_models:
                current_prefetch = f"__{field.name}"
                prefetch_related.append(current_prefetch)
                for prefetch in cls.build_prefetch_related(model, exclude_models + [model]):
                    prefetch_related.append(current_prefetch + prefetch)
        return prefetch_related

    @classmethod
    def get_prefetch_related(cls):
        return [
            prefetch_related
            for prefetch_related in cls._prefetch_related
            if len(re.findall('__', prefetch_related)) < cls.Meta.depth
        ]

    @classmethod
    def get_nested_prefetch(cls, field_name):
        parent_prefetch = []
        for prefetch in cls.nested_prefetch:
            child_prefetch = prefetch.split('__')
            if child_prefetch[0] == field_name and 0 < len(child_prefetch) - 1 <= cls.Meta.depth:
                parent_prefetch.append("__".join(child_prefetch[1:]))
        return parent_prefetch

    def get_default_field_names(self, declared_fields, model_info):
        return (
                [model_info.pk.name] +
                list(declared_fields) +
                list(model_info.fields) +
                list(set(field.split('__')[0] for field in self.nested_prefetch))
        )

    def build_nested_field(self, field_name, relation_info, nested_depth):
        serializer = self.get_serializer(relation_info.related_model, mode=f"Read{self.Meta.model.__name__}Nested")
        serializer.nested_prefetch = self.get_nested_prefetch(field_name)
        serializer.Meta.depth = nested_depth - 1
        return serializer, get_nested_relation_kwargs(relation_info)

    def create_deep_dict(self, data: dict) -> tuple:
        nest = {}
        for field_name, model in self._nested_models.items():
            field_data = data.get(field_name, None)
            serializer = self.get_serializer(model, mode="Nested")(context=self.context)
            if isinstance(field_data, dict):
                data[field_name], nest[field_name] = serializer.create_deep_dict(field_data)
            elif isinstance(field_data, list):
                data[field_name], nest[field_name] = zip(
                    *(serializer.create_deep_dict(d) if isinstance(d, dict) else (d, d) for d in field_data)
                )
        return self.get_or_create(data, nest)

    def get_or_create(self, data: dict, nested_representation: dict):
        self.instance = self.Meta.model.objects.filter(pk=data.get(self.Meta.model._meta.pk.name, None)).first()
        self.partial = bool(self.instance)
        self.initial_data = data
        if self.is_valid():
            result = self.save().pk, OrderedDict(self.data, **nested_representation)
            del self._data
            del self._validated_data
        else:
            nested_representation["ERROR"] = self.errors
            result = f"Fail to serialize {self.Meta.model.__name__}", nested_representation
        return result

    def create_deep_list(self, data_list: list) -> list[tuple]:
        representations = [{}] * len(data_list)
        nested = [zipped for zipped in zip(data_list, representations) if isinstance(zipped[0], dict)]
        for field_name, model in self._nested_models.items():
            serializer = self.get_serializer(model, mode="Nested")(context=self.context)
            if dicts := [zipped for zipped in nested if isinstance(zipped[0].get(field_name, None), dict)]:
                for (d, r), created in zip(dicts, serializer.create_deep_list([d[field_name] for d, _ in dicts])):
                    d[field_name], r[field_name] = created
            elif lists := [(d, r, len(d[field_name])) for d, r in nested if isinstance(d.get(field_name, None), list)]:
                flatten_lists = serializer.create_deep_list([item for d, _, _ in lists for item in d[field_name]])
                start = 0
                for data, representation, length in lists:
                    data[field_name], representation[field_name] = zip(*flatten_lists[start:start+length])
                    start += length
        return self.bulk_update_or_create(data_list, representations)

    def bulk_update_or_create(self, data_list: list, nested_representations: list) -> list[tuple]:
        pk_name = self.Meta.model._meta.pk.name
        instances = self.Meta.model.objects.in_bulk(set(d[pk_name] for d in data_list if pk_name in d))
        created_index, created = {}, []
        for index, (data, nested) in enumerate(zip(data_list, nested_representations)):
            primary_key = data.get(pk_name, None)
            if primary_key in created_index:
                created.append(created[created_index[primary_key]])
            else:
                self.instance = instances.get(primary_key, None)
                self.partial = bool(self.instance)
                self.initial_data = data
                if self.is_valid():
                    created.append((self.save().pk, OrderedDict(self.data, **nested)))
                    del self._data
                    del self._validated_data
                else:
                    nested["ERROR"] = self.errors
                    created.append((f"Fail to serialize {self.Meta.model.__name__}", nested))
                created_index[primary_key] = index
        return created

    def deep_create(self, data: dict | list):
        representation = None
        try:
            with atomic():
                serializer = self.get_serializer(self.Meta.model, mode="Nested")(context=self.context, data=data)
                if isinstance(data, dict):
                    primary_key, representation = serializer.create_deep_dict(data)
                    if "ERROR" in representation:
                        raise ValidationError()
                if isinstance(data, list):
                    primary_key, representation = zip(*serializer.create_deep_list(data))
                    if any("ERROR" in d for d in representation):
                        raise ValidationError()
        except ValidationError as e:
            print(f"ERROR: {e}")
        return representation

    @classmethod
    def get_serializer(cls, _model, mode: str = ""):
        if mode + _model.__name__ not in cls._serializers:
            parent = cls.get_serializer(_model) if mode else DeepSerializer

            class CommonSerializer(parent):
                _mode = mode

                class Meta:
                    model = _model
                    depth = 0
                    fields = parent.Meta.fields if mode else '__all__'

        return cls._serializers[mode + _model.__name__]

########################################################################################################################
#
########################################################################################################################
