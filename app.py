from flask import Flask, render_template, request, jsonify
from services.image_service import procesar_imagen
from services.huffman_service import procesar_huffman, decodificar_huffman
from services.shannon_fano_service import procesar_shannon_fano, decodificar_shannon_fano

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/imagenes")
def imagenes():
    return render_template("imagenes.html")


@app.route("/codificacion")
def codificacion():
    return render_template("codificacion.html")


@app.route("/api/procesar-imagen", methods=["POST"])
def api_procesar_imagen():
    if "imagen" not in request.files:
        return jsonify({"error": "No se recibió ninguna imagen"}), 400

    imagen = request.files["imagen"]
    resolucion = int(request.form.get("resolucion", 500))
    bits = int(request.form.get("bits", 8))

    try:
        resultado = procesar_imagen(imagen, resolucion, bits)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/codificar", methods=["POST"])
def api_codificar():
    data = request.get_json()
    texto = data.get("texto", "")

    if not texto.strip():
        return jsonify({"error": "El texto no puede estar vacío"}), 400

    try:
        resultado_huffman = procesar_huffman(texto)
        resultado_shannon = procesar_shannon_fano(texto)

        return jsonify({
            "huffman": resultado_huffman,
            "shannon_fano": resultado_shannon
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/decodificar-huffman", methods=["POST"])
def api_decodificar_huffman():
    data = request.get_json()
    cadena = data.get("cadena", "")
    codigos = data.get("codigos", {})

    try:
        resultado = decodificar_huffman(cadena, codigos)
        return jsonify({"texto": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/decodificar-shannon", methods=["POST"])
def api_decodificar_shannon():
    data = request.get_json()
    cadena = data.get("cadena", "")
    codigos = data.get("codigos", {})

    try:
        resultado = decodificar_shannon_fano(cadena, codigos)
        return jsonify({"texto": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)