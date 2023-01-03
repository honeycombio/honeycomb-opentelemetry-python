import typing
import requests
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from honeycomb.opentelemetry.options import HoneycombOptions, is_classic


class LocalTraceLinkSpanExporter(SpanExporter):
    """Implementation of :class:`SpanExporter` that prints direct trace links
    to Honeycomb to the console.
    This class can be used for diagnostic purposes. It prints the exported
    spans to the console STDOUT.
    """

    def __init__(
        self,
        options: HoneycombOptions,
    ):
        if not options.service_name or not options.traces_apikey:
            print("disabling local visualisations - must have both" +
                  "service name and API key configured.")
            return

        self.trace_link_url = self._build_trace_link_url(
            options.traces_apikey,
            options.service_name
        )

    def export(self, spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
        """Exports a batch of telemetry data.
        """
        if self.trace_link_url:
            for span in spans:
                # only print out links for root spans (span without a parent)
                if not span.parent:
                    print(
                        "Honeycomb link: " +
                        self._build_url(span.context.trace_id)
                    )
        return SpanExportResult.SUCCESS

    def force_flush(self) -> bool:
        """Ensures all telemetry waiting to be dispatched is processed.
        """
        return True

    def _build_trace_link_url(self, apikey: str, service_name: str):
        resp = requests.get(
            "https://api.honeycomb.io/1/auth",
            headers={"x-honeycomb-team": apikey},
            timeout=30000  # 30 seconds
        )
        if not resp.ok:
            print("failed to get auth data from Honeycomb API")
            return None

        resp_data = resp.json()
        team_slug = resp_data["team"]["slug"]
        if "environment" in resp_data:
            environment_slug = resp_data["environment"]["slug"]

        url = f"https://ui.honeycomb.io/{team_slug}"
        if not is_classic(apikey) and environment_slug:
            url += f"/environments/{environment_slug}"
        url += f"/datasets/{service_name}/trace?trace_id"
        return url

    def _build_url(self, trace_id: int):
        return f"{self.trace_link_url}={trace_id:x}"
