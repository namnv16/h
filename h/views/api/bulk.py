from logging import getLogger

from pyramid.response import Response

from h.h_api.bulk_api import BulkAPI
from h.h_api.bulk_api.executor import AutomaticReportExecutor
from h.views.api.config import api_config

LOG = getLogger(__name__)


class FakeBulkAPI(BulkAPI):
    """Temporary stub for return values.

    When this work is complete, BulkAPI will return values for us. But right
    now it doesn't and we need something to prove we can build a return value.
    """

    @classmethod
    def from_byte_stream(cls, byte_stream, executor, observer=None):
        super().from_byte_stream(byte_stream, executor, observer=None)

        yield b'["Line 1"]\n'
        yield b'["Line 2"]\n'


@api_config(
    versions=["v1", "v2"],
    route_name="api.bulk",
    request_method="POST",
    link_name="bulk",
    description="Perform multiple operations in one call",
    subtype="x-ndjson",
    # No idea what to put here or what's required to make it work
    # permission="update",
)
def bulk(request):
    """Retrieve the groups for this request's user."""

    results = FakeBulkAPI.from_byte_stream(
        request.body_file, executor=AutomaticReportExecutor()
    )

    # No return view is required (not implemented yet)
    # if results is None:
    #    return Response(status=204)

    # An NDJSON response is required
    return Response(app_iter=results, status=200, content_type="application/x-ndjson")
