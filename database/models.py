from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime

from datetime import datetime

class Base(DeclarativeBase):
    ...


class Remind(Base):
    __tablename__ = "remind"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int]
    text: Mapped[str]
    time: Mapped[int]
    end_time: Mapped[str]
    end_date: Mapped[datetime] = mapped_column(DateTime)
