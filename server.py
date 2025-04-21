import logging
import sys

# デバッグ用のサイトを起動したいときはコメントアウトを外す
#from web_deep_reversi_debug_app import create_app

# 本番のウェブサイト用
from DeepReversiKit import create_app

# アプリケーションを作成
app = create_app()



if __name__ == '__main__':
    app.run(debug=True, port=5000)
