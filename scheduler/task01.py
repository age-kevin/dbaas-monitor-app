import yaml
from remote_run import ssh
import logger.monitor_logger
from concurrent.futures import ThreadPoolExecutor
import db_conn


# 创建线程池执行器
executor = ThreadPoolExecutor(2)
logger = logger.monitor_logger.get_logger(__name__)


def my_job01():
    logger.info("定时任务开始!")
    # 获取数据源信息
    get_db_source()


def handle_sql(num, session):
    logger.info("num: %s" % num)
    with open("config/conf.yaml", "r") as yaml_file:
        yaml_obj = yaml.load(yaml_file)
        item_detail = yaml_obj["item_detail"]
        for item in item_detail:
            project = item_detail[item]
            if project["enabled"] == "y":
                if project["type"] == "sql":
                    cmd = project["cmd"]
                    logger.info("命令：%s" % cmd)
                    # 查询
                    res = session.execute(cmd)
                    for a in res:
                        result = a[0]
                        logger.info("结果：%s" % result)
                elif project["type"] == "shell":
                    cmd = project["cmd"]
                    logger.info("命令：%s" % cmd)
                    # 执行主机命令
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    # stdin  标准格式的输入，是一个写权限的文件对象
                    # stdout 标准格式的输出，是一个读权限的文件对象
                    # stderr 标准格式的错误，是一个写权限的文件对象
                    # 读返回结果
                    logger.info("结果：%s:" % str(stdout.read().decode()))


def get_db_source():
    try:
        with open("config/db_conf.yaml", "r") as yaml_file:
            yaml_obj = yaml.load(yaml_file)
            db_info = yaml_obj["db_info"]
            for db_source in db_info:
                entity = db_info[db_source]
                db_type = entity["db_type"]
                db_ip = entity["db_ip"]
                db_user = entity["db_user"]
                db_password = entity["db_password"]
                db_port = entity["db_port"]
                entity_name = entity["entity_name"]
                url = db_type + "://" + db_user + ":" + db_password + "@" + db_ip + ":" + str(
                    db_port) + "/" + entity_name
                print(url)
                session = db_conn.conn(url)
                count = 1
                executor.submit(handle_sql, count, session)
    except Exception:
        logger.error("get_db_source()异常！")

