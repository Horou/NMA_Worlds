from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import DeepSerializer


########################################################################################################################
#
########################################################################################################################


class ReadOnlyDeepViewset(ReadOnlyModelViewSet):
    serializer_class = DeepSerializer
    _viewsets = {}
    _serializers = {}
    _models = {}
    _models_fields = {}

    def __init_subclass__(cls, **kwargs):
        if not cls._serializers:
            cls._serializers = dict(DeepSerializer._serializers)
        if cls.queryset:
            nested_model = cls.queryset.model
            serializer_name = nested_model.__name__
            cls._models[nested_model.__name__] = nested_model
            cls._models_fields[nested_model.__name__] = nested_model._meta.get_fields()
            if serializer_name not in cls._serializers:

                class ViewSetSerializer(DeepSerializer):
                    class Meta:
                        model = nested_model
                        fields = '__all__'
                        depth = 1

                cls._serializers[serializer_name] = ViewSetSerializer
            cls._viewsets[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    def get_queryset(self):
        data = self.request.query_params
        fields_name = self._models_fields[self.queryset.model.__name__]
        filter_by = {
            field.name: data[field.name]
            for field in fields_name
            if field.name in data
        }
        queryset = self.queryset.filter(**filter_by) if filter_by else self.queryset
        if "order_by" in data:
            data_order_by = data["order_by"]
            list_order_by = data_order_by if isinstance(data_order_by, list) else [data_order_by]
            fields_names = {field.name for field in fields_name}
            queryset = queryset.order_by(*[field for field in list_order_by if field.replace("-", "") in fields_names])
        return queryset.select_subclasses()


class DeepViewset(ReadOnlyDeepViewset, ModelViewSet):
    def get_serializer_class(self):
        return self._serializers[self.queryset.model.__name__]


class SpecialDeepViewset(DeepViewset):
    def create(self, request, *args, **kwargs):
        block = {"TestModel4"}
        serializer = self.get_serializer()
        result, created = serializer.deep_create(request.data, block=block)
        headers = self.get_success_headers(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        result = serializer.deep_delete(self.get_object())
        return Response(result, status=status.HTTP_204_NO_CONTENT)
