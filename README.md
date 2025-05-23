# DeepReversi
<p align="center">
 <img src="/README_images/main.png" alt="対戦画面" />
</p>

ディープラーニングでリバーシを強化学習させるコード。
# プロジェクト概要

このプロジェクトでは、**強化学習でリバーシ（オセロ）AIを育成でき、ウェブブラウザ上で対戦しながら挙動を確認**することができます。
学習入門キットのようなものはあっても、ソースコードで書かれたも強化学習のテンプレートが少ないので公開しました。

- 対局中に「待った」や「やり直し」が可能です。
- 「待った」後に別の手を打った場合でも、**棋譜の分岐**を保持して管理できます。
- コードを修正することで、**モデルの構成変更や学習方法の変更**にも対応可能です。
> このREADME.mdはとても丁寧に作っているつもりですが、肝心のソースコードはだいぶ読みづらいです。
> プログラミング初心者にはさっぱりわからないと思いますが、こちらでサポートはしません。ご了承ください。
# 使用技術

- **言語**：JavaScript、Python
- **フレームワーク**：Flask
- **主なライブラリ**：TensorFlow
# 開発環境構築方法

## Anacondaを使用する場合

本プロジェクトは**Windows上でAnaconda**を使用して開発しました。同じ手順を示します。

### 手順1. Anacondaをインストールします。
### 手順2. Anacondaを起動して、Python 3.9系の新しい仮想環境を作成します。
<p align="center">
 <img src="/README_images/005.png" alt="説明用画像" />
</p>
<p align="center">図1.環境作成画面</p>


> ※Pythonのバージョンは**3.9系であれば問題ありません**。  
> （例：3.9.21で環境を作成しても、パッケージ追加時に自動的に3.9.18になる）
### 手順3. 手順2.で作成した環境内で `flask` と `tensorflow` をインストールします。

図2.の赤丸で囲ってある場所を「not installed」にします。
<p align="center">
 <img src="/README_images/015.png" alt="説明用画像" />
</p>
<p align="center">図2.パッケージ追加画面1</p>

図3.図4.のようにtensorflowとflaskを追加した後、図5のapplyを押します。

Search packageに"tensorflow"と入力してtensorflowにチェックを付けます。
<p align="center">
 <img src="/README_images/025.png" alt="説明用画像" />
</p>
<p align="center">図3.パッケージ追加画面 tensorflow追加</p>

Search packageに"flask"と入力してflaskにチェックを付けます。
<p align="center">
 <img src="/README_images/035.png" alt="説明用画像" />
</p>
<p align="center">図4.パッケージ追加画面2 flask追加</p>

<p align="center">
 <img src="/README_images/045.png" alt="説明用画像" />
</p>
<p align="center">図5パッケージ追加画面右下のapply/Clear</p>

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

### 手順a.このプロジェクトをダウンロードなり、フォークなりしてどこか任意のフォルダに入れておきます。
### 手順b.Visual Studio Code (VSCode) を起動します。
起動したらフォルダーを開くを押して、手順a.のフォルダを開きます。
<p align="center">
 <img src="/README_images/055.png" alt="説明用画像" />
</p>
<p align="center">図6 フォルダーを開くを押す</p>

### 手順c.VSCode右下の小さいpythonのバージョンが表示されているところをクリックして手順2.で作成した環境を選択します。
> すでに選択されていれば問題ありません
<p align="center">
 <img src="/README_images/065.png" alt="説明用画像" />
</p>
<p align="center">図7 バージョン選択</p>


### 手順d. **AIを学習させる場合**：
   - `learning.py` をデバッガーで実行します。
> 初期のコードでは学習AIは初期状態、対戦相手はランダム打ちです。

#### 学習手順
1. 勝率8割を10回連続で達成すると学習が自動で終了します。しばらく実行させると、自動で終了して/DeepReversiKit/model_files/配下にfinal_model.h5が作成されます。
> (途中で中断したい場合は、learning.pyのどこかの行にブレークポイントを入れて、VSCodeのデバッグコンソールで「agent.model.save(f'model_files/model_{e+1}.h5')」と打ち込むと途中セーブされます。)
> また1万対局ごとに自動でセーブされます。

2. そのままの名前にしておくと次学習が完了したとき消え去ってしまうので名前を変更しておきましょう。ここでは「sedai1.h5」とします。

3. sedai1.h5はランダム打ち相手で育ったモデルで、まだ非常に弱いです。さらに強化するために/DeepReversiKit/learning.pyの100行目付近を書き換えます。図7の対戦相手（強さ固定）とエージェント（学習して強くなるモデル）の定義の部分です。

<p align="center">
 <img src="/README_images/075.png" alt="説明用画像" />
</p>
<p align="center">図7 学習相手と学習初期状態を指定する部分</p>

図7の読み込むファイルをNoneにすると、対戦相手はランダム打ち、エージェントは初期状態になります。
このままもう一度実行するとまた最初から学習し直してしまうので図8のように書き直します。

<p align="center">
 <img src="/README_images/080.png" alt="説明用画像" />
</p>
<p align="center">図8 学習相手と学習初期状態を書き換え</p>

さきほど1.で作成したモデル同士を戦わせて、さらに強くなってもらいます。

4. しばらく待つとまた圧勝しているはずなので、sedai2.h5として保存して、気が済むまで1.～3.を繰り返します。同梱のfinal_model_gen_9_13.h5は1週間ほどかけて13回繰り返しました。


### 手順e. **AIと対戦・挙動を確認する場合**：
   - 図9を参考に、動作させたいモデルを指定します。
/DeepReversiKit/views/reversi_view.pyの39行目を、手順dで作成したモデルが"sedai1.h5"なら、図9の赤の下線部を"sedai1.h5"に書き換えます。
<p align="center">
 <img src="/README_images/085.png" alt="説明用画像" />
</p>
<p align="center">図9 動かしたいモデルの指定箇所。</p>
<p>同梱の `launch.json` を使用して、「Pythonデバッガー: launch.jsonを使用したデバッグ」でサーバーを起動します。</p>
<p>`DeepReversiKitPlatTest` を選択します。</p>
<p>ブラウザで [http://127.0.0.1:8888]にアクセスします。</p>
<p>遊べます。</p>


以下により詳しい説明は時間ができたときに記述します。
