from flask import Flask, request, Response
from flask_request_params import bind_request_params
import json
import configparser
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# 数据库连接
engine = create_engine('oracle://qhdbmon:Lahmy11c@139.198.16.188:1521/test1', echo=True)
# 连接数据库
# conn = db.connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)
app.before_request(bind_request_params)


@app.route('/main/text01', methods=['GET'])
def get_text01():
    handle_conf()

    text = request.params["askjson"]
    action = request.params["action"]
    if action == "query":
        jieguo = {"text": text}
        print(text)
        return Response(json.dumps(jieguo))
    else:
        return "Hello World"


def handle_conf():
    config = configparser.ConfigParser()
    config.read("config/test01.txt")
    # print(config.sections())
    # print(config.options("global"))
    # print(config.get("global", "db_type"))
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
    print(res)
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
