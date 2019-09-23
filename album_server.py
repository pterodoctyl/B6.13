from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
import re

import bd

# Выводим список альбомов по заданному artist. Пример: http://localhost:8080/albums/Queen
@route("/albums/<artist>")
def albums(artist):
    albums_list = bd.find(artist)
    if not albums_list:
        message = f"Альбомов {artist} не найдено"
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = f"Найдено {len(album_names)} альбомов {artist}:<br><br>"
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def new_record():
    # создаем словарь из POST-запроса
    album_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"), 
        "year": int(request.forms.get("year")),
        "album": request.forms.get("album"),
    }
    print(album_data)
    # блок валидации запросов пользователя
    for record in album_data:
        if not album_data[record]:
            return f"Некорректные данные. Отсутствует поле '{record}'"
    
    # проверка rода
    match = re.match(r"[1-2][0-9]{3}", str(album_data["year"]))
    if not match:
        return f"Некорректные данные. Неправильно указан год"
    
    new_album = bd.Album(**album_data)  # создаем экземпляр класса из словаря

    # сохраняем новый альбом
    if bd.save(new_album):
        result = f"Альбом {album_data['album']} исполнителя {album_data['artist']} успешно сохранен"
    else:
        message = f"Альбом {album_data['album']} уже есть в базе"
        result = HTTPError(409, message)
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, server='tornado', debug=True)