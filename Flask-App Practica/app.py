from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Datos para la página principal
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
    "basico": {"nombre": "Coach Básico", "precio": "11,99€"},
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

@app.route('/rutina')
def rutina():
    # catalogo de ejercicios que aparece en el panel izquierdo
    catalogo = {
        "Pecho": ["Press banca", "Press inclinado", "Aperturas", "Fondos"],
        "Espalda": ["Dominadas", "Remo con barra", "Jalón al pecho", "Remo en polea"],
        "Hombro": ["Press militar", "Elevaciones laterales", "Pájaros"],
        "Pierna": ["Sentadilla", "Prensa", "Extensiones", "Curl femoral", "Gemelos"],
        "Bíceps": ["Curl con barra", "Curl alterno", "Curl martillo"],
        "Tríceps": ["Fondos en polea", "Press francés", "Extensión overhead"],
    }

    # rutina semanal actual (vacía por defecto, el JS la rellena desde localStorage)
    semanal = {
        "Lunes": [], "Martes": [], "Miércoles": [],
        "Jueves": [], "Viernes": [], "Sábado": [], "Domingo": []
    }

    return render_template('semanal.html', catalogo=catalogo, semanal=semanal)


@app.route('/guardar_rutina', methods=['POST'])
def guardar_rutina():
    data = request.get_json()
    # aquí puedes guardar en base de datos si quieres
    # por ahora el JS ya lo guarda en localStorage
    return {'ok': True}, 200

if __name__ == "__main__":
    app.run(debug=True)