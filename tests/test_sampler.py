from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.sampler import configure_sampler, DeterministicSampler

from opentelemetry.sdk.trace.sampling import (
    DEFAULT_OFF,
    DEFAULT_ON,
    ParentBasedTraceIdRatio
#     SamplingDecision,
#     SamplingResult
)


def test_undefined_defaults_to_DEFAULT_ON():
    deterministic_sampler = configure_sampler()
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 1
    assert deterministic_sampler._sampler == DEFAULT_ON

    # TODO: get result decision, assert RECORD_AND_SAMPLED, 
    # assert sample rate attribute


def test_sampler_with_rate_of_1_defaults_to_DEFAULT_ON():
    deterministic_sampler = configure_sampler(HoneycombOptions(sample_rate=1))
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 1
    assert deterministic_sampler._sampler == DEFAULT_ON

    # TODO: get result decision, assert RECORD_AND_SAMPLED
    # assert sample rate attribute

# SEE: failing options tests for setting 0 as a rate.
# def test_sampler_with_rate_of_0_defaults_to_DEFAULT_OFF():
#     options = HoneycombOptions(sample_rate=0)
#     deterministic_sampler = configure_sampler(options)
#     assert isinstance(deterministic_sampler, DeterministicSampler)
#     assert deterministic_sampler.rate == 0
#     assert deterministic_sampler._sampler == DEFAULT_OFF


def test_sampler_with_rate_of_10_configures_ParentBasedTraceIdRatio():
    deterministic_sampler = configure_sampler(HoneycombOptions(sample_rate=10))
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 10
    assert isinstance(deterministic_sampler._sampler, ParentBasedTraceIdRatio)

    # TODO: test result decisions
    # assert sample rate attribute

# TODO: add a test that our custom sample rate has been added AND other attributes are intact?