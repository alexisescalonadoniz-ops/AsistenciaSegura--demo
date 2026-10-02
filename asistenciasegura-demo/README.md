# AsistenciaSegura — DEMO

Aplicación Flask mínima para practicar el **despliegue con Gunicorn** (Submódulo 2).
Tiene inicio de sesión, lista de alumnos (consulta a la BD) y alta de alumnos (inserción),
conectada a MySQL en **Aiven** con SSL.

Las tablas usan el prefijo `demo_` (`demo_usuario`, `demo_alumno`) para no mezclarse
con las tablas reales del proyecto que ya estén en Aiven.

## Estructura

```
asistenciasegura-demo/
├── app.py                 # Aplicación Flask (rutas y modelos)
├── config.py              # Lee las credenciales del .env / variables de entorno
├── init_db.py             # Crea las tablas y carga datos de ejemplo (se corre 1 vez)
├── requirements.txt       # Librerías del proyecto
├── .env.example           # Plantilla de variables (sin valores reales)
├── .gitignore             # Evita subir .env y el certificado
├── static/estilos.css
└── templates/
    ├── base.html
    ├── login.html
    └── alumnos/lista.html
```

## 1. Preparar en la laptop (Windows)

Abrir una terminal dentro de la carpeta del proyecto:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configurar la conexión a Aiven

1. Copiar `.env.example` y renombrar la copia a `.env`.
2. Llenarlo con los datos de Aiven (Overview → Connection information).
3. Copiar el certificado `aiven-ca.pem` a esta misma carpeta (junto a `app.py`).
4. Generar una SECRET_KEY y pegarla en el `.env`:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

## 3. Crear las tablas y los datos de ejemplo (solo una vez)

```
python init_db.py
```

Crea el usuario **docente** con contraseña **Cecytem2026** y 5 alumnos de ejemplo.

## 4. Probar en local

```
python app.py
```

Abrir http://127.0.0.1:5000, iniciar sesión y registrar un alumno.
El pie de página muestra a qué servidor de base de datos está conectada la app.
La ruta http://127.0.0.1:5000/salud confirma si la conexión a la BD funciona.

## 5. Subir a GitHub

Crear un repositorio vacío en GitHub (sin README) y luego:

```
git init
git add .
git commit -m "Proyecto demo AsistenciaSegura"
git branch -M main
git remote add origin https://github.com/USUARIO/asistenciasegura-demo.git
git push -u origin main
```

Revisar en GitHub que **no** aparezcan `.env` ni `aiven-ca.pem`.

## 6. Desplegar

A partir de aquí se sigue el **Manual de despliegue con Gunicorn** desde el Paso 1
(instalar Gunicorn, `pip freeze`, crear `gunicorn.conf.py` y `.python-version`, Render).
