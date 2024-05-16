from app.infrastructure.database import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]