from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.dependencies.core_dependencies import get_redis
from common.src.logging.logger import AppLogger
from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.redis.redis_repository import RedisRepository
from rules.src.api.dependencies.dependencies import get_breakout_handler
from rules.src.api.handlers.breakout_handler import BreakoutHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_breakout_route/",
    status_code=status.HTTP_200_OK,
    name="Get Breakout",
)
async def get_breakout_for_instrument_async(
    query: GetRuleForInstrumentQuery = Depends(),
    breakout_handler: BreakoutHandler = Depends(get_breakout_handler),
    redis: RedisRepository = Depends(get_redis),
):
    try:
        cache_key = "breakout"
        ttl = 60

        cache_statement = GetCacheStatement(key=cache_key)
        cached_data = await redis.get_cache(cache_statement)
        if cached_data:
            logger.info(f"Cache hit for symbol {query.symbol}")
            return jsonable_encoder(cached_data)

        breakout = await breakout_handler.get_breakout_async(query)
        set_cache_statement = SetCacheStatement(cache_key=cache_key, cache_value=breakout, time_to_live=ttl)
        await redis.set_cache(set_cache_statement)
        return jsonable_encoder(breakout)
    except HTTPException as e:
        logger.error(f"An error occurred while trying to calculate breakout for symbol {query.symbol}. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for symbol {query.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ['rawdata.get_daily_prices', 'rawdata.daily_returns_volatility']
