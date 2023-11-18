import re

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
            cls._exclude_models = [model]
            cls._exclude_models_for_prefetch = [model]
            cls._serializers[cls._mode + model.__name__] = cls
            cls._all_fields = {}
            cls._nested_models = {}
            cls._select_related = []
            for field_name, field in model_meta.get_field_info(model).fields.items():
                cls._all_fields[field_name] = field
            for field_name, field in model_meta.get_field_info(model).relations.items():
                if not field_name.endswith("_set"):
                    cls._all_fields[field_name] = field
                    cls._nested_models[field_name] = field.related_model
                    cls._select_related.append(field_name)
            for field_name, field in model_meta.get_field_info(model).reverse_relations.items():
                cls._all_fields[field_name] = field
                cls._nested_models[field_name] = field.related_model
                cls._select_related.append(field_name)
            cls._prefetch_related = [related[2:] for related in cls.build_prefetch_related(model, cls._exclude_models)]

    def __init__(self, *args, **kwargs):
        self.exclude_models = self._exclude_models
        self._exclude_models = [self.Meta.model]
        super().__init__(*args, **kwargs)

    def get_default_field_names(self, declared_fields, model_info):
        return [model_info.pk.name] + list(self._all_fields) + list(declared_fields)

    def build_nested_field(self, field_name, relation_info, nested_depth):
        serializer = self.get_serializer(relation_info.related_model, mode=f"Read{self.Meta.model.__name__}Nested")
        serializer._exclude_models += self.exclude_models
        if exclude_names := tuple(k for k, v in serializer._nested_models.items() if v in self.exclude_models):
            serializer.Meta.fields = None
            serializer.Meta.exclude = exclude_names
        serializer.Meta.depth = nested_depth - 1
        return serializer, get_nested_relation_kwargs(relation_info)

    @classmethod
    def build_prefetch_related(cls, parent_model, exclude_models):
        prefetch_related = []
        for field_name, field in model_meta.get_field_info(parent_model).relations.items():
            model = field.related_model
            if model not in exclude_models:
                current_prefetch = f"__{field_name}"
                prefetch_related.append(current_prefetch)
                for prefetch in cls.build_prefetch_related(model, exclude_models + [model]):
                    prefetch_related.append(current_prefetch + prefetch)
        return prefetch_related

    @classmethod
    def get_prefetch_related(cls):
        return [
            related
            for related in cls._prefetch_related
            if 0 < len(re.findall('__', related)) < cls.Meta.depth
        ]

    def deep_list_create(self, data):
        return [self.deep_create(item)[1] for item in data]

    def deep_create(self, data):
        result_pk, representation = "", {}
        try:
            with atomic():
                result_pk, representation = self.deep_get_or_create(data, self.Meta.model)
                if "ERROR" in representation:
                    raise Exception(representation["ERROR"])
                representation["pk"] = result_pk
        except Exception as e:
            print(e)
        return result_pk, representation

    def deep_get_or_create(self, data, model):
        try:
            instance = model.objects.get(pk=data[model._meta.pk.name])
        except:
            instance = None
        return self.get_serializer(model, mode="Nested")(
            instance, data=data, context=self.context, partial=True if instance else False
        ).create_child(data)

    def create_child(self, validated_data):
        representation = {}
        for field_name, field_model in self._nested_models.items():
            data = validated_data.get(field_name, None)
            if isinstance(data, dict):
                validated_data[field_name], representation[field_name] = self._deep_create(
                    data, field_model
                )
            elif isinstance(data, list):
                representation[field_name] = list(data)
                for index, item in enumerate(data):
                    if isinstance(item, dict):
                        validated_data[field_name][index], representation[field_name][index] = self._deep_create(
                            item, field_model
                        )
        self.initial_data = validated_data
        if self.is_valid():
            return self.save().pk, dict(self.data, **representation)
        representation["ERROR"] = self.errors
        return "Fail to serialize %s" % self.Meta.model.__name__, representation

    @classmethod
    def get_serializer(cls, _model, mode: str = ""):
        if mode + _model.__name__ not in cls._serializers:
            parent = cls.get_serializer(_model) if mode else DeepSerializer

            class CommonSerializer(parent):
                _mode = mode

                class Meta:
                    model = _model
                    depth = 0
                    fields = '__all__'

            CommonSerializer.Meta.fields = parent.Meta.fields if mode else '__all__'

        return cls._serializers[mode + _model.__name__]


########################################################################################################################
#
########################################################################################################################


class FilesSerializer(DeepSerializer):
    file = serializers.FileField()
    _mode = "Upload"

    @classmethod
    def get_upload_serializer(cls, _model):
        if "Upload" + _model.__name__ not in cls._serializers:
            class UploadSerializer(FilesSerializer):
                _mode = "Upload"

                class Meta:
                    model = _model
                    depth = 0
                    fields = ['file']

        return cls._serializers["Upload" + _model.__name__]
