from flask import Flask
import configparser
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
# from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:test_print',
            'args': '',  # 执行程序参数
            'trigger': 'interval',
            'seconds': 5
        }
    ]


def test_print():
    print("1")


# 数据库地址
engine = create_engine('oracle://qhdbmon:Lahmy11c@139.198.16.188:1521/test1', encoding='utf-8', echo=True)
# 数据库连接
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# @app.route('/hello', methods=["POST", "GET"])
# def hello():
#     return "success"


def handle_conf():
    config = configparser.ConfigParser()
    config.read("config/test01.txt")
    item_detail = config.options("item_detail")
    print(item_detail)
    a = 1
    for item in item_detail:
        name_key = "name0" + str(a)
        print(config.get("item_detail", name_key))
        enabled_key = "enabled0" + str(a)
        enabled_value = config.get("item_detail", enabled_key)
        if enabled_value == "y":
            type_key = "type0" + str(a)
            if type_key == item:
                type_value = config.get("item_detail", item)
                if type_value == "sql":
                    cmd_key = "cmd0" + str(a)
                    cmd_value = config.get("item_detail", cmd_key)
                    res = conn_db(cmd_value)
                    print(res)
                    a = a + 1


def conn_db(param):
    # 查询
    res = session.execute(param)
    for item in res:
        result = item[0]
    return result


if __name__ == "__main__":
    # app.config.from_object(Config())
    scheduler = BlockingScheduler()
    scheduler.add_job(test_print, 'interval', seconds=5)
    scheduler.start()
    # scheduler = APScheduler()  # 实例化APScheduler
    # scheduler.init_app(app)  # 把任务列表放进flask
    # scheduler.start()  # 启动任务列表
    # app.run(debug=False)  # 启动flask
