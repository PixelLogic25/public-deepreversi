from flask import Flask


# Import Blueprints
from .views.reversi_view import reversi_bp


from .views.reversi_view import setup_app

def create_app():
    app = Flask(__name__)
    app.register_blueprint(reversi_bp)


    setup_app(app)  # 初期化関数を登録
    return app



