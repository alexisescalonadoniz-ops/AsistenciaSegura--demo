# gunicorn.conf.py — Configuración de Gunicorn para producción
import os
 
# 1. Dirección y puerto donde escucha la aplicación.
#    0.0.0.0 = acepta conexiones de fuera del servidor.
#    El puerto lo define el hosting en la variable PORT.
#    (Render usa el 10000).
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
 
# 2. Procesos (workers) que atienden peticiones al mismo tiempo.
#    En el plan gratuito de Render (poca memoria), 2 es suficiente.
workers = 2
 
# 3. Segundos máximos por petición antes de reiniciar al worker.
timeout = 60
 
# 4. Bitácoras: '-' significa "escribir en la consola",
#    que es lo que muestra la pestaña Logs de Render.
accesslog = '-'
errorlog = '-'
loglevel = 'info'