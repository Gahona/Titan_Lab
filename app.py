from flask import Flask, render_template
 
app = Flask(__name__)
 
# ── RUTINA SEMANAL ──────────────────────────────────────────────────────────
rutina = {
    "Lunes": [
        "Press de banca plano — 4x8",
        "Press inclinado con mancuernas — 3x10",
        "Aperturas en polea — 3x12",
        "Press militar — 4x8",
        "Elevaciones laterales — 3x15",
        "Fondos en paralelas — 3x10",
    ],
    "Martes": [
        "Sentadilla trasera — 4x6",
        "Prensa de piernas — 3x12",
        "Extensiones de cuádriceps — 3x15",
        "Curl femoral tumbado — 3x12",
        "Peso muerto rumano — 3x10",
        "Gemelos de pie — 4x20",
    ],
    "Miércoles": [
        "Dominadas pronadas — 4x8",
        "Remo con barra — 4x8",
        "Remo en polea baja — 3x12",
        "Jalón al pecho — 3x12",
        "Curl de bíceps con barra — 4x10",
        "Curl martillo — 3x12",
    ],
    "Jueves": [
        "Press de banca plano — 4x6",
        "Aperturas con mancuernas en banco plano — 3x12",
        "Crossover en polea — 3x15",
        "Press Arnold — 4x10",
        "Elevaciones frontales — 3x12",
        "Tríceps en polea — 4x12",
    ],
    "Viernes": [
        "Peso muerto convencional — 4x5",
        "Sentadilla frontal — 3x8",
        "Zancadas con mancuernas — 3x12",
        "Hip thrust — 4x10",
        "Curl femoral de pie — 3x12",
        "Gemelos sentado — 4x20",
    ],
    "Sábado": [
        "Dominadas supinas — 4x8",
        "Remo con mancuerna un brazo — 3x10",
        "Pull-over en polea — 3x12",
        "Curl de bíceps concentrado — 3x12",
        "Plancha abdominal — 4x45s",
        "Rueda abdominal — 3x12",
    ],
    "Domingo": [
        "Descanso activo",
        "Estiramientos generales — 20 min",
        "Foam roller — 15 min",
        "Caminar o cardio suave — 30 min",
    ],
}
 
# ── RUTAS ───────────────────────────────────────────────────────────────────
 
@app.route("/")
def index():
    return render_template("semanal.html", rutina=rutina)
 
 
@app.route("/rutina")
def rutina_view():
    return render_template("semanal.html", rutina=rutina)
 
 
# ── ARRANQUE ─────────────────────────────────────────────────────────────────
 
if __name__ == "__main__":
    app.run(debug=True)
 