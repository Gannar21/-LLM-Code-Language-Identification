# token usage -> cost, break-even calc — TBD
"""
Cost calculations. API costs come from real token usage x provider list price.
Local cost comes from hardware cost/hour / requests/hour.
"""

from dataclasses import dataclass


@dataclass
class ApiPricing:
    price_per_1k_input: float
    price_per_1k_output: float


def api_cost_per_request(input_tokens: int, output_tokens: int, pricing: ApiPricing) -> float:
    return (
        (input_tokens / 1000) * pricing.price_per_1k_input
        + (output_tokens / 1000) * pricing.price_per_1k_output
    )


def api_cost_per_1k_requests(avg_input_tokens: float, avg_output_tokens: float, pricing: ApiPricing) -> float:
    per_request = api_cost_per_request(avg_input_tokens, avg_output_tokens, pricing)
    return per_request * 1000


def local_cost_per_request(hardware_cost_per_hour: float, requests_per_hour: float) -> float:
    if requests_per_hour <= 0:
        raise ValueError("requests_per_hour must be > 0 — measure real throughput first")
    return hardware_cost_per_hour / requests_per_hour


def local_cost_per_1k_requests(hardware_cost_per_hour: float, requests_per_hour: float) -> float:
    return local_cost_per_request(hardware_cost_per_hour, requests_per_hour) * 1000


def cost_at_volume(cost_per_request: float, n_requests: int) -> float:
    return cost_per_request * n_requests


def break_even_requests(api_cost_per_request: float, local_cost_per_request: float, local_fixed_cost: float = 0.0):
    marginal_savings = api_cost_per_request - local_cost_per_request
    if marginal_savings <= 0:
        return None
    return local_fixed_cost / marginal_savings


if __name__ == "__main__":
    pricing = ApiPricing(price_per_1k_input=0.05, price_per_1k_output=0.08)
    per_req = api_cost_per_request(input_tokens=150, output_tokens=5, pricing=pricing)
    print(f"API cost/request: ${per_req:.6f}  |  cost/1k requests: ${per_req * 1000:.2f}")