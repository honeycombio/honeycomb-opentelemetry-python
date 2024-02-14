from django.http import HttpResponse
from opentelemetry import trace

tracer = trace.get_tracer("hello_world_tracer")

def home_page_view(request):
    with tracer.start_as_current_span(name="hello") as span:
        span.set_attribute("message", "hello world!")
        return HttpResponse("Hello, world")