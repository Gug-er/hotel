import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi'},
    {'id': 2, 'title': 'Dubaisk'},
]

@app.get("/hotels")
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


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

