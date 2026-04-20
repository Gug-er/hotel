from fastapi import APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelGET
from src.database import async_session_maker

from src.models.hotels import HotelsOrm


router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('',
            summary='Get hotel list',)
async def get_hotels(
        pagination: PaginationDep,
        hotel_data: HotelGET,
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)

        if hotel_data.location:
            query = query.filter(func.lower(HotelsOrm.location).contains(hotel_data.location.strip().lower()))
        if hotel_data.title:
            query = query.filter(func.lower(HotelsOrm.title).contains(hotel_data.title.strip().lower()))

        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


@router.post('',
             summary='Create hotel',
             description='Adds hotel to hotels, title and name required, id generates')
async def create_hotel(hotel_data: Hotel = Body()):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'status': 'OK'}


@router.put('/{hotel_id}',
            summary='Edit hotel by id',
            description='Gets hotel by id and updates hotel title and name',)
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
            return {'status': 'OK'}
    return {'status': 'Hotel not found'}


@router.patch('/{hotel_id}',
              summary='Patch hotel by id',
              description='Gets hotel by id and updates hotel title or name', )
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title

            if hotel_data.name:
                hotel['name'] = hotel_data.name

            return {'status': 'OK'}
    return {'status': 'Hotel not found'}


@router.delete('/{hotel_id}',
               summary='Delete hotel by id',
               description='Rewrites hotels without deleted one', )
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

