import datetime

from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.schemas import get_schema_view
from enumfields.drf.fields import EnumField
from django.core.cache import cache
from openapi_codec import OpenAPICodec

from . import models, serializers


class CurrentStatusApi(APIView):
    """Get current breakdown status"""

    def get(self, request, **kwargs):
        last_span = models.Downtime.objects.order_by("-start").first()
        last_updated = cache.get("tweetdb:last_update")
        if last_updated:
            last_updated = datetime.datetime.fromtimestamp(last_updated)
            last_updated = DateTimeField().to_representation(last_updated)

        return Response(
            {
                "status": EnumField(models.Status, ints_as_names=True).to_representation(last_span.get_latest_status()),
                "last_span": serializers.DowntimeSerializer(last_span).data,
                "last_updated": last_updated,
            }
        )


class SpanPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class SpanApi(ListAPIView):
    """List breakdown spans"""

    queryset = models.Downtime.objects.all().order_by("-id")
    serializer_class = serializers.DowntimeSerializer
    pagination_class = SpanPagination


class SwaggerRenderer(renderers.BaseRenderer):
    media_type = "application/openapi+json"
    format = "swagger"

    def render(self, data, media_type=None, renderer_context=None):
        codec = OpenAPICodec()
        return codec.dump(data)


schema = get_schema_view(
    title="When did BTS broke last?", renderer_classes=[SwaggerRenderer, renderers.CoreJSONRenderer]
)
