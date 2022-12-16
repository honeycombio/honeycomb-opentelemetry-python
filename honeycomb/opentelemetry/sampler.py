from logging import getLogger

from opentelemetry.sdk.trace.sampling import (
    DEFAULT_ON,
    Sampler,
    SamplingResult
)
# DEFAULT_OFF,
# ParentBasedTraceIdRatio
# not Decision // call and inner sampler instead

from opentelemetry.trace import Link, SpanKind
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes
from opentelemetry.context import Context

from honeycomb.opentelemetry.options import HoneycombOptions

_logger = getLogger(__name__)


def configure_sampler(
    options: HoneycombOptions = HoneycombOptions(),
):
    return DeterministicSampler(options.sample_rate)


class DeterministicSampler(Sampler):
    """
    Custom samplers can be created by subclassing Sampler and implementing
    Sampler.should_sample as well as Sampler.get_description.
    """

    def __init__(self, rate: int):
        # do we need to check for sample rate undefined? I think the
        # options would go back to the default if nothing is put in
        self.rate = rate

    def _configure(self):
        configure_sampler()
        # logic here for which sampler
        # sample rate 0? use default off
        # sample rate 1? use default on
        # any other positive whole number, user 1/number as
        # the ratio with the ratio sampler

    def should_sample(
        self,
        parent_context: Context,
        trace_id: int,
        name: str,
        kind: SpanKind = None,
        attributes: Attributes = None,
        links: Link = None,
        trace_state: "TraceState" = None
    ) -> "SamplingResult":
        # append our SampleRate field to attributes
        sample_rate = {'SampleRate': self.rate}
        if attributes is None:
            attributes = sample_rate
        else:
            attributes.update(sample_rate)

        # TODO: call on a logic to determine which inner sampler
        return DEFAULT_ON.should_sample(
            parent_context,
            trace_id,
            name,
            kind,
            attributes,
            links,
            trace_state
        )

    def get_description(self) -> str:
        return "HNYDeterministicSampler"
