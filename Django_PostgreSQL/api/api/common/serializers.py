import json
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.utils import model_meta
from rest_framework.utils.field_mapping import (get_nested_relation_kwargs,)
from rest_framework.relations import PrimaryKeyRelatedField


########################################################################################################################
#
########################################################################################################################


class OneToManyClassField(serializers.ManyRelatedField):

    def __init__(self, child_serializer=None, relation_name=None, *args, **kwargs):
        assert child_serializer is not None, '`child_serializer` is a required argument.'
        self.child_serializer = child_serializer
        assert relation_name is not None, '`relation_name` is a required argument.'
        self.relation_name = relation_name
        child_model = child_serializer.Meta.model
        assert hasattr(child_model, relation_name), '`%s` has no attribute `%s`.' % (child_model, relation_name)
        super().__init__(child_serializer(), *args, **kwargs)

    class Memoize(dict):
        def __init__(self, func, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.func = func

        def __call__(self, *args, **kwargs):
            return self[args]

        def __missing__(self, key):
            result = self[key] = self.func(*key)
            return result

    @Memoize
    def get_serializer(self, item):
        kwargs, child_serializer = {"context": self.context}, self.child_serializer
        try:
            tmp = self.parent._serializers["%sSerializer" % item["type"]]
            return tmp(kwargs) if issubclass(tmp, child_serializer) else child_serializer(kwargs)
        except KeyError:
            return child_serializer(kwargs)

    def to_internal_value(self, data):
        if isinstance(data, type('')) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return [
            self.get_serializer(item).to_internal_value(item)
            for item in data
        ]

    def run_validators(self, value):
        return [
            self.get_serializer(item).run_validators(item)
            for item in value
        ]

    def create(self, validated_data, instance):
        kwargs = {self.relation_name: instance}
        getattr(instance, self.field_name).all().delete()
        return [
            self.get_serializer(item).create({**item, **kwargs})
            for item in validated_data
        ]

    def to_representation(self, value):
        return [
            self.get_serializer(item).to_representation(item)
            for item in value
        ]


########################################################################################################################
#
########################################################################################################################


class DeepSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    _serializers = {}
    _models = {}

    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, "Meta"):
            model = cls.Meta.model
            cls._models[model.__name__] = model
            cls._serializers[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        reverse_name = kwargs.pop("reverse_name", None)
        if hasattr(self, "Meta"):
            model = self.Meta.model
            if reverse_name:
                assert hasattr(model, reverse_name), '`%s` has no attribute `%s`.' % (model, reverse_name)
                self.reverse_name = reverse_name
            if not hasattr(self.Meta, "depth"):
                self.Meta.depth = 0
            self.serializer_related_field = PrimaryKeyTypeRelatedField
            self._instances = _instances = {
                name: serializer()
                for name, serializer in self._serializers.items()
                if issubclass(serializer.Meta.model, model) and serializer.Meta.model is not model
            }
            for _, instance in _instances.items():
                instance.bind(field_name='', parent=self)
        super().__init__(*args, **kwargs)

    def get_type(self, instance):
        return type(instance).__name__

    def get_default_field_names(self, declared_fields, model_info):
        reverse_relation = [
            name
            for name, field in model_info.reverse_relations.items()
            if field.to_many and not name.endswith("_set")
        ]
        return (
            ["type", "pk"] +
            list(model_info.fields) +
            list(model_info.forward_relations) +
            reverse_relation +
            list(declared_fields)
        )

    def build_field(self, field_name, info, model_class, nested_depth):
        if field_name in info.fields_and_pk:
            model_field = info.fields_and_pk[field_name]
            return self.build_standard_field(field_name, model_field)
        elif field_name in info.relations:
            relation_info = info.relations[field_name]
            if relation_info.reverse and nested_depth:
                return self.build_nested_field(field_name, relation_info, nested_depth)
            else:
                return self.build_relational_field(field_name, relation_info)
        elif hasattr(model_class, field_name):
            return self.build_property_field(field_name, model_class)
        elif field_name == self.url_field_name:
            return self.build_url_field(field_name, model_class)
        return self.build_unknown_field(field_name, model_class)

    def build_nested_field(self, field_name, relation_info, nested_depth):
        model_parent = self.Meta.model
        nested_model = relation_info.related_model
        serializer = self._serializers.get("%sSerializer" % nested_model.__name__, DeepSerializer)

        exclude_name = None
        if relation_info.to_many:
            for name, field in model_meta.get_field_info(nested_model).relations.items():
                if field.related_model is model_parent and not name.endswith("_set"):
                    exclude_name = name
                    break

        class NestedSerializer(serializer):
            class Meta:
                model = nested_model
                depth = nested_depth - 1
                if exclude_name:
                    exclude = (exclude_name,)
                else:
                    fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)
        field_kwargs["reverse_name"] = exclude_name
        field_kwargs["read_only"] = False
        return field_class, field_kwargs

    def create(self, validated_data):
        one_to_many = {}
        fields = self.fields
        reverse_relations = model_meta.get_field_info(self.Meta.model).reverse_relations
        for field_name, relation_info in reverse_relations.items():
            if relation_info.to_many and (field_name in validated_data):
                one_to_many[field_name] = validated_data.pop(field_name)
        instance = super().create(validated_data)
        for attr, value in one_to_many.items():
            if attr in reverse_relations and reverse_relations[attr].to_many:
                field = fields[attr]
                for item in value:
                    item[field.child.reverse_name] = instance
                field.create(value)
        return instance

    def update(self, instance, validated_data):
        fields = self.fields
        reverse_relations = model_meta.get_field_info(self.Meta.model).reverse_relations
        for attr in {**validated_data}:
            if attr in reverse_relations and reverse_relations[attr].to_many:
                value = validated_data.pop(attr)
                field = fields[attr]
                for item in value:
                    item[field.child.reverse_name] = instance
                getattr(instance, attr).all().delete()
                field.create(value)
        return super().update(instance, validated_data)

    def delete(self, instance):
        for name in model_meta.get_field_info(type(instance)).reverse_relations:
            if name.endswith("_set") and getattr(instance, name).all():
                raise PermissionError()
        instance.delete()

    def deep_create(self, data: dict, block=set()):
        _models, _serializers, context, partial = self._models, self._serializers, self.context, True

        def deep_list_create(data1, data2):
            for index, value in enumerate(data1):
                if isinstance(value, dict):
                    data1[index], data2[index] = deep_dict_create(value, data2[index])
                elif isinstance(value, list):
                    data1[index], data2[index] = deep_list_create(value, data2[index])
            return data1, data2

        def deep_dict_create(data1, data2):
            for name, field in data1.items():
                if isinstance(field, dict):
                    data1[name], data2[name] = deep_dict_create(field, data2[name])
                elif isinstance(field, list):
                    data1[name], data2[name] = deep_list_create(field, data2[name])
            data_type = data1["type"] if "type" in data1 else None
            serializer_type = "%sSerializer" % data_type
            if data_type not in block and serializer_type in _serializers:
                try:
                    instance = _models[data_type].objects.get_subclass(pk=data1["pk"])
                    serialized_instance = _serializers[serializer_type](instance, data=data1, context=context, partial=partial)
                except:
                    serialized_instance = _serializers[serializer_type](data=data1, context=context)
                if serialized_instance.is_valid():
                    return serialized_instance.save().pk, serialized_instance.data
                data2["ERROR"] = serialized_instance.errors
                default_data = {"type", "pk", "ERROR", *serialized_instance.data}
                for name in data2:
                    if name not in default_data:
                        data2.pop(name)
                return "Fail to serialize %s" % data_type, data2
            return data1, data2

        created_pk, created_data = deep_dict_create(json.loads(json.dumps(data)), data)
        return created_data, ("pk" in created_data and created_data["pk"] == created_pk)

    def deep_delete(self, instance, block=set()):
        _models, data = self._models, self.to_representation(instance)

        def deep_dict_delete(dict_data):
            deleted = {}
            data_type = dict_data["type"] if "type" in dict_data else None
            data_pk = dict_data["pk"] if "pk" in dict_data else None
            if data_pk and data_type and data_type not in block:
                try:
                    found_instance = _models[data_type].objects.get(pk=data_pk)
                    deleted["type"], deleted["pk"] = data_type, data_pk
                    self.delete(found_instance)
                    deleted["DELETED"] = True
                except:
                    deleted["DELETED"] = False
            if not ("pk" in deleted and not deleted["DELETED"]):
                for name, field in dict_data.items():
                    if isinstance(field, list):
                        result = deep_list_delete(field)
                        if result:
                            deleted[name] = result
                    elif isinstance(field, dict):
                        result = deep_dict_delete(field)
                        if result:
                            deleted[name] = result
            return deleted

        def deep_list_delete(list_data):
            deleted = []
            for field in list_data:
                if isinstance(field, list):
                    result = deep_list_delete(field)
                    if result:
                        deleted.append(result)
                elif isinstance(field, dict):
                    result = deep_dict_delete(field)
                    if result:
                        deleted.append(result)
            return deleted

        return deep_dict_delete(data)

    def to_representation(self, instance):
        instance_type = type(instance)
        if hasattr(self, "Meta") and instance_type is self.Meta.model:
            return super().to_representation(instance)

        serializer_name = "%sSerializer" % instance_type.__name__
        print("regardon si ca marche:  %s" % serializer_name)
        if serializer_name in self._instances:
            print("ca marche")
            return self._instances[serializer_name].to_representation(instance)

        class Serializer(DeepSerializer):
            class Meta:
                model = instance_type
                fields = '__all__'
                depth = 1

        serializer = self._instances[serializer_name] = Serializer()
        serializer.bind(field_name='', parent=self)
        return serializer.to_representation(instance)


class PrimaryKeyTypeRelatedField(PrimaryKeyRelatedField):
    def to_representation(self, value):
        parent = self.parent
        while not isinstance(parent, DeepSerializer):
            parent = parent.parent
        nested_depth = parent.Meta.depth
        if nested_depth <= 0 or not value.pk:
            return super().to_representation(value)

        instance = self.queryset.get_subclass(pk=value.pk)
        nested_model = type(instance)

        class NestedSerializer(DeepSerializer._serializers.get("%sSerializer" % nested_model.__name__, DeepSerializer)):
            class Meta:
                model = nested_model
                depth = nested_depth - 1
                fields = '__all__'

        return NestedSerializer(context=self.context).to_representation(instance)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                super(PrimaryKeyTypeRelatedField, self).to_representation(item),
                self.display_value(item)
            )
            for item in queryset
        ])