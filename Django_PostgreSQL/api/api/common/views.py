from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import DeepSerializer, FilesSerializer


########################################################################################################################
#
########################################################################################################################


class ReadOnlyDeepViewset(ReadOnlyModelViewSet):
    _viewsets = {}
    _mode = "Read"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.queryset:
            _model = cls.queryset.model
            cls._viewsets[cls._mode + _model.__name__] = cls
            cls._fields = {field.name for field in _model._meta.get_fields()}
            cls.serializer_class = cls.get_serializer_class()
            cls.depth = cls.serializer_class.Meta.depth if hasattr(cls.serializer_class.Meta, 'depth') else 0

    @classmethod
    def init_router(cls, router, models: list):
        for model in models:
            router.register(model.__name__, cls.get_viewsets(model))

    @classmethod
    def get_serializer_class(cls):
        return DeepSerializer.get_serializer(cls.queryset.model, mode=cls._mode)

    def get_queryset(self):
        params = self.request.query_params
        depth = int(params.get("depth", self.depth))
        serializer = self.get_serializer_class()
        serializer.Meta.depth = depth
        queryset = self.queryset.select_related(*serializer._select_related) if depth > 0 else self.queryset
        queryset = queryset.prefetch_related(*serializer.get_prefetch_related()) if depth > 1 else queryset
        filter_by = {name: params[name] for name in self._fields if name in params}
        queryset = queryset.filter(**filter_by) if filter_by else queryset
        if order_by := params.get("order_by", None):
            list_order_by = order_by if isinstance(order_by, list) else [order_by]
            queryset = queryset.order_by(*[field for field in list_order_by if field.replace("-", "") in self._fields])
        return queryset

    @classmethod
    def get_viewsets(cls, _model, mode: str = ""):
        if mode + _model.__name__ not in cls._viewsets:

            class CommonViewSet(cls):
                _mode = mode
                queryset = _model.objects
                depth = 0

            CommonViewSet.__name__ = _model.__name__
            CommonViewSet.__doc__ = f"View Set for the model: '{_model.__name__}' used for {mode if mode else 'Read and Write'}"

        return cls._viewsets[mode + _model.__name__]


class DeepViewSet(ReadOnlyDeepViewset, ModelViewSet):
    _mode = ""


class UploadViewSet(DeepViewSet):
    _mode = "Upload"

    @classmethod
    def get_serializer_class(cls):
        return FilesSerializer.get_upload_serializer(cls.queryset.model)


class SpecialDeepViewset(DeepViewSet):

    def create(self, request, *args, **kwargs):
        result, created = self.get_serializer().deep_create(request.data)
        created["pk"] = result
        return Response(created, status=status.HTTP_201_CREATED, headers=self.get_success_headers(created))

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        result = serializer.deep_delete(self.get_object())
        return Response(result, status=status.HTTP_204_NO_CONTENT)
