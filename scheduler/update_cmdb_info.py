from db_conn import conn
from logger.monitor_logger import get_logger
import datetime


logger = get_logger(__name__)
currently_time = datetime.datetime.now()


def update_instance_info(is_accessable, currently_role, is_readwrite, currently_hostname, instance_name,
                         instance_port, default_role):
    # noinspection PyBroadException
    try:
        pass
    except Exception:
        logger.error("更新数据库异常！==========>scheduler/update_cmdb_info.py update_instance_info()")
