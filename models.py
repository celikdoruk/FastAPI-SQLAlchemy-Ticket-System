from sqlalchemy import Integer, String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass 

# association table
customer_show = Table(
    "customer_show",
    Base.metadata,
    Column("customer_id", ForeignKey("customers.id"), primary_key=True, index=True),
    Column("show_id", ForeignKey("shows.id"), primary_key=True, index=True)
)


class CustomerORM(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    show_list: Mapped[list["ShowORM"]] = relationship(secondary=customer_show,back_populates="customer_list")

class ShowORM(Base):
    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    age_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    head_count: Mapped[int] = mapped_column(Integer, nullable=False)
    avanue_id: Mapped[int | None] = mapped_column(ForeignKey("avanues.id", ondelete="SET NULL"), index=True, nullable=True)

    customer_list: Mapped[list["CustomerORM"]] = relationship(secondary=customer_show,back_populates="show_list")
    avanue: Mapped["AvanueORM | None"] = relationship(back_populates="show_list")


class AvanueORM(Base):
    __tablename__ = "avanues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    availability:  Mapped[bool] = mapped_column(Boolean, nullable=False)

    show_list: Mapped[list["ShowORM"]] = relationship(back_populates="avanue", passive_deletes=True)

