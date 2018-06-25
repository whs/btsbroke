import datetime

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.pagination import LimitOffsetPagination
from django.core.cache import cache

from . import models, serializers


class CurrentStatusApi(APIView):
    def get(self, request, **kwargs):
        last_span = models.Downtime.objects.order_by("-start").first()
        last_updated = cache.get("tweetdb:last_update")
        if last_updated:
            last_updated = datetime.datetime.fromtimestamp(last_updated)
            last_updated = DateTimeField().to_representation(last_updated)

        return Response(
            {
                "status": last_span.get_latest_status().name,
                "status_id": last_span.get_latest_status().value,
                "last_span": serializers.DowntimeSerializer(last_span).data,
                "last_updated": last_updated,
            }
        )


class SpanPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class SpanApi(ListAPIView):
    queryset = models.Downtime.objects.all().order_by("-id")
    serializer_class = serializers.DowntimeSerializer
    pagination_class = SpanPagination
