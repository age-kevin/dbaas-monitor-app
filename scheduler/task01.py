import yaml
from db_conn import session
from remote_run import ssh


def my_job01():
    handle_sql()


def handle_sql():
    with open("config/conf.yaml", "r") as yaml_file:
        yaml_obj = yaml.load(yaml_file)
        item_detail = yaml_obj["item_detail"]
        for item in item_detail:
            project = item_detail[item]
            if project["enabled"] == "y":
                if project["type"] == "sql":
                    cmd = project["cmd"]
                    print(cmd)
                    # 查询
                    res = session.execute(cmd)
                    for a in res:
                        result = a[0]
                        print(result)
                elif project["type"] == "shell":
                    cmd = project["cmd"]
                    print(cmd)
                    # 执行主机命令
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    # stdin  标准格式的输入，是一个写权限的文件对象
                    # stdout 标准格式的输出，是一个读权限的文件对象
                    # stderr 标准格式的错误，是一个写权限的文件对象
                    # 读返回结果
                    print("stdout:" + str(stdout.read().decode()))
