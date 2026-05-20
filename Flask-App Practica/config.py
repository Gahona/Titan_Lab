import os
class Config:
    # ─────────────────────────────────────────
    #  SEGURIDAD
    # ─────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gym_secret_key_2026')  # Cambia esto en producción

    # ─────────────────────────────────────────
    #  MYSQL
    # ─────────────────────────────────────────
    MYSQL_HOST        = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER        = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD    = os.environ.get('MYSQL_PASSWORD', 'Passw0rd')  # ← Contraseña de Workbench
    MYSQL_DB          = os.environ.get('MYSQL_DB', 'gym_project')
    MYSQL_CURSORCLASS = 'DictCursor'  # Las consultas devuelven dicts en vez de tuplas


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Configuración activa (cambia a ProductionConfig al desplegar)
config_activa = DevelopmentConfig