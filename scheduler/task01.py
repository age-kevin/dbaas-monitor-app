import yaml
import os
import socket
from remote_run import ssh
from logger.monitor_logger import get_logger
from concurrent.futures import ThreadPoolExecutor
from conn_prometheus import conn_gateway, PmMetrics
from db_conn import conn


# 创建线程池执行器
executor = ThreadPoolExecutor(2)
logger = get_logger(__name__)


def my_job01():
    logger.debug("定时任务开始!")
    # 判断是本台主机上是什么数据库实例
    db_type = config_is_exists()
    # 获取数据源信息
    get_db_source(db_type)


def handle_sql(flag, session, instance_info):
    logger.debug("flag: {}".format(flag))
    with open("config/oracle_config.yaml", "r", encoding='UTF-8') as yaml_file:
        yaml_obj = yaml.load(yaml_file)
        item_detail = yaml_obj["item_detail"]
        job = PmMetrics()
        for item in item_detail:
            project = item_detail[item]
            # 指标名称
            index_name = project["index_name"]
            # 指标描述
            desc = project["desc"]
            if project["enabled"] == "y":
                if project["type"] == "sql":
                    cmd = project["cmd"]
                    logger.debug("sql命令：{}".format(cmd))
                    # 查询
                    res = session.execute(cmd)
                    for a in res:
                        result = a[0]
                        logger.debug("结果：{}".format(result))
                        # push_to_gateway
                        conn_gateway(flag, index_name, desc, instance_info, result, job.registry)
                elif project["type"] == "shell":
                    cmd = project["cmd"]
                    logger.debug("shell命令：{}".format(cmd))
                    # 执行主机命令
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    # stdin  标准格式的输入，是一个写权限的文件对象
                    # stdout 标准格式的输出，是一个读权限的文件对象
                    # stderr 标准格式的错误，是一个写权限的文件对象
                    logger.debug("结果：{}".format(str(stdout.read().decode())))
                    # 读返回结果
                    conn_gateway(flag, index_name, desc, instance_info, stdout.read().decode(), job.registry)


def get_db_source(db_type):
    # 获取本机ip地址
    # my_name = socket.getfqdn(socket.gethostname())
    # my_address = socket.gethostbyname(my_name)
    my_address = "10.60.233.51"
    logger.debug("本机地址：{}".format(my_address))
    # noinspection PyBroadException
    with open("config/" + db_type + "_config.yaml", "r", encoding='UTF-8') as yaml_file:
        yaml_obj = yaml.load(yaml_file)
        my_global = yaml_obj["global"]
        # 实例信息配置文件
        instance_config_file = my_global["instance_config_file"]
        # 账户名
        db_user = my_global["user_name"]
        # 密码
        db_password = my_global["password"]
        with open(instance_config_file, "r") as f:
            for line in f.readlines():
                line = line.strip('\n')
                if line:
                    instance_info = line.split(':')
                    logger.debug("实例信息：{}".format(instance_info))
                    db_port = instance_info[0]
                    instance_name = instance_info[2]
                    url = db_type + "://" + db_user + ":" + db_password + "@" + my_address + ":" + str(
                            db_port) + "/" + instance_name
                    logger.debug("数据库连接串：{}".format(url))
                    session = conn(url)
                    flag = db_type + "_" + instance_name + "_" + db_port
                    # executor.submit(handle_sql, flag, session, instance_info)
                    handle_sql(flag, session, instance_info)


def config_is_exists():
    if os.path.exists("config/oracle_config.yaml"):
        db_type = "oracle"
    elif os.path.exists("config/redis_config.yaml"):
        db_type = "redis"
    return db_type
