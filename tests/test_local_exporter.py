from honeycomb.opentelemetry.local_exporter import LocalTraceLinkSpanExporter
from honeycomb.opentelemetry.options import HoneycombOptions

APIKEY = "0000000000000000000000" # 22 chars
CLASSIC_APIKEY = "00000000000000000000000000000000" # 32 chars


def test_exporter_formats_correct_url(requests_mock):
    requests_mock.get("https://api.honeycomb.io/1/auth", json = { "environment": { "slug": "my-env"}, "team": { "slug": "my-team"} })
    options = HoneycombOptions(apikey=APIKEY, service_name="my-service")
    exporter = LocalTraceLinkSpanExporter(options)
    assert exporter.trace_link_url == "https://ui.honeycomb.io/my-team/environments/my-env/datasets/my-service/trace?trace_id"


def test_exporter_formats_correct_url_clasic(requests_mock):
    requests_mock.get("https://api.honeycomb.io/1/auth", json = { "team": { "slug": "my-team"} })
    options = HoneycombOptions(apikey=CLASSIC_APIKEY, service_name="my-service")
    exporter = LocalTraceLinkSpanExporter(options)
    assert exporter.trace_link_url == "https://ui.honeycomb.io/my-team/datasets/my-service/trace?trace_id"
