# -*- coding: utf-8 -*-
"""
20190330
"""

import paramiko
import time
from confs.log import logger


class EasyConnectHandle(object):
    """操作远程服务器"""

    def __init__(self, connect_host_name:dict):
        """初始化参数"""
        """
            "189":{
                "ip":"192.168.11.189",
                "user_name":"liuchao",
                "pwd":"jianxun1302"
            },
        """
        self.connect_host = connect_host_name
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接陌生服务器
        self.ssh.connect(hostname=self.connect_host["ip"], port=22, username=self.connect_host["user_name"],
                         password=self.connect_host["pwd"])  # 初始化的时候连接到新的服务器
        logger.info(f"登录服务器---{self.connect_host['ip']}成功:")

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(EasyConnectHandle, cls).__new__(cls)
        return cls._instance

    def exec(self, cmd=""):
        """执行操作"""
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.read().decode()

    def quit(self):
        """断开服务器"""
        self.ssh.close()
        logger.info(f"退出服务器---{self.connect_host['ip']}成功")

if __name__ == '__main__':
    test_host = {
        "huzheng": {
                "ip": "192.168.0.111",
                "user_name": "lemon",
                "pwd": "1234asdf"
            },
        "yangwei": {
                "ip": "192.168.92.131",
                "user_name": "yangwei",
                "pwd": "123456"
        }
        }
    for i in ["huzheng"]:
        easy_conn = EasyConnectHandle(test_host[i])
        transport = easy_conn.ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command("touch c.py")
        time.sleep(2)
        easy_conn.quit()
        time.sleep(2)

