 resenas_pendientes=resenas_producto + resenas_rutina
    )

@app.route("/coach/panel")
@login_required
@rol_required("coach", "admin")
def panel_coach():
    return render_template("coach/panel.html")

@app.route("/admin/usuario/<int:id>/cambiar_rol", methods=["POST"])
@login_required
@rol_required("admin")
def cambiar_rol(id):
    nuevo_rol = request.form.get("rol")
    if nuevo_rol not in ("admin", "cliente", "coach"):
        flash("Rol no válido.", "error")
        return redirect(url_for("panel_admin"))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET rol = %s WHERE id_usuario = %s", (nuevo_rol, id))
    mysql.connection.commit()
    cur.close()
    flash("Rol actualizado correctamente.", "success")
    return redirect(url_for("panel_admin"))

@app.route("/admin/rutina/<int:id_rutina>/aprobar", methods=["POST"])
@login_required
@rol_required("admin")
def aprobar_rutina(id_rutina):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rutinas SET estado = 'aprobado' WHERE id_rutina = %s", (id_rutina,))
    mysql.connection.commit()
    cur.close()
    flash("Rutina aprobada correctamente.", "success")
    return redirect(url_for("panel_admin"))

@app.route("/admin/rutina/<int:id_rutina>/rechazar", methods=["POST"])
@login_required
@rol_required("admin")
def rechazar_rutina(id_rutina):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rutinas SET estado = 'rechazado' WHERE id_rutina = %s", (id_rutina,))
    mysql.connection.commit()
    cur.close()
    flash("Rutina rechazada.", "info")
    return redirect(url_for("panel_admin"))

@app.route("/admin/comentario/<int:id_comentario>/aprobar", methods=["POST"])
@login_required
@rol_required("admin")
def aprobar_comentario(id_comentario):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE comentarios_ejercicio SET estado = 'aprobado' WHERE id_comentario = %s", (id_comentario,))
    mysql.connection.commit()
    cur.close()
    flash("Comentario aprobado correctamente.", "success")
    return redirect(url_for("panel_admin"))

@app.route("/admin/comentario/<int:id_comentario>/rechazar", methods=["POST"])
@login_required
@rol_required("admin")
def rechazar_comentario(id_comentario):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE comentarios_ejercicio SET estado = 'rechazado' WHERE id_comentario = %s", (id_comentario,))
    mysql.connection.commit()
    cur.close()
    flash("Comentario rechazado.", "info")
    return redirect(url_for("panel_admin"))

@app.route("/admin/resena/<tipo>/<int:id_resena>/aprobar", methods=["POST"])
@login_required
@rol_required("admin")
def aprobar_resena(tipo, id_resena):
    cur = mysql.connection.cursor()
    if tipo == "producto":
        cur.execute("UPDATE resenas_producto SET estado = 'aprobado' WHERE id_resena = %s", (id_resena,))
    elif tipo == "rutina":
        cur.execute("UPDATE resenas_rutina SET estado = 'aprobado' WHERE id_resena_rutina = %s", (id_resena,))
    mysql.connection.commit()
    cur.close()
    flash("Reseña aprobada correctamente.", "success")
    return redirect(url_for("panel_admin"))

@app.route("/admin/resena/<tipo>/<int:id_resena>/rechazar", methods=["POST"])
@login_required
@rol_required("admin")
def rechazar_resena(tipo, id_resena):
    cur = mysql.connection.cursor()
    if tipo == "producto":
        cur.execute("UPDATE resenas_producto SET estado = 'rechazado' WHERE id_resena = %s", (id_resena,))
    elif tipo == "rutina":
        cur.execute("UPDATE resenas_rutina SET estado = 'rechazado' WHERE id_resena_rutina = %s", (id_resena,))
    mysql.connection.commit()
    cur.close()
    flash("Reseña rechazada.", "info")
    return redirect(url_for("panel_admin"))

@app.route("/pago_sub/<plan_id>")
def pago_sub(plan_id):
    PLANES = {
        "basico": {"nombre": "Coach Básico", "precio": "11,99€"},
        "premium": {"nombre": "Coach Premium", "precio": "22,99€"},
    }
    plan = PLANES.get(plan_id)
    if not plan:
        return redirect(url_for("planes"))
    return render_template("pago_sub.html", plan_nombre=plan["nombre"], precio=plan["precio"])

@app.route("/pago-exitoso")
def pago_exitoso():
    return render_template("pago_exitoso.html")

@app.route("/guardar_rutina", methods=["POST"])
@login_required
def guardar_rutina():
    data = request.get_json()
    titulo = data.get("titulo")
    descripcion = data.get("descripcion") or None
    nivel = data.get("nivel")
    publica = bool(data.get("publica", False))
    rutina_json = data.get("rutina")

    if not titulo or not nivel:
        return jsonify({"ok": False, "mensaje": "Faltan campos obligatorios (título o nivel)."}), 400

    if not isinstance(rutina_json, dict):
        return jsonify({"ok": False, "mensaje": "Formato de rutina no válido."}), 400

    total_ejercicios = 0
    for _, ejercicios_dia in rutina_json.items():
        if isinstance(ejercicios_dia, list):
            total_ejercicios += len(ejercicios_dia)

    if total_ejercicios == 0:
        return jsonify({"ok": False, "mensaje": "La rutina debe tener al menos un ejercicio."}), 400

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
        cur.execute("""
            INSERT INTO rutinas (id_usuario, titulo, descripcion, nivel, publica, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (session["id_usuario"], titulo, descripcion, nivel, publica, "pendiente"))

        id_rutina = cur.lastrowid

        for dia_front, ejercicios_dia in rutina_json.items():
            if dia_front not in dias_validos or not isinstance(ejercicios_dia, list):
                continue
            dia_semana = dias_validos[dia_front]
            orden = 1

            for ej in ejercicios_dia:
                nombre_ej = ej.get("nombre")
                series = int(ej.get("series") or 0)
                reps = int(ej.get("reps") or 0)

                if not nombre_ej or series <= 0 or reps <= 0:
                    continue

                cur.execute("SELECT id_ejercicio FROM ejercicios WHERE nombre = %s", (nombre_ej,))
                fila_ej = cur.fetchone()
                if not fila_ej:
                    continue

                cur.execute("""
                    INSERT INTO rutina_detalle (
                        id_rutina, dia_semana, id_ejercicio, orden_ejercicio, series, repeticiones, descanso_seg, notas
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_rutina, dia_semana, fila_ej["id_ejercicio"], orden, series, reps, None, None))
                orden += 1

        mysql.connection.commit()
        return jsonify({"ok": True, "mensaje": "Rutina guardada y enviada para revisión del administrador.", "id_rutina": id_rutina}), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"ok": False, "mensaje": f"Error al guardar la rutina: {str(e)}"}), 500

    finally:
        if cur:
            cur.close()

@app.route("/admin/rutina/<int:id_rutina>")
@login_required
@rol_required("admin")
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
        flash("Rutina no encontrada.", "error")
        return redirect(url_for("panel_admin"))

    cur.execute("""
        SELECT rd.id_detalle, rd.dia_semana, rd.orden_ejercicio, rd.series, rd.repeticiones,
               rd.descanso_seg, rd.notas, e.nombre AS nombre_ejercicio, e.grupo_muscular
        FROM rutina_detalle rd
        JOIN ejercicios e ON rd.id_ejercicio = e.id_ejercicio
        WHERE rd.id_rutina = %s
        ORDER BY FIELD(rd.dia_semana, 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'),
                 rd.orden_ejercicio ASC
    """, (id_rutina,))
    detalles = cur.fetchall()
    cur.close()

    rutina_por_dias = {d: [] for d in ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]}
    for detalle in detalles:
        if detalle["dia_semana"] in rutina_por_dias:
            rutina_por_dias[detalle["dia_semana"]].append(detalle)

    return render_template("detalle_rutina_admin.html", rutina=rutina, rutina_por_dias=rutina_por_dias)

if __name__ == "__main__":
    app.run(debug=True)
