from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


class CRUDBase:
    """CRUD for all Models."""
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Get object by id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
                )
        )
        db_obj = db_obj.scalars().first()  # type: ignore
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str | int,
        session: AsyncSession,
    ):
        """Get (filter) object by attribute and value."""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        # return db_obj.scalars().first()
        return db_obj.scalars().all()

    async def get_multi(
        self,
        session: AsyncSession
    ):  # Sequence for Mypy
        """Get all objects."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: User | None = None,
    ):
        obj_in
        # print('BASE CRUD 1:', obj_in)
        # BASE CRUD 1: start_date=datetime.date(2024, 1, 21) end_date=datetime.date(2024, 1, 22) jet_id=14
        
        obj_in_data = obj_in.dict()
        # print('BASE CRUD 2:', obj_in_data)
        # BASE CRUD: {'start_date': datetime.date(2024, 1, 21), 'end_date': datetime.date(2024, 1, 22), 'jet_id': 13}
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Create object."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
