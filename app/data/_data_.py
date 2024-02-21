import csv
import pathlib
import re
import time

import pandas as pd
from fastapi import APIRouter, Depends, Query, UploadFile
from sqlalchemy import create_engine, delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session, settings
from app.models import Jet, Rental, User
from app.schemas.rental import RentalLoad

router = APIRouter()

MODELS = {'Jet': Jet, 'Rental': Rental, 'User': User}
CURRENT_DIR = pathlib.Path(__file__).parent
CSV = {'Jet': 'jets.csv', 'Rental': 'rental.csv'}


@router.get(
    '/check-data'
)
async def check_data(
    session: AsyncSession = Depends(get_async_session),
    model: str = Query(
        description='Select any model: Jet, Rental',
        default='Jet'),
    start_from: int = Query(ge=0, default=0),
    page_size: int = Query(ge=1, le=20, default=5)
):
    """
    <b>Check data, pagination available.</b>\n
    Select any model/table \n
    start_from - start from row\n
    page_size - number of response rows
    """
    try:
        all_data = await session.execute(
            select(MODELS[model])
        )
    except Exception as e:
        print(e)
        return {'Smth going wrong': str(e)}
    result = all_data.scalars().all()[start_from: page_size]
    return result


@router.post(
    '/insert-data-jet-rental',
)
async def insert_data_jet_rental(
    session: AsyncSession = Depends(get_async_session),
):
    """
    <b>Insert data Jet and Rental from csv files.</b>\n
    pandas read csv + session insert.\n
    """
    start = time.time()
    # current_dir_rental = pathlib.Path(__file__).parent / 'rental.csv'
    # data_to_insert_rental: list[dict] = pd.read_csv(
    #     current_dir_rental).to_dict(orient='records')
    # print(data_to_insert_rental)
    # [{'id': 1, 'start_date': '2027-01-11', 'end_date': '2027-01-14'}, {...}]

    data: dict = {
        key: pd.read_csv(CURRENT_DIR / CSV[key]).to_dict(orient='records')
        for key in CSV
            }
    # print(data)
    # {'Jet': [{'id': 1, 'name': 'Star',...
    await session.execute(
        insert(Jet),
        data['Jet'],  # type: ignore
    )
    await session.commit()

    await session.execute(
        insert(Rental),
        [RentalLoad(**row).model_dump() for row in data['Rental']]
    )
    await session.commit()
    end = time.time()
    return {
        'Result': 'Successful!',
        'Time-v2': round(end - start, 5)}


@router.post(
    '/insert-data-jet-v1',
)
async def insert_data_jet_v1(
    session: AsyncSession = Depends(get_async_session),
    *,
    # csv_file_name: str = 'jets_csv'
    file: UploadFile,
):
    """
    Open file and insert data Jet.\n
    pandas read csv + session insert.\n
    """
    start = time.time()
    # current_dir = pathlib.Path(__file__).parent / (csv_file_name + '.csv')
    # data_to_insert = pd.read_csv(current_dir).to_dict(orient='records')

    data_to_insert = pd.read_csv(file.file).to_dict(orient='records')

    await session.execute(
        insert(Jet),
        data_to_insert  # type: ignore
    )
    await session.commit()
    end = time.time()
    print(end - start)
    return {
        'Result': 'Successful!',
        'Time-v2': round(end - start, 5)}


@router.post(
    '/insert-data-rental-v1',
    # deprecated=True
)
async def insert_data_rental_v1(
    session: AsyncSession = Depends(get_async_session),
    *,
    file: UploadFile,

    # csv_file_name: str = 'jets_csv'
):
    """
    Open file and insert data Rental.\n\n
    pandas read csv + session insert.\n
    """
    start = time.time()
    # current_dir = pathlib.Path(__file__).parent / (csv_file_name + '.csv')
    # data_to_insert = pd.read_csv(current_dir).to_dict(orient='records')

    data_to_insert: list[dict] = pd.read_csv(
        file.file).to_dict(orient='records')

    # '2027-01-11' ('str' object has no attribute 'toordinal')
    # Custom fix for insert to PostgreSQL DATE column
    # convert str(date) from csv file to datetime.date()
    # 2024-02-15 => datetime.date(2024, 2, 15)
    await session.execute(
        insert(Rental),
        [RentalLoad(**row).model_dump() for row in data_to_insert]
    )

    await session.commit()

    end = time.time()
    print(end - start)
    return {
        'Result': 'Successful!',
        'Time-v2': round(end - start, 5)}


@router.post(
    '/insert-data-v2',
    deprecated=True
)
async def insert_data_v2(
    session: AsyncSession = Depends(get_async_session),
    csv_file_name: str = 'jets_csv'
):
    """
    Insert data Jet.\n\n
    With open + session insert.\n
    """
    start = time.time()
    current_dir = pathlib.Path(__file__).parent / (csv_file_name + '.csv')
    try:
        with open(current_dir, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data_to_insert = [x for x in csv_reader]
            await session.execute(
                insert(Jet),
                data_to_insert
            )
            await session.commit()
    except Exception as e:
        print(e)
    end = time.time()
    print(end - start)
    return {'Time-v2': end - start}


@router.post(
    '/insert-data-v3',
    deprecated=True,
)
def insert_data_v3():
    """
    Insert with engine connect, pandas read_csv + to_sql.\n
    """
    start = time.time()
    # current_dir = pathlib.Path(__file__).parent / 'jets_1.csv'
    current_dir = pathlib.Path(__file__).parent / 'new_jet.csv'
    cut_db_url = re.sub('[+].*[:]', ':', settings.database_url)
    # print(cut_db_url)
    # sqlite:///./fastapijetz.db

    try:
        engine = create_engine(cut_db_url)
        with engine.connect() as conn:
            df = pd.read_csv(current_dir)
            df.to_sql('jet', conn, index=False, if_exists='append')
    except Exception as e:
        print(f'We got some Error: {e}')
    end = time.time()
    print(end - start)
    return {'Time': end - start}


@router.post(
    '/create-csv',
    deprecated=True
)
def create_csv(
    rows: int = 10,
    csv_file_name: str = 'jets_csv'
):
    """
    Create Jets csv file for Testing.\n
    Select rows count.
    """
    start = time.time()
    current_dir = pathlib.Path(__file__).parent / (csv_file_name + '.csv')
    data = [
        (i, 'name' + str(i), 'type' + str(i),
         'descp' + str(i), 100 + i, 1000 + i,
         17, 2000 + i) for i in range(1, rows)
    ]
    df = pd.DataFrame(data, columns=[
        'id', 'name', 'jet_type', 'description',
        'speed', 'flight_range', 'passenger_capacity', 'price'])
    df.to_csv(current_dir, sep=',', index=False)
    end = time.time()
    print(end - start)
    return {'CSV created, number of rows: ': rows}


@router.delete(
    '/delete-my-data'
)
async def delete_jets_and_rental(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete all rows from Rental table.\n
    Delete all rows from Jet table.
    """
    count_jets = select(func.count()).select_from(Jet)
    count_rentals = select(func.count()).select_from(Rental)
    jets = await session.execute(count_jets)
    rentals = await session.execute(count_rentals)

    delete_rentals = delete(Rental)
    delete_jets = delete(Jet)

    await session.execute(delete_rentals)
    await session.execute(delete_jets)
    await session.commit()
    return {'Deleted:': [
            {Jet.__tablename__: jets.scalar()},
            {Rental.__tablename__: rentals.scalar()}]
            }
