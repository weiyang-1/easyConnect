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
                         password=self.connect_host["pwd"], timeout=10)  # 初始化的时候连接到新的服务器
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
                "pwd": "1234asdf",
                "jobs": [
                    {
                        "path": "/home/lemon",
                        "type": "touch stop_zhipin.sh"
                    },
                    {
                        "path": "/home/lemon",
                        "type": "touch restart_zhipin.sh"
                    }
                ]
            }
        }
    for i in ["huzheng", "yangwei"]:
        try:
            easy_conn = EasyConnectHandle(test_host[i])
        except:
            logger.error(f"连接服务器{test_host[i]}失败")
        transport = easy_conn.ssh.get_transport()
        if len(test_host[i].get("jobs", [])) >= 1:
            for job in test_host[i]["jobs"]:
                channel = transport.open_session()
                channel.exec_command(f"cd {job['path']};{job['type']}")
                logger.info(f"服务器---{easy_conn.connect_host['ip']}执行---cd {job['path']};{job['type']}---成功")
                time.sleep(2)
        else:
            logger.info(f"服务器---{easy_conn.connect_host['ip']}暂时没有任务")
        easy_conn.quit()

