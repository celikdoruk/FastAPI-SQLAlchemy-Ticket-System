from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict

class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Message(Base):
    message: str

# ---- REQUEST SCHEMAS ----- 
class CustomerAdd(Base):
    name: str = Field(min_length=2, max_length=512, description="Name of the customer.")
    age: int = Field(description="Age of customer.")

class CustomerUpdate(Base):
    name: str | None = Field(default=None, min_length=2, max_length=512, description="Name of customer.")
    age: int | None = Field(default=None, description="Age of customer.")

class ShowAdd(Base):
    title: str = Field(min_length=2, max_length=512, description="Title of the show.")
    age_limit: int = Field(description="Age limit for the show.")
    head_count: int = Field(description="Total available places for the show.")

class ShowUpdate(Base):
    title: str | None = Field(default=None, min_length=2, max_length=512, description="Title of the show.")
    age_limit: int | None = Field(default=None, description="Age limit for the show.")
    head_count: int | None = Field(default=None, description="Total available places for the show.")

class AvanueAdd(Base):
    name: str = Field(min_length=2, max_length=512, description="Name of the avanue.")
    availability: bool = Field(default=True, description="Availability of the avanue. True/False")

class AvanueUpdate(Base):
    name: str | None = Field(default=None, description="Name of the avanue.")
    availability: bool | None = Field(default=None, description="Availability of the avanue. True/False")


# ----- RESPONSE SCHEMAS -----
class CustomerReadList(Base):
    id: int
    name: str
    age: int

class ShowReadList(Base):
    id: int
    title: str
    age_limit: int
    head_count: int
    avanue_id: int | None = Field(default=None, description="Avanue id associated with the show.")

class AvanueReadList(Base):
    id: int
    name: str
    availability: bool

class Customer(Base):
    id: int
    name: str = Field(description="Name of customer.")
    age: int = Field(description="Age of customer.")
    show_list: list["Show"] = Field(default_factory=list, description="List of the shows customer attends to.")

class Show(Base):
    id: int = Field(description="A unique identifier of the show.")
    title: str = Field(description="Title of the show.")
    age_limit: int = Field(description="Age limit of the show.")
    head_count: int = Field(description="Places available on the show.")
    avanue_id: int | None = Field(default=None, description="Avanue id associated with the show.")
    customer_list: list["Customer"] = Field(default_factory=list, description="Customers enrolled at the show.")
    avanue: Avanue | None = Field(default=None, description="Avanue of the show.")

class Avanue(Base):
    id: int = Field(description="A unique identifier of the avanue.")
    name: str = Field(description="Name of the avanue.")
    availability: bool = Field(default=True, description="Availability of the avanue.")
    show_list: list["Show"] = Field(default_factory=list , description="Shows listed for the avanue.")

# for circular referance
Customer.model_rebuild()
Show.model_rebuild()
Avanue.model_rebuild()


