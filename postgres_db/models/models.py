from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


class Samples(Base):
    __tablename__ = "samples"
    id: Mapped[int] = mapped_column(primary_key=True)
    sample_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    sample_group: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(Integer(), nullable=False)
    sex: Mapped[str] = mapped_column(String(10), nullable=False)
    tissue: Mapped[str] = mapped_column(String(10), nullable=False)
    epigenetic_age: Mapped[float] = mapped_column(Float(), nullable=False)
