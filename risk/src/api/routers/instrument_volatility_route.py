import httpx
from fastapi import APIRouter, Depends, Request, status

from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get("/test_route/{symbol}/", status_code=status.HTTP_200_OK, name="test_route")
async def test_route(symbol: str, request: Request):
    # Assuming you have an HTTP client setup on your FastAPI app instance for reuse
    requests_client = request.app.state.requests_client

    try:
        # Replace "risk:8000" with the appropriate service name and port as defined in your docker-compose.yml
        response = await requests_client.get(f"http://raw_data:8000/fx_prices_route/get_fx_rate_by_symbol/{symbol}/")

        # Check if the response status is OKsymbol
        if response.status_code == 200:
            return response.json()
        else:
            # Handle non-OK responses or add more specific error handling as needed
            return {"error": "Failed to fetch data", "status_code": response.status_code}
    except httpx.RequestError as e:
        logger.error(f"An error occurred while trying to fetch FX rate for symbol {symbol}. Error: {e}")
        return {"error": "Unable to reach the service", "details": str(e)}
