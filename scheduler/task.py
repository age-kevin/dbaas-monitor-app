import configparser
from db_conn import session
from remote_run import ssh


def my_job():
    handle_sql()


def handle_sql():
    config = configparser.RawConfigParser()
    config.read("config/test01.txt")
    item_detail = config.options("item_detail")
    print(item_detail)
    type_list = []
    cmd_list = []
    for item in item_detail:
        if 'type' in item:
            type_list.append(item)
        elif 'cmd' in item:
            cmd_list.append(item)
    print(type_list)
    print(cmd_list)
    count = 1
    for type_key in type_list:
        if config.get("item_detail", type_key) == 'sql':
            cmd_value = config.get("item_detail", "cmd0" + str(count))
            # 查询
            res = session.execute(cmd_value)
            count = count + 1
            for a in res:
                result = a[0]
                print(result)
        if config.get("item_detail", type_key) == 'shell':
            cmd_value = config.get("item_detail", "cmd0" + str(count))
            # 执行主机命令
            stdin, stdout, stderr = ssh.exec_command(cmd_value)
            # stdin  标准格式的输入，是一个写权限的文件对象
            # stdout 标准格式的输出，是一个读权限的文件对象
            # stderr 标准格式的错误，是一个写权限的文件对象
            # 读返回结果
            print("stdout:" + str(stdout.read().decode()))
            count = count + 1
