from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

catalogo = {
    "Pecho": ["Press banca", "Press inclinado mancuernas", "Aperturas peck deck"],
    "Espalda": ["Dominadas", "Remo con barra", "Jalón al pecho"],
    "Pierna": ["Sentadilla", "Peso muerto rumano", "Prensa de piernas"],
    "Hombro": ["Press militar", "Elevaciones laterales", "Face pull"],
    "Brazos": ["Curl bíceps", "Curl martillo", "Press francés"],
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

@app.route("/")
def home():
    return render_template(
        "semanal.html",
        semanal=semanal,
        catalogo=catalogo,
        orden_dias=orden_dias
    )

@app.route("/rutina")
def rutina_view():
    return render_template(
        "semanal.html",
        semanal=semanal,
        catalogo=catalogo,
        orden_dias=orden_dias
    )

@app.route("/crear-rutina")
def crear_rutina():
    return render_template(
        "semanal.html",
        semanal=semanal,
        catalogo=catalogo,
        orden_dias=orden_dias
    )

@app.route("/guardar_rutina", methods=["POST"])
def guardar_rutina():
    global semanal
    data = request.get_json() or {}

    for dia in orden_dias:
        semanal[dia] = data.get(dia, [])

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
