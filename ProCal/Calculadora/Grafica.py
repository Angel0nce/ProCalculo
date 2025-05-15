import io
import base64
import matplotlib
matplotlib.use('Agg')  # Correcto para servidores
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, jsonify

Graficador = Blueprint('graficador', __name__)

@Graficador.route('/graficador')
def graficador():
    return render_template('Grafica.html')

@Graficador.route('/graficar', methods=['POST'])
def graficar():
    try:
        data = request.get_json()
        xs = data.get('x', [])
        ys = data.get('y', [])

        xs = [float(x) for x in xs if x != ""]
        ys = [float(y) for y in ys if y != ""]

        if not xs or not ys or len(xs) != len(ys):
            return jsonify({"error": "Datos inválidos"}), 400

        fig, ax = plt.subplots()
        ax.scatter(xs, ys, color="red")
        ax.plot(xs, ys, linestyle="-", color="black")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Gráfica de Coordenadas")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close(fig)

        return jsonify({"image": f"data:image/png;base64,{image_base64}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
