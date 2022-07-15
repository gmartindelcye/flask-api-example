import os
from config import db
from models import Person

# Datos a inicializar
PEOPLE = [
    {"fname": "Juan", "lname": "Pérez"},
    {"fname": "Ana", "lname": "Villa"},
    {"fname": "Susana", "lname": "Paredes"},
]

# borrar archivo de base de datos si existe
if os.path.exists("gente.db"):
    os.remove("gente.db")

# crear la bd
db.create_all()

# iterar PEOPLE para cargar la bd
for person in PEOPLE:
    p = Person(lname=person.get("lname"), fname=person.get("fname"))
    print(p)
    db.session.add(p)

db.session.commit()