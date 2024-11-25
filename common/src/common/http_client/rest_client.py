import httpx
from httpx import AsyncClient

from common.http_client.errors.http_errors import HttpRequestError, HttpStatusError, HttpUnexpectedError
from common.http_client.requests.fetch_request import FetchRequest
from common.http_client.requests.post_request import PostRequest
from common.logging.logger import AppLogger


class RestClient:
    def __init__(self, client: AsyncClient):
        self.client = client
        self.logger = AppLogger.get_instance().get_logger()

    async def get_data_async(self, request: FetchRequest) -> dict:
        try:
            response = await self.client.get(request.url_string, params=request.params, timeout=60.0)
            response.raise_for_status()
            self.logger.info('GET request successful to %s', request.url_string)
            return response.json()
        except httpx.HTTPStatusError as exc:
            self.logger.exception('HTTP status error occurred: %s - %s', exc.response.status_code, exc.response.text)
            raise HttpStatusError(exc.response.status_code, exc.response.text) from exc
        except httpx.RequestError as exc:
            self.logger.exception('An error occurred while requesting %r', exc.request.url)
            raise HttpRequestError(str(exc.request.url), str(exc)) from exc
        except Exception as exc:
            self.logger.exception('Failed to complete GET request to %s', request.url_string)
            raise HttpUnexpectedError(str(exc)) from exc

    async def post_data_async(self, request: PostRequest) -> dict:
        try:
            response = await self.client.post(
                request.url_string,
                json=request.data,
                timeout=20.0,  # Přidání timeout pro konzistenci
            )
            response.raise_for_status()
            self.logger.info('POST request successful to %s', request.url_string)
            return response.json()
        except httpx.HTTPStatusError as exc:
            self.logger.exception('HTTP status error occurred: %s - %s', exc.response.status_code, exc.response.text)
            raise HttpStatusError(exc.response.status_code, exc.response.text) from exc
        except httpx.RequestError as exc:
            self.logger.exception('An error occurred while requesting %r', exc.request.url)
            raise HttpRequestError(str(exc.request.url), str(exc)) from exc
        except Exception as exc:
            self.logger.exception('Failed to complete POST request to %s', request.url_string)
            raise HttpUnexpectedError(str(exc)) from exc
