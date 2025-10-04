from flask import Flask, render_template
from routes import faq_routes
from routes import prediction_routes  # <-- new blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(faq_routes.bp)
    app.register_blueprint(prediction_routes.bp)  # <-- register prediction blueprint

    @app.route("/")
    def home():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
