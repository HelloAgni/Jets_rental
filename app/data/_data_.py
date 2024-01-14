import csv
import pathlib
import re
import time

import pandas as pd
from fastapi import APIRouter, Depends, Query, UploadFile
from sqlalchemy import create_engine, delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session, settings
from app.models import Jet

router = APIRouter()


@router.get(
    '/check-data'
)
async def check_data(
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=20)
):
    """
    <b>Check data, pagination available.</b>\n
    skip - start from row\n
    size - number of response rows
    """
    all_data = await session.execute(
        select(Jet)
    )
    result = all_data.scalars().all()[skip: size]
    return result


@router.post(
    '/insert-data-v1',
)
async def insert_data_v1(
    session: AsyncSession = Depends(get_async_session),
    *,
    # csv_file_name: str = 'jets_csv'
    file: UploadFile,
):
    """
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
    return {'Time-v2': end - start}


@router.post(
    '/insert-data-v2'
)
async def insert_data_v2(
    session: AsyncSession = Depends(get_async_session),
    csv_file_name: str = 'jets_csv'
):
    """
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
    '/insert-data-v3'
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
    '/create-csv'
)
def create_csv(
    rows: int = 10,
    csv_file_name: str = 'jets_csv'
):
    """
    Create csv file for testing.\n
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
    return {'csv created with rows:': rows}


@router.delete(
    '/delete-my-data'
)
async def delete_jets(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete all rows from Jet table.
    """
    count_jets = select(func.count()).select_from(Jet)
    z = await session.execute(count_jets)
    # print(z.scalar())
    # 8999

    # sss = delete(Jet).where(Jet.id == 1)
    # sss = delete(Jet).where(Jet.id.in_([11, 12, 13]))
    delete_jets = delete(Jet)
    await session.execute(delete_jets)
    await session.commit()
    return {'Deleted:': z.scalar()}
