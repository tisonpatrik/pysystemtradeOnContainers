from common.http_client.rest_client import RestClient


class AccountClient:
    def __init__(self, rest_client: RestClient):
        self.client = rest_client

    async def get_SR_cost_for_instrument_forecast_async(self, instrument_code: str, rule_variation_name: str) -> float:
        raise NotImplementedError("Method not implemented")
