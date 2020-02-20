import configparser
from db_conn import session


def my_job():
    config = configparser.ConfigParser()
    config.read("config/test01.txt")
    item_detail = config.options("item_detail")
    print(item_detail)
    cmd_value = config.get("item_detail", "cmd01")
    # 查询
    res = session.execute(cmd_value)
    for item in res:
        result = item[0]
    print(result)
