from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import DeepSerializer


########################################################################################################################
#
########################################################################################################################


class ReadOnlyDeepViewSet(ReadOnlyModelViewSet):
    _viewsets = {}
    _mode = "Read"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.queryset:
            cls._viewsets[cls._mode + cls.queryset.model.__name__] = cls
            cls._fields = {field.name for field in cls.queryset.model._meta.get_fields()}

    @classmethod
    def init_router(cls, router, models: list):
        for model in models:
            router.register(model.__name__, cls.get_view(model), basename=model.__name__)

    def get_serializer_class(self):
        return DeepSerializer.get_serializer(self.queryset.model, mode=self._mode)

    def get_queryset(self):
        params = self.request.query_params
        queryset = self.queryset
        serializer = self.get_serializer_class()
        serializer.Meta.depth = int(params.get("depth", 0))
        if serializer.Meta.depth > 0:
            queryset = queryset.prefetch_related(*serializer.get_prefetch_related())
        if filter_by := {name: params[name] for name in self._fields if name in params}:
            queryset = queryset.filter(**filter_by) if filter_by else queryset
        if order_by := params.get("order_by", None):
            list_order_by = order_by if isinstance(order_by, list) else [order_by]
            queryset = queryset.order_by(*[field for field in list_order_by if field.replace("-", "") in self._fields])
        return queryset

    @classmethod
    def get_view(cls, _model, mode: str = ""):
        if mode + _model.__name__ not in cls._viewsets:

            class CommonViewSet(cls):
                _mode = mode
                queryset = _model.objects
                depth = 0

            CommonViewSet.__name__ = _model.__name__
            CommonViewSet.__doc__ = f"View Set for the model: '{_model.__name__}' used for {mode if mode else 'Read and Write'}"

        return cls._viewsets[mode + _model.__name__]


class DeepViewSet(ReadOnlyDeepViewSet, ModelViewSet):
    _mode = ""
