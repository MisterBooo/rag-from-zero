# 🐛 跑不通?看这里

按你的系统找对应小节。绝大多数「装不上 / 跑不了」都是下面三类:**命令名不对、缺 CA 证书、pypi 太慢**。

---

## macOS

### `zsh: command not found: pip` / `python`

macOS 自带的命令是 `python3` / `pip3`,**不是** `python` / `pip`。直接用带 `3` 的:

```bash
pip3 install -r requirements.txt
python3 reproduce-disaster.py
```

> 想偷懒少打字,可以建别名(可选):`echo 'alias python=python3 pip=pip3' >> ~/.zshrc && source ~/.zshrc`

### `SSL: CERTIFICATE_VERIFY_FAILED`

你装的是 [python.org](https://www.python.org/downloads/) 官方安装包,它默认**不会**把 CA 证书装进系统,导致 pip 走 HTTPS 时验证不了证书。在终端运行一次(把 `3.13` 换成你的实际版本):

```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

成功时末尾会出现类似 `update complete` 的输出。装完再重新 `pip3 install`。

> 不确定版本?`ls /Applications/ | grep Python` 看一下目录名里的版本号。
> 用 Homebrew 装的 Python(`brew install python`)一般没有这个问题。

### `pip3 install` 卡在国外源 / 一直 timeout

换清华镜像(一次性):

```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或设为默认源(以后都走镜像):

```bash
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install -r requirements.txt
```

---

## Windows

### 命令是 `pip` / `python` 还是 `py -3`?

Windows 通常用 `pip` / `python`;如果提示找不到,用 `py -3` 启动器最稳:

```cmd
py -3 -m pip install -r requirements.txt
py -3 reproduce-disaster.py
```

### pypi 太慢

```cmd
py -3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## Linux

命令一般和 macOS 一致,用 `python3` / `pip3`:

```bash
pip3 install -r requirements.txt
python3 reproduce-disaster.py
```

若提示 `pip3: command not found`,先装:`sudo apt install python3-pip`(Debian/Ubuntu)或 `sudo dnf install python3-pip`(Fedora)。

---

## 通用

- **缺依赖报 `ModuleNotFoundError` / `ImportError`**:确认你 `cd` 进了对应章节目录,且 `pip3 install -r requirements.txt` 装在**当前正在用的** Python 上(`python3 -m pip install ...` 可保证装到同一个解释器)。
- **首次跑 `real_embedding.py` / `build_index.py` 很慢**:`sentence-transformers` 会自动下载几百 MB 模型权重,需要联网且耐心等一次;之后有本地缓存就快了。
- **只想验证逻辑、不想装重型依赖**:`rag_project/` 下跑 `python3 tests/smoke_test.py`,零依赖、不下模型。

还有问题?在 [Issues](https://github.com/MisterBooo/rag-from-zero/issues) 里贴上**完整报错**(包含命令和系统),我会看。
