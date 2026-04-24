from fastapi import APIRouter, Body

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelGET
from src.database import async_session_maker
from repositories.hotels import HotelsRepository


router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('',
            summary='Get hotel list',)
async def get_hotels(
        pagination: PaginationDep,
        hotel_data: HotelGET,
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=hotel_data.location,
            title=hotel_data.title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )


@router.get('/{hotel_id}',)
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post('',
             summary='Create hotel',
             description='Adds hotel to hotels, '
                         'location and title required, '
                         'id generates'
)
async def create_hotel(hotel_data: Hotel = Body()):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(
            hotel_data
        )
        await session.commit()

    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}',
            summary='Edit hotel by id',
            description='Gets hotel by id and updates hotel title AND name,'
                        'both are required',)
async def edit_hotel(hotel_id: int,
                     hotel_data: Hotel
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            data=hotel_data,
            id=hotel_id,
        )
        await session.commit()

    return {'status': 'OK'}


@router.patch('/{hotel_id}',
              summary='Patch hotel by id',
              description='Gets hotel by id and updates hotel title or name', )
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            data=hotel_data,
            exclude_unset=True,
            id=hotel_id,
        )
        await session.commit()

    return {'status': 'OK'}


@router.delete('/{hotel_id}',
               summary='Delete hotel by id'
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(
            id=hotel_id
        )
        await session.commit()

    return {'status': 'OK'}
