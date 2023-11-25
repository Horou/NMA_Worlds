import re
from pprint import pprint

from django.db.transaction import atomic
from rest_framework import serializers
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
            cls._nested_models = cls.get_nested_models(model)
            cls._prefetch_related = [related[2:] for related in cls.build_prefetch_related(model, [model])]
            cls.parent_prefetch = cls.parent_prefetch if hasattr(cls, 'parent_prefetch') else cls._prefetch_related
            cls.Meta.read_only_fields = tuple(model_meta.get_field_info(model).reverse_relations)


    @classmethod
    def get_nested_models(cls, model):
        nested_models = {}
        for field_name, field in model_meta.get_field_info(model).relations.items():
            if not field_name.endswith("_set"):
                nested_models[field_name] = field.related_model
        for field in model._meta.get_fields():
            if field.one_to_one:
                nested_models[field.name] = field.related_model
        return nested_models


    @classmethod
    def build_prefetch_related(cls, parent_model, exclude_models):
        prefetch_related = []
        for field_name, model in cls.get_nested_models(parent_model).items():
            if model not in exclude_models:
                current_prefetch = f"__{field_name}"
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
    def get_parent_prefetch(cls, field_name):
        parent_prefetch = []
        for prefetch in cls.parent_prefetch:
            child_prefetch = prefetch.split('__')
            if child_prefetch[0] == field_name and 0 < len(child_prefetch) - 1 <= cls.Meta.depth:
                parent_prefetch.append("__".join(child_prefetch[1:]))
        return parent_prefetch

    def get_default_field_names(self, declared_fields, model_info):
        return (
            [model_info.pk.name] +
            list(declared_fields) +
            list(model_info.fields) +
            list(set(field.split('__')[0] for field in self.parent_prefetch))
        )

    def build_nested_field(self, field_name, relation_info, nested_depth):
        serializer = self.get_serializer(relation_info.related_model, mode=f"Read{self.Meta.model.__name__}Nested")
        serializer.parent_prefetch = self.get_parent_prefetch(field_name)
        serializer.Meta.depth = nested_depth - 1
        return serializer, get_nested_relation_kwargs(relation_info)

    def create_nested(self, data):
        representation = {}
        for field_name, model in self._nested_models.items():
            field_data = data.get(field_name, None)
            if isinstance(field_data, dict):
                data[field_name], representation[field_name] = self.get_or_create(model, field_data)
            if isinstance(field_data, list):
                data[field_name], representation[field_name] = self.get_or_create_many(model, field_data)
        self.initial_data = data
        if self.is_valid():
            return self.save().pk, dict(self.data, **representation)
        representation["ERROR"] = self.errors
        return "Fail to serialize %s" % self.Meta.model.__name__, representation

    def get_or_create(self, model, data: dict):
        try:
            instance = model.objects.get(pk=data[model._meta.pk.name])
        except:
            instance = None
        return self.get_serializer(model, mode="Nested")(
            instance, data=data, context=self.context, partial=bool(instance)
        ).create_nested(data)

    def get_or_create_many(self, model, list_data: list):
        primary_keys, representations = [], []
        for data in list_data:
            pk, representation = self.get_or_create(model, data) if isinstance(data, dict) else (data, data)
            primary_keys.append(pk)
            representations.append(representation)
        return primary_keys, representations

    def deep_create(self, data: dict | list):
        result = None
        try:
            with atomic():
                if isinstance(data, dict):
                    primary_key, representation = self.get_or_create(self.Meta.model, data)
                    result = representation
                    if "ERROR" in representation:
                        raise Exception(representation['ERROR'])
                if isinstance(data, list):
                    primary_keys, representations = self.get_or_create_many(self.Meta.model, data)
                    result = representations
                    if any("ERROR" in d for d in representations):
                        raise Exception([
                            representation['ERROR'] if 'ERROR' in representation else None
                            for representation in representations
                        ])
        except Exception as e:
            print(e)
        return result

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
