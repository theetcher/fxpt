import subprocess

from fxpt3.fx_spark import cfg


def run():
    subprocess.Popen(['explorer', r'/select,', cfg.TOOLS_CFG_USER.replace('/', '\\')])
