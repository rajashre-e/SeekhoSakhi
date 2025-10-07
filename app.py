from flask import Flask, render_template, request, send_file
from routes import faq_routes
from routes import prediction_routes
from gtts import gTTS
import os

def create_app():
    app = Flask(__name__)

    # -------------------- Register Blueprints --------------------
    app.register_blueprint(faq_routes.bp)
    app.register_blueprint(prediction_routes.bp)

    # -------------------- Home Route --------------------
    @app.route("/")
    def home():
        return render_template("index.html")

    # -------------------- TTS Route (gTTS) --------------------
    @app.route("/tts", methods=["POST"])
    def tts():
        data = request.json
        text = data.get("text", "")
        if not text:
            return {"error": "No text provided"}, 400

        # Generate gTTS audio
        tts = gTTS(text=text, lang="en")
        audio_path = "static/audio/output.mp3"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        tts.save(audio_path)

        return send_file(audio_path)
    
    @app.route("/about")
    def about():
        return render_template("about.html")

    return app

# -------------------- Run App --------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
