from dotenv import load_dotenv
import os

# Lee el archivo .env si existe (en la laptop).
# En Render no hay .env: los valores vienen de las variables de entorno del panel.
load_dotenv()


class Config:
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_SSL_CA = os.environ.get('DB_SSL_CA')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # Aiven exige SSL: se pasa el certificado como opción de conexión.
    # pool_pre_ping revisa que la conexión siga viva antes de usarla
    # (útil porque Aiven y Render "duermen" por inactividad).
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'ssl': {'ca': DB_SSL_CA}},
        'pool_pre_ping': True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
