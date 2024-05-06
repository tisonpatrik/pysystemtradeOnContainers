from httpx import AsyncClient

from common.src.http_client.requests.fetch_request import FetchRequest
from common.src.http_client.requests.post_request import PostRequest
from common.src.logging.logger import AppLogger


class RestClient:
    def __init__(self, client: AsyncClient):
        self.client = client
        self.logger = AppLogger.get_instance().get_logger()

    async def get_data_async(self, request: FetchRequest) -> dict:
        try:
            self.logger.debug(f"Sending GET request to {request.url_string} with params {request.params}")
            response = await self.client.get(request.url_string, params=request.params)
            response.raise_for_status()
            self.logger.info("GET request successful")
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to complete GET request: {e}")
            raise

    async def post_data_async(self, request: PostRequest) -> dict:
        try:
            self.logger.debug(f"Sending POST request to {request.url_string} with data {request.data}")
            response = await self.client.post(request.url_string, json=request.data)
            response.raise_for_status()
            self.logger.info("POST request successful")
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to complete POST request: {e}")
            raise
