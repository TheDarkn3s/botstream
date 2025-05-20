from flask import Flask, jsonify
import subprocess
import threading
import time

app = Flask(__name__)

# Variable global para almacenar la URL actual del stream
stream_url = None

# Función para actualizar la URL del stream cada 30 segundos
def actualizar_stream():
    global stream_url
    while True:
        try:
            result = subprocess.run(
                ["streamlink", "--twitch-disable-ads", "--stream-url", "https://www.twitch.tv/il_daniil", "best"],
                capture_output=True, text=True
            )
            nueva_url = result.stdout.strip()

            if nueva_url:
                if nueva_url != stream_url:
                    print(f"🔄 Nueva URL obtenida: {nueva_url}")
                    stream_url = nueva_url
                else:
                    print("✅ La URL sigue siendo la misma, no se actualiza.")
            else:
                print("❌ No se pudo obtener la URL del stream")

        except Exception as e:
            print(f"❌ Error al actualizar la URL del stream: {e}")

        time.sleep(30)  # Esperar 30 segundos antes de volver a actualizar

# Ruta en Flask para devolver la URL actual del stream
@app.route('/get_stream')
def get_stream():
    if stream_url:
        return jsonify({"stream_url": stream_url})
    else:
        return jsonify({"error": "No se ha podido obtener la URL del stream"}), 404

# Iniciar el hilo para actualizar la URL cada 30 segundos
threading.Thread(target=actualizar_stream, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
