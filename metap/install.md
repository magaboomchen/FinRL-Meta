# Installation
pip version 21.2.4
```
conda install -c conda-forge ta-lib
```

wsl中运行jupyter notebook
```
这是一个很好的演练，解释了如何设置 jupyter notebook 以使用 WSL 运行并在 Windows 中启动浏览器而不会出现此错误：

https://towardsdatascience.com/running-jupyter-notebook-on-wsl-while-using-firefox-on-windows-5a47ebfae4c1?gi=fc70b24c75bf

有两个重要步骤：

运行jupyter notebook --generate-config以生成文件，~/.jupyter/jupyter_notebook_config.py然后更改以下行：
c.NotebookApp.use_redirect_file = False

将您的浏览器添加到~/.bashrcEg
export BROWSER='/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe'

不要忘记源 bashrc：

source ~/.bashrc

jupyter notebook
```

