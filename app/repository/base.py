from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
import logging

from app.exceptions import ObjectAlreadyExistsException
from app.repository.datamapper.base import DataMapper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filters_, **filter_by):
        query = select(self.model).filter(*filters_).filter_by(**filter_by)
        result = await self.session.execute(query)
        return self.mapper.alchemy_to_pydantic(result.scalars().one())

    async def get_all(self, *args, **kwargs):
        return self.get_filtered()

    async def add(self, model: BaseModel):
        try:
            stmt = insert(self.model).values(**model.model_dump()).returning(self.model)
            result = await self.session.execute(stmt)
            return self.mapper.alchemy_to_pydantic(result.scalars().one())

        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException
            else:
                logger.info(
                    f"Не удалось обработать, переданные данные {model.model_dump()} - ошибка {ex.orig.__cause__}"
                )
                raise ex

    async def update(self, data: BaseModel, exclude_unset=True, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        ).returning(self.model)
        res = await self.session.execute(stmt)
        result = res.scalars().one()
        return self.mapper.alchemy_to_pydantic(result)
