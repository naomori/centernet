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

この開発環境の全体像を以下に示します。
![Remote PyCharm Architecture](pics/RemotePyCharm.png "Remote PyCharm Architecture")

また、必要となる SSH Tunnel は以下です。
Port 8888 は Jupyter Notebook を実行するためのものです。
![Remote PyCharm SSH Tunnels](pics/RemotePyCharm_sshtun.png "Remote PyCharm SSH Tunnels")

- - -
# Remote Server & Docker Container の準備 

GPUを使用するため、[NGC][]から [PyTorch][]用の Container Image をダウンロードします。
その後で、Container のセットアップをします(詳細な設定内容については割愛します)。

- - -
以下は実際に [CenterNet][] の動作に必要な [Python][] 環境を
[Docker][] Container 上に構築した例です。

[Python][] 環境は conda を使用します。
[CenterNet][] では、 [Python][], [PyTorch][], OpenCV などのバージョン依存がありますので、
注意してインストールする必要がありました。
```bash
root@centernet:~# conda create --name CenterNet python=3.6
root@centernet:~# conda init
root@centernet:~# exit
$ docker exec -it centernet bash
(base) root@centernet:/workspace# conda activate CenterNet
(CenterNet) root@centernet:~# conda update -n base -c defaults conda
(CenterNet) root@centernet:~# conda install pytorch=1.1 torchvision -c pytorch
(CenterNet) root@centernet:~# conda install Cython
(CenterNet) root@centernet:~# conda install -c conda-forge opencv=4.1.1
(CenterNet) root@centernet:~# conda install -c conda-forge numba easydict scipy
(CenterNet) root@centernet:~# conda install -c conda-forge progress matplotlib
(CenterNet) root@centernet:~# apt install libgl1-mesa-glx
(CenterNet) root@centernet:~# conda install -c conda-forge pycocotools
```
- - -

そうやって[CenterNet][]用のイメージ(ここでは centernet:1.0 としています)を作成した後、
Containerを生成するときのスクリプトを以下のようにします。
```bash
docker run --detach \
        -p 8888:8888 \
        -p 2222:22 \
        --privileged \
        --gpus all \
        --shm-size=1g --ulimit memlock=-1 \
        -it \
        -v /home/my_project:/workspace/my_project \
        --hostname centernet \
        --name centernet \
        centernet:1.0
```
`-p`オプションで Remote Server から Docker Container へのポート転送設定を行います。
* Port`8888:8888` は Jupyter用です
* Port`2222:22`はSSH用です

`-v`オプションで Remote Server 上のディレクトリを
Docker Container 上にマウントします。
* Remote Server 上のディレクトリが `/home/my_project` です
* Docker Container 上のマウントポイントが `/workspace/my_project` です

上記のコマンドによって、ポート転送をディレクトリのマウントができます。
しかし、Docker Container上では sshd が起動していないため、
ssh でアクセスすることができません。

- - -
## Docker Container 上で sshd を準備

まずは Docker Container に sshd をインストールします。
```bash
(base) root@centernet:~# apt install openssh-server
```

Local PC の Pycharm から Docker Container には root アカウントでログインしているため、
以下のようにログインを許可しておきます。
パスワードログインを許可しているのはメンテナンスのためです。
実際には、公開鍵を登録して、それを使ってログインします(パスフレーズなし)。

```bash
(base) root@centernet:~# vim /etc/ssh/sshd_config
```
```diff
--- sshd_config.orig    2019-10-24 17:03:39.993604170 +0000
+++ sshd_config 2019-10-24 16:59:20.989606640 +0000
@@ -30,11 +30,13 @@

 #LoginGraceTime 2m
 #PermitRootLogin prohibit-password
+PermitRootLogin yes
 #StrictModes yes
 #MaxAuthTries 6
 #MaxSessions 10

 #PubkeyAuthentication yes
+PubkeyAuthentication yes

 # Expect .ssh/authorized_keys2 to be disregarded by default in future.
 #AuthorizedKeysFile    .ssh/authorized_keys .ssh/authorized_keys2
@@ -54,6 +56,7 @@

 # To disable tunneled clear text passwords, change to no here!
 #PasswordAuthentication yes
+PasswordAuthentication yes
 #PermitEmptyPasswords no

 # Change to yes to enable challenge-response passwords (beware issues with
```

root のパスワードは適当に設定しておきます。
```bash
(base) root@centernet:~# passwd root
```

sshd のテストとして Docker Container で sshd を起動して、
```bash
(base) root@centernet:~# /etc/init.d/ssh start
* Starting OpenBSD Secure Shell server sshd                 [OK]
```
Remote Server から root アカウントでログインしてみます。
```bash
$ slogin -p 2222 root@localhost
(base) root@centernet:~#
```
ログインできました。

## Docker Container 上で jupyter を準備

最初に jupyter lab をインストールします。
```bash
(base) root@centernet:~# conda activate CenterNet
(CenterNet) root@centernet:~# conda install -c conda-forge jupyterlab
``` 

Jupyter 利用上のアクセス制限を外します。

まずは、設定ファイルを生成します。
```bash
(base) root@centernet:~# conda activate CenterNet
(CenterNet) root@centernet:~# jupyter lab --generate-config
Writing default config to: /root/.jupyter/jupyter_noetbook_config.py
```
そしてアクセス関連のパラメタを変更します。
```bash
(CenterNet) root@centernet:~# vim /root/.jupyter/jupyter_noetbook_config.py
```

```diff
--- jupyter_notebook_config.py.orig     2019-10-24 15:27:12.145659367 +0000
+++ jupyter_notebook_config.py  2019-10-24 15:35:29.173654627 +0000
@@ -82,7 +82,7 @@
 #c.NotebookApp.allow_remote_access = False

 ## Whether to allow the user to run the notebook as root.
-#c.NotebookApp.allow_root = False
+c.NotebookApp.allow_root = True

 ## DEPRECATED use base_url
 #c.NotebookApp.base_project_url = '/'
@@ -202,6 +202,7 @@

 ## The IP address the notebook server will listen on.
 #c.NotebookApp.ip = 'localhost'
+c.NotebookApp.ip = '0.0.0.0'

 ## Supply extra arguments that will be passed to Jinja environment.
 #c.NotebookApp.jinja_environment_options = {}
@@ -258,7 +259,7 @@
 #c.NotebookApp.nbserver_extensions = {}

 ## The directory to use for notebooks and kernels.
-#c.NotebookApp.notebook_dir = ''
+c.NotebookApp.notebook_dir = '/workspace/my_project'

 ## Whether to open in a browser after starting. The specific browser used is
 #  platform dependent and determined by the python standard library `webbrowser`
@@ -273,7 +274,7 @@
 #    from notebook.auth import passwd; passwd()
 #
 #  The string should be of the form type:salt:hashed-password.
-#c.NotebookApp.password = ''
+c.NotebookApp.password = ''

 ## Forces users to use a password for the Notebook server. This is useful in a
 #  multi user environment, for instance when everybody in the LAN can access each
@@ -284,7 +285,7 @@
 #c.NotebookApp.password_required = False

 ## The port the notebook server will listen on.
-#c.NotebookApp.port = 8888
+c.NotebookApp.port = 8888

 ## The number of additional ports to try if the specified port is not available.
 #c.NotebookApp.port_retries = 50
@@ -337,7 +338,7 @@
 #
 #  Setting to an empty string disables authentication altogether, which is NOT
 #  RECOMMENDED.
-#c.NotebookApp.token = '<generated>'
+c.NotebookApp.token = ''

 ## Supply overrides for the tornado.web.Application that the Jupyter notebook
 #  uses.
```

jupyter lab のテストとして、 Docker Container で jupyter lab を起動して、
```bash
(CenterNet) root@centernet:~# jupyter lab --config=/root/.jupyter/jupyter_noetbook_config.py
```

Local PCからブラウザで以下のURLにアクセスしてみます。  
`http://<Remote Server のIPアドレス>:8888`  
アクセスできました。

## Docker Container 起動時に sshd & jupyter lab を起動する

このままでは、 Docker Container を立ち上げたときに sshd も jupyter lab も立ち上がっていないため、
一度 Docker Container にログインして、手動で立ち上げる必要があります。
とても面倒ですし、忘れがちです。

そこで、自動で sshd も jupyter lab も起動するようにします。
[こちら](https://docs.docker.com/engine/examples/running_ssh_service/)が
参考になります。
ただし、jupyter labは自動で起動できなかったので、sshdだけ自動化しておきます。

jupyter lab を簡単に起動するためのスクリプトを用意して、
後で簡単に jupyter lab だけ立ち上げられるようにしておきます。
```bash
$ docker exec -it centernet bash
(base) root@centernet:~# vim /usr/local/bin/jupyterlab_start.sh
#!bin/bash
nohup /opt/conda/envs/CenterNet/bin/jupyter lab --config=/root/.jupyter/jupyter_notebook_config.py &> /dev/null &
(base) root@centernet:~# chmod +x /usr/local/bin/jupyterlab_start.sh
```

そして、このイメージを `docker commit` で保存しておきます。
次に Dockerfile を作成します。
```bash
$ vim Dockerfile
```
```Dockerfile
FROM centernet:1.1

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
```

この Dockerfile をもとに、イメージを作成します。
```bash
$ docker build -t ceneternet:1.2 .
```

これで、sshdが自動で起動するイメージが出来ました。
あとは、これまでと同様に centernet:1.2 から container を生成し、
```bash
$ docker exec -it centernet bash
(base) root@centernet:~# /usr/local/bin/jupyterlab_start.sh
```
で jupyter lab を起動できます。

上記の centernet のタグについては、好きは番号を使ってください。

- - -
# Local PC の準備

## ssh access without pass-phrase
Local PC から Remote Server 上の Docker Container に SSH でアクセスするときの
認証には公開鍵を使用することにします。また、パスフレーズは空にしておきます。
パスフレーズを空にするのは簡単で、パスフレーズの入力時にリターンキーを押すだけです。
```bash
$ ssh-keygen -t rsa
```
作成した公開鍵を Remote Server 上の Docker Container に配置します。
まずは、Local PCで作成した公開鍵を Remote Sever 上に転送し、
```bash
$ scp ~/.ssh/id_rsa.pub <Remote Server>:
```
転送された公開鍵を Remote Server 上で Docker Container にコピーします。
```bash
$ docker cp id_rsa.pub centernet:/root/
```
Docker Container にログインし、ssh の公開鍵を設定しておきます。　
```bash
$ docker exec -it center bash
(base) root@centernet:~# mkdir .ssh
(base) root@centernet:~# chmod 700 .ssh
(base) root@centernet:~# touch .ssh/authorized_keys
(base) root@centernet:~# chmod 600 .ssh/authorized_keys
(base) root@centernet:~# cat id_rsa.pub >> .ssh/authorized_keys
```

## Local PC から Remote Server のポート転送

Local PC から Remote Server にポート転送の設定をします。
このポート転送をすることで、Local PC から Remote Server 経由で
Remote Server 上の Docker Container にアクセスすることができます。
```bash
$ ssh -fN -X -L 8888:localhost:8888 <Remote Server>
$ ssh -fN -X -L 2222:localhost:2222 <Remote Server>
```
つまり、 Local PC の Port`8888`にアクセスすると、
Remote Server経由で Docker Container の Port`8888` にアクセスし、
Local PC の Port `2222` にアクセスすると、
Remote Server経由で Docker Container の Port`22` にアクセスできるようになります。

## 

- - -
[PyCharm]: https://www.jetbrains.com/pycharm/
[Docker]: https://www.docker.com/
[NGC]: https://ngc.nvidia.com/
[PyTorch]: https://pytorch.org/
[Python]: https://www.python.org/
[CenterNet]: https://github.com/xingyizhou/CenterNet
