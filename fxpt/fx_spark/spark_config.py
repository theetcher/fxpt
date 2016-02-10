import subprocess

from fxpt.fx_spark import cfg


def run():
    subprocess.Popen(['explorer', r'/select,', cfg.TOOLS_CFG_USER.replace('/', '\\')])
