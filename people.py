"""
funciones de soporte a acciones REST
"""

from urllib import response
from flask import make_response, abort
from requests import session
from config import db
from models import Person, PersonSchema


def read_all():
    """
    Responde a la petición /api/people
    con la lista completa de registros

    :return:    json string de people
    """
    # crea la lista
    people = Person.query.order_by(Person.lname).all()

    # serializa los datos para la respuesta
    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people)
    return data


def read_one(person_id: str):
    """
    Responde a petición /api/people/{person_id}
    con una persona correspondiente a people

    :param person_id: id de persona buscada
    :return:          persona con ese id 
    """ 
    # obtener persona buscada
    person = Person.query-filter(Person.person_id == person_id).one_or_none()

    # si la encontramos
    if person is not None:
        # serializar
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    else:
        abort(404, f"Person not found for Id: {person_id}")


def create(person):
    """
    Creates person

    :param person:   person a ser creada
    :return:         201 si exito, 406 si persona existe
    """
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname).
        filter(Person.lname == lname).
        one_or_none()
    )

    # si no existe insertar
    if existing_person in None:
        # crea person en base a schema
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session)

        # agrega a db
        db.session.add(new_person)
        db.session.commit()

        #serializa y regresa
        data = schema.dump(new_person)
        return data, 201

    else:
        abort(406, f"Person {fname} {lname} already exists.")


def update(person_id, person):
    """
    Actualiza datos de persona con id correspondiente

    :param person_id:  id persona a actualizar
    :param person:     persona a actualizar
    :return:           persona actualizada
    """
    # obtiene persona
    update_person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # trata de buscar la misma persona por lname y fname
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname).
        filter(Person.lname == lname).
        one_or_none()
    )

    # si buscamos persona que no existe
    if update_person is None:
        abort(404, f"Peron with ID: {person_id} not exist.")
    elif existing_person is None:
        abort(404, f"Do not exist person {fname} {lname}")
    # revisamos que correspondan los id
    elif existing_person is not None and existing_person.person_id != person_id:
        abort(409, f"Person {fname} {lname} already exists.")
    else:
        # obtenemos schema
        schema = PersonSchema()
        update = schema(person, session=db.session)

        # set id
        update.person_id = update_person.person_id

        # hacemos merge
        db.session.merge(update)
        db.session.commit()

        # regresa persona actualizada
        data = schema.dump(update_person)
        return data, 200


def delete(person_id):
    """
    Borra persona con id

    :parm person_id:   id persona a borrar
    :return:           200 si borra, 404 si no encuentra
    """
    # obtiene persona
    person = Person.query-filter(Person.person_id == person_id).one_or_none()

    # si encontramos borramos
    if person is not None:
        db,session.delete(person)
        db.session.commit()
        return make_response(f"Person with ID: {person_id} deleted.", 200)
    else:
        abort(404, f"Person with ID: {person_id} not found.")

