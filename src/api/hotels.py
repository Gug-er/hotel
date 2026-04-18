import uvicorn
from fastapi import APIRouter

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelGET


router = APIRouter(prefix='/hotels', tags=['Hotels'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get('',
            summary='Get hotel list',)
def get_hotels(
        pagination: PaginationDep,
        hotel_data: HotelGET,
):
    hotels_ = []
    for hotel in hotels:
        if hotel_data.id and (hotel['id'] != hotel_data.id):
            continue
        if hotel_data.title and (hotel['title'] != hotel_data.title):
            continue
        hotels_.append(hotel)

    return hotels_[(pagination.page + 1)
                   * pagination.per_page:pagination.per_page]


@router.post('',
             summary='Create hotel',
             description='Adds hotel to hotels, title and name required, id generates')
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
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


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
