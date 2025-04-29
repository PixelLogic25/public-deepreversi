# public-deepreversi
リバーシの深層学習のコード
# プロジェクト概要

このプロジェクトは、**強化学習でリバーシ（オセロ）AIを育成できるシステム**です。  
育成したAIとは、**ウェブブラウザ上で対戦しながら挙動を確認**することができます。

- 対局中に「待った」や「やり直し」が可能です。
- 「待った」後に別の手を打った場合でも、**棋譜の分岐**を保持して管理できます。
- コードを修正することで、**モデルの構成変更や学習方法の変更**にも対応可能です。

# 使用技術

- **言語**：JavaScript、Python
- **フレームワーク**：Flask、TensorFlow

# 開発環境構築方法

## Anacondaを使用する場合

本プロジェクトは**Windows上でAnaconda**を使用して開発しました。

手順1. Anacondaをインストールします。
手順2. Anacondaを起動して、Python 3.9系の新しい仮想環境を作成します。
<p align="center">
 <img src="/README_images/005.png" alt="説明用画像" />
</p>
<p align="center">図1.環境作成画面</p>


> ※Pythonのバージョンは**3.9系であれば問題ありません**。  
> （例：3.9.21で環境を作成しても、パッケージ追加時に自動的に3.9.18になる）
手順3. 手順2.で作成した環境内で `flask` と `tensorflow` をインストールします。
<p align="left">
 <img src="/README_images/015.png" alt="説明用画像" />
</p>
図2.
<p align="left">
 <img src="/README_images/005.png" alt="説明用画像" />
</p>

他のOS（Linux, Macなど）でも、基本的に同様の手順で構築できるはずです。

## Anacondaを使用しない場合

使用パッケージとバージョン一覧を参考に、個別にインストールしてください。  
基本的には**Flask**と**TensorFlow**をインストールすれば動作するはずですが、保証はできません。  
以下に動作したパッケージ名とバージョンの表を示します。
| Package                 | Version |
|--------------------------|---------|
| absl-py                  | 2.1.0   |
| aiohappyeyeballs         | 2.4.0   |
| aiohttp                  | 3.10.5  |
| aiosignal                | 1.2.0   |
| astunparse               | 1.6.3   |
| async-timeout            | 4.0.3   |
| attrs                    | 23.1.0  |
| blinker                  | 1.6.2   |
| Brotli                   | 1.0.9   |
| cachetools               | 5.3.3   |
| certifi                  | 2024.8.30 |
| cffi                     | 1.17.1  |
| charset-normalizer       | 3.3.2   |
| click                    | 8.1.7   |
| colorama                 | 0.4.6   |
| cryptography             | 41.0.3  |
| Flask                    | 3.0.3   |
| flatbuffers              | 24.3.25 |
| frozenlist               | 1.4.0   |
| gast                     | 0.4.0   |
| google-auth              | 2.29.0  |
| google-auth-oauthlib     | 0.4.4   |
| google-pasta             | 0.2.0   |
| grpcio                   | 1.48.2  |
| h5py                     | 3.11.0  |
| idna                     | 3.7     |
| importlib-metadata       | 7.0.1   |
| itsdangerous             | 2.2.0   |
| Jinja2                   | 3.1.4   |
| keras                    | 2.10.0  |
| Keras-Preprocessing      | 1.1.2   |
| Markdown                 | 3.4.1   |
| MarkupSafe               | 2.1.3   |
| mkl_fft                  | 1.3.10  |
| mkl_random               | 1.2.7   |
| mkl-service              | 2.4.0   |
| multidict                | 6.0.4   |
| numpy                    | 1.26.4  |
| oauthlib                 | 3.2.2   |
| opt-einsum               | 3.3.0   |
| packaging                | 24.1    |
| pip                      | 24.2    |
| protobuf                 | 3.20.3  |
| pyasn1                   | 0.4.8   |
| pyasn1-modules           | 0.2.8   |
| pycparser                | 2.21    |
| PyJWT                    | 2.8.0   |
| pyOpenSSL                | 23.2.0  |
| PySocks                  | 1.7.1   |
| requests                 | 2.32.3  |
| requests-oauthlib        | 2.0.0   |
| rsa                      | 4.7.2   |
| scipy                    | 1.13.1  |
| setuptools               | 75.1.0  |
| six                      | 1.16.0  |
| tensorboard              | 2.10.0  |
| tensorboard-data-server  | 0.6.1   |
| tensorboard-plugin-wit   | 1.8.1   |
| tensorflow               | 2.10.0  |
| tensorflow-estimator     | 2.10.0  |
| termcolor                | 2.1.0   |
| typing_extensions        | 4.11.0  |
| urllib3                  | 2.2.3   |
| Werkzeug                 | 3.0.3   |
| wheel                    | 0.44.0  |
| win-inet-pton            | 1.1.0   |
| wrapt                    | 1.14.1  |
| yarl                     | 1.11.0  |
| zipp                     | 3.17.0  |


# プロジェクトの起動・使用方法

1. Visual Studio Code (VSCode) を起動します。
2. **AIを学習させる場合**：
   - `learning.py` をデバッガーで実行します。
3. **AIと対戦・挙動を確認する場合**：
   - 同梱の `launch.json` を使用して、「Pythonデバッガー: launch.jsonを使用したデバッグ」でサーバーを起動します。
   - `DeepReversiKitPlatTest` を選択します。
   - ブラウザで [http://127.0.0.1:8888](http://127.0.0.1:8888) にアクセスします。
