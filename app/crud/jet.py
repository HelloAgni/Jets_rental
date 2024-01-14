from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.jet import Jet


class CRUDJet(CRUDBase):

    async def get_jet_id_by_name(
            self,
            jet_name: str,
            session: AsyncSession
    ) -> int | None:
        """Get jet obj id by name."""
        jet_id = await session.execute(
            select(Jet.id).where(
                Jet.name == jet_name
            )
        )
        return jet_id.scalars().first()


jet_crud = CRUDJet(Jet)
