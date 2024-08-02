import httpx

from common.src.http_client.requests.fetch_request import FetchRequest
from common.src.http_client.requests.post_request import PostRequest
from common.src.logging.logger import AppLogger


class RestClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.logger = AppLogger.get_instance().get_logger()

    async def get_data_async(self, request: FetchRequest) -> dict:
        try:
            response = await self.client.get(request.url_string, params=request.params, timeout=10.0)
            response.raise_for_status()
            self.logger.info("GET request successful")
            return response.json()
        except httpx.HTTPStatusError as exc:
            self.logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            raise
        except httpx.RequestError as exc:
            self.logger.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to complete GET request: {e}")
            raise

    async def post_data_async(self, request: PostRequest) -> dict:
        try:
            response = await self.client.post(request.url_string, json=request.data)
            response.raise_for_status()
            self.logger.info("POST request successful")
            return response.json()
        except httpx.HTTPStatusError as exc:
            self.logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            raise
        except httpx.RequestError as exc:
            self.logger.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to complete POST request: {e}")
            raise
