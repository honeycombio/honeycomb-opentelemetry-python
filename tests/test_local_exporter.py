from honeycomb.opentelemetry.local_exporter import LocalTraceLinkSpanExporter
from honeycomb.opentelemetry.options import HoneycombOptions

APIKEY = "0000000000000000000000" # 22 chars
CLASSIC_APIKEY = "00000000000000000000000000000000" # 32 chars
TRACE_ID = 220134740205765644819457394801066567152

def test_exporter_formats_correct_url(requests_mock):
    requests_mock.get("https://api.honeycomb.io/1/auth", json = { "environment": { "slug": "my-env"}, "team": { "slug": "my-team"} })
    options = HoneycombOptions(apikey=APIKEY, service_name="my-service")
    exporter = LocalTraceLinkSpanExporter(options)
    url = exporter._build_url(TRACE_ID)
    assert url == "https://ui.honeycomb.io/my-team/environments/my-env/datasets/my-service/trace?trace_id=a59c68a6de76d5e642bdc9a7641ae5f0"


def test_exporter_formats_correct_url_clasic(requests_mock):
    requests_mock.get("https://api.honeycomb.io/1/auth", json = { "team": { "slug": "my-team"} })
    options = HoneycombOptions(apikey=CLASSIC_APIKEY, service_name="my-service")
    exporter = LocalTraceLinkSpanExporter(options)
    url = exporter._build_url(TRACE_ID)
    assert url == "https://ui.honeycomb.io/my-team/datasets/my-service/trace?trace_id=a59c68a6de76d5e642bdc9a7641ae5f0"
