from flask import Flask, render_template

app = Flask(__name__)

# ── Datos de la app ────────────────────────────────────────────────────────────

stats = [
    {"valor": "+3,000", "label": "Miembros activos"},
    {"valor": "180+",   "label": "Ejercicios"},
    {"valor": "99%",    "label": "Satisfacción"},
]

suplementos = [
    {
        "nombre": "Proteína",
        "imagen": "proteina.png",
        "alt":    "Proteína whey",
        "descripcion": (
            "Aumenta tu recuperación muscular y acelera tus resultados con proteína "
            "de alta calidad. Ideal para ganar masa muscular, mantener tus músculos "
            "y recuperarte después de entrenamientos intensos."
        ),
    },
    {
        "nombre": "Creatina",
        "imagen": "creatina.png",
        "alt":    "Creatina",
        "descripcion": (
            "Mejora tu fuerza, potencia y rendimiento en cada entrenamiento. "
            "La creatina es uno de los suplementos más eficaces para aumentar masa "
            "muscular y superar tus límites físicos."
        ),
    },
    {
        "nombre": "Pre-entreno",
        "imagen": "prewornk.png",
        "alt":    "Pre-entreno",
        "descripcion": (
            "Activa tu energía y concentración antes de entrenar. "
            "Consigue más intensidad, motivación y resistencia para rendir al máximo "
            "en cada sesión."
        ),
    },
    {
        "nombre": "BCAAs / EAAs",
        "imagen": "intrawork.png",
        "alt":    "BCAAs / EAAs",
        "descripcion": (
            "Protege tu masa muscular y mejora la recuperación durante y después del "
            "entrenamiento. Perfectos para reducir la fatiga y mantener el rendimiento "
            "incluso en rutinas exigentes."
        ),
    },
    {
        "nombre": "Omega 3",
        "imagen": "omega3.png",
        "alt":    "Omega 3",
        "descripcion": (
            "Cuida tu corazón, articulaciones y bienestar general con ácidos grasos "
            "esenciales. Un suplemento clave para mejorar la salud y favorecer una "
            "recuperación más eficiente."
        ),
    },
    {
        "nombre": "Zinc / Magnesio",
        "imagen": "zmzinc.png",
        "alt":    "Zinc y Magnesio",
        "descripcion": (
            "Mejora tu descanso, recuperación muscular y niveles de energía. "
            "Una combinación perfecta para optimizar el rendimiento físico y apoyar "
            "tu sistema inmunológico."
        ),
    },
]

colaboradores = [
    {"imagen": "iogenix.logo-removebg-preview.png",  "alt": "Io.Genix"},
    {"imagen": "logopaypal-removebg-preview.png",    "alt": "PayPal"},
    {"imagen": "pannattaaa-removebg-preview.png",    "alt": "Panatta"},
]

# ── Rutas ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template(
        "main.html",
        stats=stats,
        suplementos=suplementos,
        colaboradores=colaboradores,
    )


# ── Punto de entrada ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)