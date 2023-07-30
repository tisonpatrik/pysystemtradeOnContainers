from uuid import UUID, uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.errors import EntityDoesNotExist
from src.db.repositories.multiple_prices import MultiplePricesRepository
from src.schemas.multiple_prices import MultiplePricesPatch


@pytest.mark.asyncio
async def test_create_multiple_prices(db_session: AsyncSession, create_multiple_prices):
    multiple_prices = create_multiple_prices()
    repository = MultiplePricesRepository(db_session)

    db_multiple_prices = await repository.create(multiple_prices)

    assert db_multiple_prices.amount == multiple_prices.amount
    assert db_multiple_prices.description == multiple_prices.description
    assert isinstance(db_multiple_prices.id, UUID)


@pytest.mark.asyncio
async def test_get_multiple_pricess(db_session: AsyncSession, create_multiple_prices):
    multiple_prices = create_multiple_prices()
    repository = MultiplePricesRepository(db_session)
    await repository.create(multiple_prices)

    db_multiple_pricess = await repository.list()

    assert isinstance(db_multiple_pricess, list)
    assert db_multiple_pricess[0].amount == multiple_prices.amount
    assert db_multiple_pricess[0].description == multiple_prices.description


@pytest.mark.asyncio
async def test_get_multiple_prices_by_id(db_session: AsyncSession, create_multiple_prices):
    multiple_prices = create_multiple_prices()
    repository = MultiplePricesRepository(db_session)

    multiple_prices_created = await repository.create(multiple_prices)
    multiple_prices_db = await repository.get(multiple_prices_id=multiple_prices_created.id)

    assert multiple_prices_created == multiple_prices_db


@pytest.mark.asyncio
async def test_get_multiple_prices_by_id_not_found(db_session: AsyncSession):
    repository = MultiplePricesRepository(db_session)

    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(multiple_prices_id=uuid4())


@pytest.mark.asyncio
async def test_update_multiple_prices(db_session: AsyncSession, create_multiple_prices):
    init_amount = 10
    init_description = "Initial Description"
    final_amount = 20
    final_description = "Final Description"
    multiple_prices = create_multiple_prices(amount=init_amount, description=init_description)
    repository = MultiplePricesRepository(db_session)
    db_multiple_prices = await repository.create(multiple_prices)

    update_multiple_prices = await repository.patch(
        multiple_prices_id=db_multiple_prices.id,
        multiple_prices_patch=MultiplePricesPatch(
            amount=final_amount, description=final_description
        ),
    )

    assert update_multiple_prices.id == db_multiple_prices.id
    assert update_multiple_prices.amount == final_amount
    assert update_multiple_prices.description == final_description


@pytest.mark.asyncio
async def test_soft_delete_multiple_prices(db_session: AsyncSession, create_multiple_prices):
    multiple_prices = create_multiple_prices()
    repository = MultiplePricesRepository(db_session)
    db_multiple_prices = await repository.create(multiple_prices)

    delete_multiple_prices = await repository.delete(multiple_prices_id=db_multiple_prices.id)

    assert delete_multiple_prices is None
    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(multiple_prices_id=db_multiple_prices.id)
