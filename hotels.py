import uvicorn
from fastapi import Query, Body, APIRouter


router = APIRouter(prefix='/hotels', tags=['Hotels'])

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
]

@router.get('',
            summary='Get hotel list',)
def get_hotels(
        id: int | None = Query(None, description='Hotel ID'),
        title: str | None = Query(None, description='Hotel title'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post('',
             summary='Create hotel',
             description='Adds hotel to hotels, title and name required, id generates')
def create_hotel(
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title,
        'name': name
    })
    return {'status': 'OK'}


@router.put('/{hotel_id}',
            summary='Edit hotel by id',
            description='Gets hotel by id and updates hotel title and name',)
def edit_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
            return {'status': 'OK'}
    return {'status': 'Hotel not found'}


@router.patch('/{hotel_id}',
              summary='Patch hotel by id',
              description='Gets hotel by id and updates hotel title or name', )
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(default=None),
        name: str | None = Body(default=None),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if title:
                hotel['title'] = title

            if name:
                hotel['name'] = name

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
