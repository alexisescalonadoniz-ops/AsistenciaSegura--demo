"""
AsistenciaSegura - DEMO
Aplicación Flask mínima para practicar el despliegue con Gunicorn.
Tiene inicio de sesión, lista de alumnos (consulta) y alta de alumnos (inserción).
"""
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# ------------------------------------------------------------------
# Modelos (tablas con prefijo demo_ para no chocar con las tablas
# reales del proyecto que ya se importaron en Aiven)
# ------------------------------------------------------------------
class Usuario(db.Model):
    __tablename__ = 'demo_usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class Alumno(db.Model):
    __tablename__ = 'demo_alumno'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)
    uid_credencial = db.Column(db.String(30))  # UID de la tarjeta RFID/NFC


# ------------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------------
def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Inicia sesión para continuar.', 'aviso')
            return redirect(url_for('login'))
        return vista(*args, **kwargs)
    return envoltura


@app.context_processor
def datos_globales():
    # Se muestra en el pie de página para comprobar a qué servidor está conectada la app
    return {'servidor_bd': app.config.get('DB_HOST') or 'sin configurar'}


# ------------------------------------------------------------------
# Rutas
# ------------------------------------------------------------------
@app.route('/')
def inicio():
    return redirect(url_for('alumnos'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '')
        u = Usuario.query.filter_by(usuario=usuario).first()
        if u and check_password_hash(u.password_hash, password):
            session.clear()
            session['usuario_id'] = u.id
            session['nombre'] = u.nombre
            return redirect(url_for('alumnos'))
        flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/alumnos', methods=['GET', 'POST'])
@login_requerido
def alumnos():
    if request.method == 'POST':
        matricula = request.form.get('matricula', '').strip()
        nombre = request.form.get('nombre', '').strip()
        grupo = request.form.get('grupo', '').strip().upper()
        uid = request.form.get('uid_credencial', '').strip() or None
        if not (matricula and nombre and grupo):
            flash('Matrícula, nombre y grupo son obligatorios.', 'error')
        elif Alumno.query.filter_by(matricula=matricula).first():
            flash(f'La matrícula {matricula} ya está registrada.', 'error')
        else:
            db.session.add(Alumno(matricula=matricula, nombre=nombre, grupo=grupo, uid_credencial=uid))
            db.session.commit()
            flash(f'Alumno {nombre} registrado correctamente.', 'ok')
        return redirect(url_for('alumnos'))

    lista = Alumno.query.order_by(Alumno.grupo, Alumno.nombre).all()
    return render_template('alumnos/lista.html', alumnos=lista)


@app.route('/salud')
def salud():
    """Revisión rápida: ¿la app responde y se conecta a la base de datos?"""
    try:
        version = db.session.execute(text('SELECT VERSION()')).scalar()
        return {'app': 'ok', 'base_de_datos': 'ok', 'mysql': version}
    except Exception as e:  # noqa: BLE001
        return {'app': 'ok', 'base_de_datos': 'error', 'detalle': str(e)}, 500


# Solo para trabajar en la laptop (servidor de desarrollo).
# En producción Gunicorn importa "app" y este bloque NO se ejecuta.
if __name__ == '__main__':
    app.run(debug=True)
