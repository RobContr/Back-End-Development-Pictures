from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((picture for picture in data if picture['id'] == id), None)
    if picture:
        return jsonify(picture)
    else:
        abort(404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Estrai i dati dell'immagine dalla richiesta
    picture_data = request.json

    # Verifica se un'immagine con lo stesso ID esiste già
    for picture in data:
        if picture['id'] == picture_data['id']:
            return jsonify({"Message": f"picture with id {picture_data['id']} already present"}), 302

    # Aggiungi l'immagine alla lista di dati
    data.append(picture_data)

    return jsonify({"Message": "Picture added successfully"}), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Estrai i dati dell'immagine dalla richiesta
    updated_picture_data = request.json

    # Trova l'immagine corrispondente all'ID nella lista dei dati
    picture = next((picture for picture in data if picture['id'] == id), None)
    if picture:
        # Aggiorna i dati dell'immagine con i nuovi dati
        picture.update(updated_picture_data)
        return jsonify({"message": f"Picture with id {id} updated successfully"}), 200
    else:
        # Se l'immagine non esiste, restituisci un errore 404
        abort(404, {"message": "Picture not found"})

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Trova l'immagine corrispondente all'ID nella lista dei dati
    picture = next((picture for picture in data if picture['id'] == id), None)
    if picture:
        # Rimuovi l'immagine dalla lista dei dati
        data.remove(picture)
        return '', 204
    else:
        # Se l'immagine non esiste, restituisci un errore 404
        abort(404, {"message": "Picture not found"})
