from common.src.http_client.requests.fetch_request import FetchRequest
from raw_data.src.validation.factor_name import FactorName


class GetHistoricAverageFactorValueAllAssetsQuery(FetchRequest):
    factor_name: FactorName
    lookback: int

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/historic_average_factor_value_all_assets_route/get_historic_average_factor_value_all_assets/"
