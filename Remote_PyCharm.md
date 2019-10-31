# Remote PC の Docker Container 上の Python 実行環境を Local PC の PyCharm から利用する

Python で開発をしていると IDE が欲しくなります。
Python の IDE として現在とても使いやすいと感じているのが、[PyCharm][]です。

また、Python で開発しているプロジェクトは Deep Learning を利用したものであり、
その Training/Validation/Testing に GPU を使う必要があります。
GPU を搭載したサーバは複数の開発者からアクセスできるリモートにあります。
当然ながら、Deep Learning 開発環境の構築には、
開発ツール/ライブラリ/フレームワーク/GPUドライバのバージョン依存が問題になるため、
[Docker][] Container を用意して、その上で開発環境を構築します。

手元のPC上で作成したコード群を変更するたびに、
Remote PC の Docker Container 上にコピーしてデバッグして修正して、
を繰り返すのはとても長く辛い開発になります。

つまり、手元のPCで [PyCharm][] を使いつつ、
動作環境はリモートPCの Docker Container を使用する。
という環境を使いたくなります。

このメモは、それを実現するためのものです。

全体像としては以下です。
![Remote PyCharm Architecture](pics/RemotePyCharm.png "Remote PyCharm Architecture")

また、必要となる SSH Tunnel は以下です。
Port 8888 は Jupyter Notebook を実行するためのものです。
![Remote PyCharm SSH Tunnels](pics/RemotePyCharm_sshtun.png "Remote PyCharm SSH Tunnels")

- - -
[PyCharm]: https://www.jetbrains.com/pycharm/
[Docker]: https://www.docker.com/
