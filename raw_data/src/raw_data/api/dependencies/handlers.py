from common.clients.dependencies import get_daily_prices_client, get_instruments_client, get_redis
from common.database.repository import PostgresClient

from raw_data.api.handlers.absolute_skew_deviation_handler import AbsoluteSkewDeviationHandler
from raw_data.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from raw_data.api.handlers.average_neg_skew_in_asset_class_for_instrument_handler import (
    AverageNegSkewInAssetClassForInstrumentHandler,
)
from raw_data.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler
from raw_data.api.handlers.current_average_negskew_over_all_assets_handler import (
    CurrentAverageNegSkewOverAllAssetsHandler,
)
from raw_data.api.handlers.current_average_negskew_over_asset_class_handler import CurrentAverageNegSkewOverAssetClassHandler
from raw_data.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.api.handlers.daily_vol_normalized_price_for_asset_handler import DailyVolNormalizedPriceForAssetHandler
from raw_data.api.handlers.daily_vol_normalized_returns_handler import DailyVolNormalizedReturnsHandler
from raw_data.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.api.handlers.historic_average_negskew_all_assets_handler import (
    HistoricAverageNegSkewAllAssetsHandler,
)
from raw_data.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from raw_data.api.handlers.median_carry_for_asset_class_handler import MedianCarryForAssetClassHandler
from raw_data.api.handlers.neg_skew_all_instruments_handler import NegSkewAllInstrumentsHandler
from raw_data.api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler
from raw_data.api.handlers.normalized_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler
from raw_data.api.handlers.raw_carry_handler import RawCarryHandler
from raw_data.api.handlers.relative_skew_deviation_handler import RelativeSkewDeviationHandler
from raw_data.api.handlers.skew_handler import SkewHandler
from raw_data.api.handlers.smooth_carry_handler import SmoothCarryHandler
from raw_data.api.handlers.vol_attenuation_handler import VolAttenuationHandler


class HandlerFactory:
    def __init__(self, postgres: PostgresClient):
        self.redis = get_redis()
        self.postgres = postgres
        self.prices_client = get_daily_prices_client(postgres=self.postgres, redis=self.redis)
        self.instruments_client = get_instruments_client(postgres=self.postgres)
        self.instrument_repository = get_instruments_client(postgres=self.postgres)

    def get_daily_returns_handler(self) -> DailyReturnsHandler:
        return DailyReturnsHandler(prices_client=self.prices_client, redis=self.redis)

    def get_daily_percentage_returns_handler(self) -> DailyPercentageReturnsHandler:
        daily_returns_handler = self.get_daily_returns_handler()
        return DailyPercentageReturnsHandler(prices_client=self.prices_client, daily_returns_handler=daily_returns_handler)

    def get_skew_handler(self) -> SkewHandler:
        daily_percentage_returns_handler = self.get_daily_percentage_returns_handler()
        return SkewHandler(daily_percentage_returns_handler=daily_percentage_returns_handler, redis=self.redis)

    def get_negskew_over_instrument_list_handler(self) -> NegSkewOverInstrumentListHandler:
        skew_handler = self.get_skew_handler()
        return NegSkewOverInstrumentListHandler(skew_handler=skew_handler)

    def get_negskew_all_instruments_handler(self) -> NegSkewAllInstrumentsHandler:
        negskew_over_instrument_list_handler = self.get_negskew_over_instrument_list_handler()
        return NegSkewAllInstrumentsHandler(
            instruments_client=self.instruments_client,
            negskew_over_instrument_list_handler=negskew_over_instrument_list_handler,
        )

    def get_current_average_negskew_over_all_assets_handler(self) -> CurrentAverageNegSkewOverAllAssetsHandler:
        negskew_all_instruments_handler = self.get_negskew_all_instruments_handler()
        return CurrentAverageNegSkewOverAllAssetsHandler(negskew_all_instruments_handler=negskew_all_instruments_handler)

    def get_historic_average_negskew_all_assets_handler(self) -> HistoricAverageNegSkewAllAssetsHandler:
        current_average_negskew_over_all_assets_handler = self.get_current_average_negskew_over_all_assets_handler()
        return HistoricAverageNegSkewAllAssetsHandler(
            current_average_negskew_over_all_assets_handler=current_average_negskew_over_all_assets_handler
        )

    def get_absolute_skew_deviation_handler(self) -> AbsoluteSkewDeviationHandler:
        historic_negskew_value_all_assets_handler = self.get_historic_average_negskew_all_assets_handler()
        skew_handler = self.get_skew_handler()
        return AbsoluteSkewDeviationHandler(
            historic_negskew_value_all_assets_handler=historic_negskew_value_all_assets_handler,
            skew_handler=skew_handler,
        )

    def get_fx_prices_handler(self) -> FxPricesHandler:
        instruments_client = get_instruments_client(postgres=self.postgres)
        return FxPricesHandler(instruments_client=instruments_client, prices_client=self.prices_client)

    def get_daily_returns_vol_handler(self) -> DailyReturnsVolHandler:
        daily_returns_handler = self.get_daily_returns_handler()
        return DailyReturnsVolHandler(redis=self.redis, daily_returns_handler=daily_returns_handler)

    def get_daily_percentage_volatility_handler(self) -> DailyPercentageVolatilityHandler:
        daily_returns_vol_handler = self.get_daily_returns_vol_handler()
        return DailyPercentageVolatilityHandler(
            prices_client=self.prices_client,
            redis=self.redis,
            daily_returns_vol_handler=daily_returns_vol_handler,
        )

    def get_instrument_currency_vol_handler(self) -> InstrumentCurrencyVolHandler:
        daily_percentage_volatility_handler = self.get_daily_percentage_volatility_handler()
        return InstrumentCurrencyVolHandler(
            prices_client=self.prices_client,
            instruments_client=self.instruments_client,
            daily_percentage_volatility_handler=daily_percentage_volatility_handler,
        )

    def get_vol_attenuation_handler(self) -> VolAttenuationHandler:
        daily_percentage_volatility_handler = self.get_daily_percentage_volatility_handler()
        return VolAttenuationHandler(daily_percentage_volatility_handler=daily_percentage_volatility_handler, redis=self.redis)

    def get_current_average_negskew_over_asset_class_handler(self) -> CurrentAverageNegSkewOverAssetClassHandler:
        negskew_over_instrument_list_handler = self.get_negskew_over_instrument_list_handler()
        return CurrentAverageNegSkewOverAssetClassHandler(
            instruments_client=self.instruments_client, negskew_over_instrument_list_handler=negskew_over_instrument_list_handler
        )

    def get_average_neg_skew_in_asset_class_for_instrument_handler(self) -> AverageNegSkewInAssetClassForInstrumentHandler:
        current_average_negskew_over_asset_class_handler = self.get_current_average_negskew_over_asset_class_handler()
        return AverageNegSkewInAssetClassForInstrumentHandler(
            instruments_client=self.instruments_client,
            current_average_negskew_over_asset_class_handler=current_average_negskew_over_asset_class_handler,
        )

    def get_relative_skew_deviation_handler(self) -> RelativeSkewDeviationHandler:
        average_neg_skew_in_asset_class_for_instrument_handler = self.get_average_neg_skew_in_asset_class_for_instrument_handler()
        skew_handler = self.get_skew_handler()
        return RelativeSkewDeviationHandler(
            average_neg_skew_in_asset_class_for_instrument_handler=average_neg_skew_in_asset_class_for_instrument_handler,
            skew_handler=skew_handler,
        )

    def get_daily_vol_normalized_returns_handler(self) -> DailyVolNormalizedReturnsHandler:
        daily_returns_vol_handler = self.get_daily_returns_vol_handler()
        daily_returns_handler = self.get_daily_returns_handler()

        return DailyVolNormalizedReturnsHandler(
            daily_returns_vol_handler=daily_returns_vol_handler,
            redis=self.redis,
            daily_returns_handler=daily_returns_handler,
        )

    def get_cumulative_daily_vol_norm_returns_handler(self) -> CumulativeDailyVolNormReturnsHandler:
        daily_vol_normalized_returns_handler = self.get_daily_vol_normalized_returns_handler()
        return CumulativeDailyVolNormReturnsHandler(
            daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler, redis=self.redis
        )

    def get_daily_annualised_roll_handler(self) -> DailyAnnualisedRollHandler:
        return DailyAnnualisedRollHandler(prices_client=self.prices_client)

    def get_raw_carry_handler(self) -> RawCarryHandler:
        daily_annualised_roll_handler = self.get_daily_annualised_roll_handler()
        daily_returns_vol_handler = self.get_daily_returns_vol_handler()
        return RawCarryHandler(
            redis=self.redis,
            daily_annualised_roll_handler=daily_annualised_roll_handler,
            daily_returns_vol_handler=daily_returns_vol_handler,
        )

    def get_median_carry_for_asset_class_handler(self) -> MedianCarryForAssetClassHandler:
        raw_carry_handler = self.get_raw_carry_handler()
        return MedianCarryForAssetClassHandler(raw_carry_handler=raw_carry_handler, instrument_client=self.instrument_repository)

    def get_smooth_carry_handler(self) -> SmoothCarryHandler:
        raw_carry_handler = self.get_raw_carry_handler()
        return SmoothCarryHandler(raw_carry_handler=raw_carry_handler)

    def get_aggregated_returns_for_asset_handler(self) -> AggregatedReturnsForAssetClassHandler:
        daily_vol_normalized_returns_handler = self.get_daily_vol_normalized_returns_handler()
        return AggregatedReturnsForAssetClassHandler(
            instruments_client=self.instruments_client, daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler
        )

    def get_daily_vol_normalized_price_for_asset_handler(self) -> DailyVolNormalizedPriceForAssetHandler:
        aggregated_returns_for_asset_handler = self.get_aggregated_returns_for_asset_handler()
        return DailyVolNormalizedPriceForAssetHandler(aggregated_returns_for_asset_handler=aggregated_returns_for_asset_handler)

    def get_normalized_prices_handler(self) -> NormalizedPricesForAssetClassHandler:
        daily_vol_normalized_price_for_asset_handler: DailyVolNormalizedPriceForAssetHandler = (
            self.get_daily_vol_normalized_price_for_asset_handler()
        )
        cumulative_daily_vol_norm_returns_handler: CumulativeDailyVolNormReturnsHandler = (
            self.get_cumulative_daily_vol_norm_returns_handler()
        )
        return NormalizedPricesForAssetClassHandler(
            instruments_client=self.instruments_client,
            daily_vol_normalized_price_for_asset_handler=daily_vol_normalized_price_for_asset_handler,
            cumulative_daily_vol_norm_returns_handler=cumulative_daily_vol_norm_returns_handler,
        )
