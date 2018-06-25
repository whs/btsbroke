from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import api_views

urlpatterns = [
    # path("current_status", name="current_status"),
]

urlpatterns += format_suffix_patterns(
    [
        re_path(r"^current_status$", api_views.CurrentStatusApi.as_view(), name="current_status_api"),
        # re_path(r"^spans$", name="span_api"),
    ],
    suffix_required=True,
)
