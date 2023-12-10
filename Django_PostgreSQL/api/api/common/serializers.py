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
            if len(prefetch_related.split('__')) < cls.Meta.depth + 2
        ]

    @classmethod
    def get_nested_prefetch(cls, field_name):
        nested_prefetch = []
        for prefetch in cls.nested_prefetch:
            child_prefetch = prefetch.split('__')
            if 1 < len(child_prefetch) < cls.Meta.depth + 2 and child_prefetch[0] == field_name:
                nested_prefetch.append("__".join(child_prefetch[1:]))
        return nested_prefetch

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

    def deep_dict_travel(self, data: dict) -> tuple:
        nested = {}
        for field_name, model in self._nested_models.items():
            field_data = data.get(field_name, None)
            serializer = self.get_serializer(model, mode="Nested")(context=self.context)
            if isinstance(field_data, dict):
                data[field_name], nested[field_name] = serializer.deep_dict_travel(field_data)
            elif isinstance(field_data, list):
                data[field_name], nested[field_name] = map(list, zip(*serializer.deep_list_travel(field_data)))
        return self.update_or_create(data, nested)

    def deep_list_travel(self, data_list: list) -> list[tuple]:
        data_and_nested = [(data, {}) for data in data_list]
        datas = [d_n for d_n in data_and_nested if isinstance(d_n[0], dict)]
        for field_name, model in self._nested_models.items():
            serializer = self.get_serializer(model, mode="Nested")(context=self.context)
            if dicts := [zipped for zipped in datas if isinstance(zipped[0].get(field_name, None), dict)]:
                for (data, rep), res in zip(dicts, serializer.deep_list_travel([d[field_name] for d, _ in dicts])):
                    data[field_name], rep[field_name] = res
            elif lists := [(d, r, len(d[field_name])) for d, r in datas if isinstance(d.get(field_name, None), list)]:
                flatten_res = serializer.deep_list_travel([item for d, _, _ in lists for item in d[field_name]])
                start = 0
                for data, representation, length in lists:
                    data[field_name], representation[field_name] = map(list, zip(*flatten_res[start:start + length]))
                    start += length
        return self.bulk_update_or_create(data_and_nested)

    def update_or_create(self, data: dict, nested: dict, instances: dict = None):
        model = self.Meta.model
        if pk := data.get(model._meta.pk.name, None):
            self.instance = instances.get(pk, None) if instances is not None else model.objects.filter(pk=pk).first()
        self.initial_data, self.partial = data, bool(self.instance)
        if self.is_valid():
            return self.save().pk, OrderedDict(self.data, **nested)
        return f"Failed to serialize {model.__name__}", OrderedDict(nested, ERROR=self.errors)

    def bulk_update_or_create(self, data_and_nested: list[tuple]) -> list[tuple]:
        pks_and_representations, created = [], {}
        pk_name = self.Meta.model._meta.pk.name
        instances = self.Meta.model.objects.prefetch_related(*self.get_prefetch_related()).in_bulk(
            set(d[pk_name] for d, _ in data_and_nested if pk_name in d)
        )
        for data, nested in data_and_nested:
            if isinstance(data, dict):
                found_pk = data.get(pk_name, None)
                if found_pk not in created:
                    created_pk, representation = self.update_or_create(data, nested, instances=instances)
                    found_pk = found_pk if found_pk is not None else created_pk
                    created[found_pk] = (created_pk, representation)
                    if "ERROR" not in representation:
                        del self._data, self._validated_data
                pks_and_representations.append(created[found_pk])
            else:
                pks_and_representations.append((data, data))
        return pks_and_representations

    def deep_create(self, data: dict | list):
        try:
            with atomic():
                serializer = self.get_serializer(self.Meta.model, mode="Nested")(context=self.context)
                if data and isinstance(data, dict):
                    primary_key, representation = serializer.deep_dict_travel(data)
                    if "ERROR" in representation:
                        raise ValidationError(representation)
                elif data and isinstance(data, list):
                    primary_key, representation = map(list, zip(*serializer.deep_list_travel(data)))
                    if any("ERROR" in d for d in representation):
                        raise ValidationError(representation)
        except ValidationError as representation:
            return representation
        return representation

    @classmethod
    def get_serializer(cls, _model, mode: str = ""):
        if mode + _model.__name__ not in cls._serializers:
            parent = cls.get_serializer(_model) if mode else DeepSerializer

            class CommonNestedSerializer(parent):
                _mode = mode

                class Meta:
                    model = _model
                    depth = 0
                    fields = parent.Meta.fields if mode else '__all__'

        return cls._serializers[mode + _model.__name__]

########################################################################################################################
#
########################################################################################################################
