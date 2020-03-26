import paramiko


# 创建一个ssh的客户端，用来连接服务器
ssh = paramiko.SSHClient()
# 创建一个ssh的白名单
know_host = paramiko.AutoAddPolicy()
# 加载创建的白名单
ssh.set_missing_host_key_policy(know_host)
# 连接服务器
ssh.connect(
    hostname="10.60.233.51",
    port=2222,
    username="oracle",
    password="oracle"
)


