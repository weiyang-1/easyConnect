# -*- coding: utf-8 -*-
"""
20190330
"""

import time
from easy_connect import EasyConnectHandle
from confs.log import logger
from confs.conf import AliYun_jobs


def run_main():
    tasks = [AliYun_jobs.get(i, {}) for i in ["189", "201", "202", "203", "205", "206", "244", "245"]]  # , "201", "202", "203", "205", "206", "244", "245"
    for task in tasks:
        if len(task) == 0:
            continue
        # 取到了任务 开始连接
        try:
            easy_conn = EasyConnectHandle(task)
        except:
            logger.error(f"连接服务器{task['ip']}失败")
            time.sleep(2)
            continue
        transport = easy_conn.ssh.get_transport()
        if len(task.get("jobs", [])) >= 1:
            for job in task["jobs"]:
                channel = transport.open_session()
                channel.exec_command(f"cd {job['path']};{job['type']}")
                logger.info(f"服务器---{easy_conn.connect_host['ip']}执行---cd {job['path']};{job['type']}---成功")
                time.sleep(2)
        else:
            logger.info(f"服务器---{easy_conn.connect_host['ip']}暂时没有任务")
        easy_conn.quit()



if __name__ == '__main__':
    run_main()