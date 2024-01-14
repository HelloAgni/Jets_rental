from pydantic import BaseModel, ConfigDict, Field, validator


class JetBase(BaseModel):
    """Jet Base schema."""
    name: str
    jet_type: str
    description: str | None
    speed: int
    flight_range: int
    passenger_capacity: int
    price: int
    model_config = ConfigDict(extra='forbid')

    # Block params not from shema
    # old version
    # class Config:
    #     extra = Extra.forbid


class JetCreate(JetBase):
    """Jet Create schema."""
    name: str = Field(min_length=4, max_length=25)
    jet_type: str = Field(default='fast', max_length=25)
    speed: int = Field(default=10, ge=10)
    flight_range: int = Field(default=10, ge=10)
    passenger_capacity: int = Field(default=2, ge=2)
    price: int = Field(default=10, ge=10)

    @validator('name')
    def name_check(cls, value):
        if value == 'string':
            raise ValueError(f'Lets rename {value}')
        return value


class JetUpdate(JetCreate):
    """Jet Update schema."""
    pass


class JetDB(JetBase):
    """Jet Response schema."""
    id: int

    # ORM obj to Shema
    # class Config:
    #     orm_mode = True
