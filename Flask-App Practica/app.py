from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import config_activa


app = Flask(__name__)
app.config.from_object(config_activa)

mysql = MySQL(app)


# ─────────────────────────────────────────
#  DECORADORES DE AUTENTICACIÓN Y ROLES
# ─────────────────────────────────────────
def login_required(f):
    """Redirige al login si el usuario no ha iniciado sesión."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'id_usuario' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def rol_required(*roles):
    def decorator(f):
        @wraps(f)          
        def decorated(*args, **kwargs):
            if 'rol' not in session or session['rol'] not in roles:
                flash('No tienes permiso para acceder a esta sección.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─────────────────────────────────────────
#  DATOS ESTÁTICOS (página principal)
# ─────────────────────────────────────────
stats = [
    {"valor": "+3,000", "label": "Miembros activos"},
    {"valor": "180+",   "label": "Ejercicios"},
    {"valor": "99%",    "label": "Satisfacción"},
]

suplementos = [
    {
        "nombre": "Proteína",
        "imagen": "proteina.jpg",
        "alt": "Proteína whey",
        "descripcion": "Aumenta tu recuperación muscular y acelera tus resultados con proteína de alta calidad. Ideal para ganar masa muscular, mantener tus músculos y recuperarte después de entrenamientos intensos."
    },
    {
        "nombre": "Creatina",
        "imagen": "creatina.jpg",
        "alt": "Creatina",
        "descripcion": "Mejora tu fuerza, potencia y rendimiento en cada entrenamiento. La creatina es uno de los suplementos más eficaces para aumentar masa muscular y superar tus límites físicos."
    },
    {
        "nombre": "Pre-entreno",
        "imagen": "prewornk.jpg",
        "alt": "Pre-entreno",
        "descripcion": "Activa tu energía y concentración antes de entrenar. Consigue más intensidad, motivación y resistencia para rendir al máximo en cada sesión."
    },
    {
        "nombre": "BCAAs / EAAs",
        "imagen": "intrawork.jpg",
        "alt": "BCAAs / EAAs",
        "descripcion": "Protege tu masa muscular y mejora la recuperación durante y después del entrenamiento. Perfectos para reducir la fatiga y mantener el rendimiento incluso en rutinas exigentes."
    },
    {
        "nombre": "Omega 3",
        "imagen": "omega3.jpg",
        "alt": "Omega 3",
        "descripcion": "Cuida tu corazón, articulaciones y bienestar general con ácidos grasos esenciales. Un suplemento clave para mejorar la salud y favorecer una recuperación más eficiente."
    },
    {
        "nombre": "Zinc / Magnesio",
        "imagen": "zmzinc.jpg",
        "alt": "Zinc y Magnesio",
        "descripcion": "Mejora tu descanso, recuperación muscular y niveles de energía. Una combinación perfecta para optimizar el rendimiento físico y apoyar tu sistema inmunológico."
    },
]

colaboradores = [
    {"imagen": "iogenix.logo-removebg-preview.jpg", "alt": "Io.Genix"},
    {"imagen": "logopaypal-removebg-preview.jpg",   "alt": "PayPal"},
    {"imagen": "pannattaaa-removebg-preview.jpg",   "alt": "Panatta"},
]


# ─────────────────────────────────────────
#  AUTENTICACIÓN
# ─────────────────────────────────────────
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre   = request.form['nombre']
        email    = request.form['email']
        password = generate_password_hash(request.form['password'])
        rol      = 'cliente'  # Siempre cliente al registrarse; el admin asigna otros roles

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (%s, %s, %s, %s)",
                (nombre, email, password, rol)
            )
            mysql.connection.commit()
            cur.close()
            flash('Cuenta creada correctamente. ¡Inicia sesión!', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('El email ya está registrado o ha ocurrido un error.', 'error')

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'id_usuario' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id_usuario, nombre, password_hash, rol FROM usuarios WHERE email = %s",
            (email,)
        )
        usuario = cur.fetchone()
        cur.close()

        if usuario and check_password_hash(usuario['password_hash'], password):
            session['id_usuario'] = usuario['id_usuario']
            session['nombre']     = usuario['nombre']
            session['rol']        = usuario['rol']

            flash(f"Bienvenido, {usuario['nombre']}!", 'success')

            if session['rol'] == 'admin':
                return redirect(url_for('panel_admin'))
            elif session['rol'] == 'coach':
                return redirect(url_for('panel_coach'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))


# ─────────────────────────────────────────
#  PANELES POR ROL
# ─────────────────────────────────────────
@app.route('/admin/panel')
@login_required
@rol_required('admin')
def panel_admin():
    """Panel exclusivo para administradores."""
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id_usuario, nombre, email, rol, fecha_registro FROM usuarios ORDER BY fecha_registro DESC"
    )
    usuarios = cur.fetchall()
    cur.close()
    return render_template('admin/panel.html', usuarios=usuarios)


@app.route('/admin/usuario/<int:id>/cambiar_rol', methods=['POST'])
@login_required
@rol_required('admin')
def cambiar_rol(id):
    """El admin puede cambiar el rol de cualquier usuario."""
    nuevo_rol = request.form.get('rol')
    if nuevo_rol not in ('admin', 'cliente', 'coach'):
        flash('Rol no válido.', 'error')
        return redirect(url_for('panel_admin'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET rol = %s WHERE id_usuario = %s", (nuevo_rol, id))
    mysql.connection.commit()
    cur.close()
    flash('Rol actualizado correctamente.', 'success')
    return redirect(url_for('panel_admin'))


@app.route('/coach/panel')
@login_required
@rol_required('coach', 'admin')
def panel_coach():
    """Panel para coaches (y admins)."""
    return render_template('coach/panel.html')


# ─────────────────────────────────────────
#  RUTAS PÚBLICAS
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template(
        "main.html",
        stats=stats,
        suplementos=suplementos,
        colaboradores=colaboradores
    )


@app.route("/planes")
def planes():
    return render_template("Plan5.html")


@app.route("/plan5")
def plan5():
    return render_template("Plan5.html")


@app.route("/dieta")
def dieta():
    return render_template("macros.html")


PLANES = {
    "basico":  {"nombre": "Coach Básico",  "precio": "11,99€"},
    "premium": {"nombre": "Coach Premium", "precio": "22,99€"},
}


@app.route('/pago_sub/<plan_id>')
def pago_sub(plan_id):
    plan = PLANES.get(plan_id)
    if not plan:
        return redirect(url_for('planes'))
    return render_template('pago_sub.html',
        plan_nombre=plan["nombre"],
        precio=plan["precio"])


@app.route('/pago-exitoso')
def pago_exitoso():
    return render_template('pago_exitoso.html')


# ─────────────────────────────────────────
#  RUTINAS (requiere login)
# ─────────────────────────────────────────
@app.route('/rutina')
def rutina():
    catalogo = {
        "Pecho":   ["Press banca", "Press inclinado", "Aperturas", "Fondos"],
        "Espalda": ["Dominadas", "Remo con barra", "Jalón al pecho", "Remo en polea"],
        "Hombro":  ["Press militar", "Elevaciones laterales", "Pájaros"],
        "Pierna":  ["Sentadilla", "Prensa", "Extensiones", "Curl femoral", "Gemelos"],
        "Bíceps":  ["Curl con barra", "Curl alterno", "Curl martillo"],
        "Tríceps": ["Fondos en polea", "Press francés", "Extensión overhead"],
    }

    semanal = {
        "Lunes": [], "Martes": [], "Miércoles": [],
        "Jueves": [], "Viernes": [], "Sábado": [], "Domingo": []
    }

    return render_template('semanal.html', catalogo=catalogo, semanal=semanal)


@app.route('/guardar_rutina', methods=['POST'])
@login_required
def guardar_rutina():
    data = request.get_json()
    # Aquí puedes insertar en la tabla `rutinas` de MySQL si quieres persistencia real
    return {'ok': True}, 200


if __name__ == "__main__":
    app.run(debug=True)