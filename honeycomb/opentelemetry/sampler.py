from opentelemetry.sdk.trace.sampling import (
    Sampler,
    SamplingResult,
    ALWAYS_OFF, 
    ALWAYS_ON,
    ParentBasedTraceIdRatio
) 
# not Decision // call and inner sampler instead

from opentelemetry.trace import Link, SpanKind, get_current_span
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes
from opentelemetry.context import Context

from honeycomb.opentelemetry.options import HoneycombOptions
from logging import getLogger

_logger = getLogger(__name__)

def configure_sampler(
    options: HoneycombOptions = HoneycombOptions(),
):
    _logger.debug(f"🐝 Setting a Sample Rate of {options.sample_rate} 🐝")
    # question: any user guards against non-valid sample rates?

    #return DeterministicSampler(
#         # rate (number)
#         # if undefined, set rate to default, else use given sample rate
#     )

# define the DeterministicSampler, based off upstream Sampler
class DeterministicSampler(Sampler):
    """
    Custom samplers can be created by subclassing Sampler and implementing
    Sampler.should_sample as well as Sampler.get_description.
    """

    def _configure(self, **kwargs):
        configure_sampler()
        #logic here for which sampler 
            # sample rate 0? use always off
            # sample rate 1? use always on
            # any other positive whole number, user 1/number as the ratio with the ratio sampler


    def should_sample(
        self,
        parent_context: Context,
        trace_id: int,
        name: str,
        kind: SpanKind = None,
        attributes: Attributes = None,
        links: Link = None,
        trace_state: "TraceState" = None,
    ) -> "SamplingResult":
        pass
        # call on a logic to determine which inner sampler
        
        # return sampler with contexts (i.e.
            # parent_context: Context,
            # trace_id: int,
            # name: str,
            # kind: SpanKind = None,
            # attributes: Attributes = None,
            # links: Link = None,)

        # don't forget to append our sample rate to attributes


    def get_description(self) -> str:
        return "HNYDeterministicSampler"

# if sampling_result.decision.is_sampled()
# AttributeError: 'NoneType' object has no attribute 'decision'