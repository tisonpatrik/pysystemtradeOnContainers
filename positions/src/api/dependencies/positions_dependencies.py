from fastapi import Request

from common.src.database.repository import Repository


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)
