from datetime import date, timedelta

from pydantic import BaseModel, ConfigDict, Field, root_validator, validator

START_DATE = date.today() + timedelta(days=1)
END_DATE = date.today() + timedelta(days=2)


class RentalBase(BaseModel):
    """
    Rental Base schema.
    """
    start_date: date = Field(example=START_DATE)
    end_date: date = Field(example=END_DATE)
    model_config = ConfigDict(extra='forbid')

    #  Block params not from shema
    # old version
    # class Config:
    #     extra = Extra.forbid


class RentalUpdate(RentalBase):
    """
    Rental Update schema.
    """

    @validator('start_date')
    def check_start_date(cls, value):
        # print('Rental Schema1', value)
        #  2024-01-15
        if value <= date.today():
            raise ValueError(f'You cant rent from {value}\n'
                             f'Today is {date.today()}')
        return value

    # Validate two params
    @root_validator(skip_on_failure=True)
    def check_start_end_date(cls, values):
        # print('Rental Shema3', values)
        # Rental Shema3 {'start_date': datetime.date(2023, 6, 26),
        # 'end_date': datetime.date(2023, 6, 28), 'jet_id': 2}
        if values['start_date'] >= values['end_date']:
            raise ValueError(
                f'Start date: {values["start_date"]}\n'
                f'cant be greater than or equal to end date: '
                f'{values["end_date"]}'
            )
        return values


class RentalCreate(RentalUpdate):
    """
    Rental Create schema.
    """
    jet_id: int


class RentalDB(RentalBase):
    """
    Rental Response schema.
    """
    id: int
    jet_id: int
    user_id: int | None
    duration: int  # Rental model @hybrid_property

    # By default only dict and json can serialize.
    # ORM obj to Shema
    # class Config:
    # orm_mode = True  # old version
    # from_attributes = True
