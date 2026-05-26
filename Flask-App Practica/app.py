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
    {"valor": "180+", "label": "Ejercicios"},
    {"valor": "99%", "label": "Satisfacción"},
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
    {"imagen": "logopaypal-removebg-preview.jpg", "alt": "PayPal"},
    {"imagen": "pannattaaa-removebg-preview.jpg", "alt": "Panatta"},
]

# ─────────────────────────────────────────
#  AUTENTICACIÓN
# ─────────────────────────────────────────
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        rol = 'cliente'

        edad = request.form.get('edad') or None
        sexo = request.form.get('sexo') or None
        altura = request.form.get('altura_cm') or None
        peso = request.form.get('peso_kg') or None
        objetivo = request.form.get('objetivo_principal') or None

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """INSERT INTO usuarios
                   (nombre, email, password_hash, rol, edad, sexo, altura_cm, peso_kg, objetivo_principal)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (nombre, email, password, rol, edad, sexo, altura, peso, objetivo)
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
        email = request.form['email']
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
            session['nombre'] = usuario['nombre']
            session['rol'] = usuario['rol']

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
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM usuarios")
    total_usuarios = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'admin'")
    total_admins = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'cliente'")
    total_clientes = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'coach'")
    total_coaches = cur.fetchone()['total']

    cur.execute("""
        SELECT r.id_rutina, r.titulo, r.descripcion, r.fecha_creacion, u.nombre AS nombre_usuario
        FROM rutinas r
        JOIN usuarios u ON r.id_usuario = u.id_usuario
        WHERE r.estado = 'pendiente'
        ORDER BY r.fecha_creacion DESC
    """)
    rutinas_pendientes = cur.fetchall()

    cur.execute("""
        SELECT c.id_comentario, c.comentario, c.fecha, u.nombre AS nombre_usuario
        FROM comentarios_ejercicio c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.estado = 'pendiente'
        ORDER BY c.fecha DESC
    """)
    comentarios_pendientes = cur.fetchall()

    cur.execute("""
        SELECT rp.id_resena, rp.comentario, rp.fecha, u.nombre AS nombre_usuario, 'producto' AS tipo
        FROM resenas_producto rp
        JOIN usuarios u ON rp.id_usuario = u.id_usuario
        WHERE rp.estado = 'pendiente'
        ORDER BY rp.fecha DESC
    """)
    resenas_producto = cur.fetchall()

    cur.execute("""
        SELECT rr.id_resena_rutina AS id_resena, rr.comentario, rr.fecha, u.nombre AS nombre_usuario, 'rutina' AS tipo
        FROM resenas_rutina rr
        JOIN usuarios u ON rr.id_usuario = u.id_usuario
        WHERE rr.estado = 'pendiente'
        ORDER BY rr.fecha DESC
    """)
    resenas_rutina = cur.fetchall()

    resenas_pendientes = resenas_producto + resenas_rutina

    cur.close()

    return render_template(
        'dashboard_admin.html',
        total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_clientes=total_clientes,
        total_coaches=total_coaches,
        rutinas_pendientes=rutinas_pendientes,
        comentarios_pendientes=comentarios_pendientes,
        resenas_pendientes=resenas_pendientes
    )


@app.route('/admin/usuario/<int:id>/cambiar_rol', methods=['POST'])
@login_required
@rol_required('admin')
def cambiar_rol(id):
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
    return render_template('coach/panel.html')

# ─────────────────────────────────────────
#  MODERACIÓN DE CONTENIDO
# ─────────────────────────────────────────
@app.route('/admin/rutina/<int:id_rutina>/aprobar', methods=['POST'])
@login_required
@rol_required('admin')
def aprobar_rutina(id_rutina):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rutinas SET estado = 'aprobado' WHERE id_rutina = %s", (id_rutina,))
    mysql.connection.commit()
    cur.close()
    flash('Rutina aprobada correctamente.', 'success')
    return redirect(url_for('panel_admin'))


@app.route('/admin/rutina/<int:id_rutina>/rechazar', methods=['POST'])
@login_required
@rol_required('admin')
def rechazar_rutina(id_rutina):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rutinas SET estado = 'rechazado' WHERE id_rutina = %s", (id_rutina,))
    mysql.connection.commit()
    cur.close()
    flash('Rutina rechazada.', 'info')
    return redirect(url_for('panel_admin'))


@app.route('/admin/comentario/<int:id_comentario>/aprobar', methods=['POST'])
@login_required
@rol_required('admin')
def aprobar_comentario(id_comentario):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE comentarios_ejercicio SET estado = 'aprobado' WHERE id_comentario = %s", (id_comentario,))
    mysql.connection.commit()
    cur.close()
    flash('Comentario aprobado correctamente.', 'success')
    return redirect(url_for('panel_admin'))


@app.route('/admin/comentario/<int:id_comentario>/rechazar', methods=['POST'])
@login_required
@rol_required('admin')
def rechazar_comentario(id_comentario):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE comentarios_ejercicio SET estado = 'rechazado' WHERE id_comentario = %s", (id_comentario,))
    mysql.connection.commit()
    cur.close()
    flash('Comentario rechazado.', 'info')
    return redirect(url_for('panel_admin'))


@app.route('/admin/resena/<tipo>/<int:id_resena>/aprobar', methods=['POST'])
@login_required
@rol_required('admin')
def aprobar_resena(tipo, id_resena):
    cur = mysql.connection.cursor()
    if tipo == 'producto':
        cur.execute("UPDATE resenas_producto SET estado = 'aprobado' WHERE id_resena = %s", (id_resena,))
    elif tipo == 'rutina':
        cur.execute("UPDATE resenas_rutina SET estado = 'aprobado' WHERE id_resena_rutina = %s", (id_resena,))
    mysql.connection.commit()
    cur.close()
    flash('Reseña aprobada correctamente.', 'success')
    return redirect(url_for('panel_admin'))


@app.route('/admin/resena/<tipo>/<int:id_resena>/rechazar', methods=['POST'])
@login_required
@rol_required('admin')
def rechazar_resena(tipo, id_resena):
    cur = mysql.connection.cursor()
    if tipo == 'producto':
        cur.execute("UPDATE resenas_producto SET estado = 'rechazado' WHERE id_resena = %s", (id_resena,))
    elif tipo == 'rutina':
        cur.execute("UPDATE resenas_rutina SET estado = 'rechazado' WHERE id_resena_rutina = %s", (id_resena,))
    mysql.connection.commit()
    cur.close()
    flash('Reseña rechazada.', 'info')
    return redirect(url_for('panel_admin'))


# ─────────────────────────────────────────
#  RUTAS PÚBLICAS
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template(
        "index.html",
        stats=stats,
        suplementos=suplementos,
        colaboradores=colaboradores
    )


@app.route("/planes")
def planes():
    return render_template("Plan.html")


@app.route("/dieta")
def dieta():
    return render_template("macros.html")


PLANES = {
    "basico": {"nombre": "Coach Básico", "precio": "11,99€"},
    "premium": {"nombre": "Coach Premium", "precio": "22,99€"},
}


@app.route('/pago_sub/<plan_id>')
def pago_sub(plan_id):
    plan = PLANES.get(plan_id)
    if not plan:
        return redirect(url_for('planes'))
    return render_template(
        'pago_sub.html',
        plan_nombre=plan["nombre"],
        precio=plan["precio"]
    )


@app.route('/pago-exitoso')
def pago_exitoso():
    return render_template('pago_exitoso.html')


# ─────────────────────────────────────────
#  RUTINAS
# ─────────────────────────────────────────
@app.route('/rutina')
def rutina():
    catalogo = {
        "Pecho": ["Press banca", "Press inclinado", "Aperturas"],
        "Espalda": ["Dominadas", "Remo con barra" ],
        "Hombro": ["Press militar", "Elevaciones laterales", "Pájaros"],
        "Pierna": ["Sentadilla", "Prensa", "Extensiones"],
        "Bíceps": ["Curl con barra","Curl martillo"],
        "Tríceps": ["Fondos en polea", "Press francés", "Extensión overhead"],
        "Abdomen": ["Rueda abdominal", "Plancha"]
    }

    semanal = {
        "Lunes": [],
        "Martes": [],
        "Miércoles": [],
        "Jueves": [],
        "Viernes": [],
        "Sábado": [],
        "Domingo": []
    }

    return render_template('semanal.html', catalogo=catalogo, semanal=semanal)


@app.route('/guardar_rutina', methods=['POST'])
@login_required
def guardar_rutina():
    data = request.get_json()

    titulo = data.get('titulo')
    descripcion = data.get('descripcion') or None
    nivel = data.get('nivel')
    publica = bool(data.get('publica', False))
    rutina_json = data.get('rutina')

    if not titulo or not nivel:
        return jsonify({
            'ok': False,
            'mensaje': 'Faltan campos obligatorios (título o nivel).'
        }), 400

    if not isinstance(rutina_json, dict):
        return jsonify({
            'ok': False,
            'mensaje': 'Formato de rutina no válido.'
        }), 400

    total_ejercicios = 0
    for dia, ejercicios in rutina_json.items():
        if isinstance(ejercicios, list):
            total_ejercicios += len(ejercicios)

    if total_ejercicios == 0:
        return jsonify({
            'ok': False,
            'mensaje': 'La rutina debe tener al menos un ejercicio.'
        }), 400

    dias_validos = {
        "Lunes": "lunes",
        "Martes": "martes",
        "Miércoles": "miercoles",
        "Miercoles": "miercoles",
        "Jueves": "jueves",
        "Viernes": "viernes",
        "Sábado": "sabado",
        "Sabado": "sabado",
        "Domingo": "domingo"
    }

    cur = None

    try:
        cur = mysql.connection.cursor()

        # 1. Guardar cabecera en rutinas
        cur.execute("""
            INSERT INTO rutinas (
                id_usuario,
                titulo,
                descripcion,
                nivel,
                publica,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            session['id_usuario'],
            titulo,
            descripcion,
            nivel,
            publica,
            'pendiente'
        ))

        id_rutina = cur.lastrowid

        # 2. Guardar detalle de ejercicios
        for dia_front, ejercicios in rutina_json.items():
            if dia_front not in dias_validos:
                continue

            dia_semana = dias_validos[dia_front]

            if not isinstance(ejercicios, list):
                continue

            orden = 1

            for ej in ejercicios:
                nombre_ej = ej.get('nombre')
                series = int(ej.get('series') or 0)
                reps = int(ej.get('reps') or 0)

                if not nombre_ej or series <= 0 or reps <= 0:
                    continue

                cur.execute(
                    "SELECT id_ejercicio FROM ejercicios WHERE nombre = %s",
                    (nombre_ej,)
                )
                fila_ej = cur.fetchone()

                if not fila_ej:
                    continue

                id_ejercicio = fila_ej['id_ejercicio']

                cur.execute("""
                    INSERT INTO rutina_detalle (
                        id_rutina,
                        dia_semana,
                        id_ejercicio,
                        orden_ejercicio,
                        series,
                        repeticiones,
                        descanso_seg,
                        notas
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    id_rutina,
                    dia_semana,
                    id_ejercicio,
                    orden,
                    series,
                    reps,
                    None,
                    None
                ))

                orden += 1

        mysql.connection.commit()

        return jsonify({
            'ok': True,
            'mensaje': 'Rutina guardada y enviada para revisión del administrador.',
            'id_rutina': id_rutina
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'ok': False,
            'mensaje': f'Error al guardar la rutina: {str(e)}'
        }), 500

    finally:
        if cur:
            cur.close()

@app.route('/admin/rutina/<int:id_rutina>')
@login_required
@rol_required('admin')
def ver_rutina_admin(id_rutina):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT r.id_rutina, r.titulo, r.descripcion, r.nivel, r.publica, r.estado,
               r.fecha_creacion, u.nombre AS nombre_usuario
        FROM rutinas r
        JOIN usuarios u ON r.id_usuario = u.id_usuario
        WHERE r.id_rutina = %s
    """, (id_rutina,))
    rutina = cur.fetchone()

    if not rutina:
        cur.close()
        flash('Rutina no encontrada.', 'error')
        return redirect(url_for('panel_admin'))

    cur.execute("""
        SELECT rd.id_detalle, rd.dia_semana, rd.orden_ejercicio, rd.series, rd.repeticiones,
               rd.descanso_seg, rd.notas,
               e.nombre AS nombre_ejercicio,
               e.grupo_muscular
        FROM rutina_detalle rd
        JOIN ejercicios e ON rd.id_ejercicio = e.id_ejercicio
        WHERE rd.id_rutina = %s
        ORDER BY
            FIELD(rd.dia_semana, 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'),
            rd.orden_ejercicio ASC
    """, (id_rutina,))
    detalles = cur.fetchall()
    cur.close()

    rutina_por_dias = {
        'lunes': [],
        'martes': [],
        'miercoles': [],
        'jueves': [],
        'viernes': [],
        'sabado': [],
        'domingo': []
    }

    for detalle in detalles:
        dia = detalle['dia_semana']
        if dia in rutina_por_dias:
            rutina_por_dias[dia].append(detalle)

    return render_template(
        'detalle_rutina_admin.html',
        rutina=rutina,
        rutina_por_dias=rutina_por_dias
    )

@app.route("/suplementacion")
def suplementacion():
    return render_template("suplementos.html")


if __name__ == "__main__":
    app.run(debug=True)