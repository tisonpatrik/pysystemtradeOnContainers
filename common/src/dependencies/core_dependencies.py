from fastapi import Request

from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_client(request: Request) -> RestClient:
    return RestClient(request.app.state.requests_client)
