"""
Crea las tablas de la demo en la base de datos (Aiven) y carga datos de ejemplo.
Se ejecuta UNA sola vez, desde la laptop:   python init_db.py
"""
from werkzeug.security import generate_password_hash

from app import app, db, Usuario, Alumno

USUARIO = 'docente'
PASSWORD = 'Cecytem2026'   # Cámbiala si quieres; es solo para la demostración

ALUMNOS = [
    ('2026001', 'Ana Sofía Martínez López', '501', '04A1B2C3'),
    ('2026002', 'Luis Fernando García Ruiz', '501', '04D4E5F6'),
    ('2026003', 'María José Hernández Cruz', '502', '04112233'),
    ('2026004', 'Jorge Iván Sánchez Pérez', '502', None),
    ('2026005', 'Valeria Ramírez Flores', '503', '04AABBCC'),
]

with app.app_context():
    db.create_all()
    print('Tablas demo_usuario y demo_alumno listas.')

    if not Usuario.query.filter_by(usuario=USUARIO).first():
        db.session.add(Usuario(usuario=USUARIO, nombre='Docente de prueba',
                               password_hash=generate_password_hash(PASSWORD)))
        print(f'Usuario creado -> usuario: {USUARIO}   contraseña: {PASSWORD}')
    else:
        print(f'El usuario {USUARIO} ya existía.')

    nuevos = 0
    for matricula, nombre, grupo, uid in ALUMNOS:
        if not Alumno.query.filter_by(matricula=matricula).first():
            db.session.add(Alumno(matricula=matricula, nombre=nombre, grupo=grupo, uid_credencial=uid))
            nuevos += 1
    db.session.commit()
    print(f'Alumnos de ejemplo agregados: {nuevos}')
