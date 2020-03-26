# noinspection PyProtectedMember
from prometheus_client import push_to_gateway, CollectorRegistry, Gauge
import yaml
from logger.monitor_logger import get_logger


logger = get_logger(__name__)


with open("config/configuration.yaml", "r") as yaml_file:
    yaml_obj = yaml.load(yaml_file)
    prometheus_url = yaml_obj["prometheus_url"]


class PmMetrics:
    def __init__(self):
        self.registry = CollectorRegistry()


def conn_gateway(flag, index_name, desc, instance_info, value, registry):
    tags = ["PORT", "NAME", "VERSION", "DEFAULT_ROLE", "SITE", "TENANT_ID", "PRD_REGION",
            "CPU_COUNT", "ENTITY_ID"]
    if instance_info:
        port = instance_info[0]
        name = instance_info[2]
        version = instance_info[3]
        default_role = instance_info[4]
        site = instance_info[5]
        tenant_id = instance_info[6]
        prd_region = instance_info[7]
        cpu_count = instance_info[8]
        entity_id = instance_info[9]
        g = Gauge(index_name, desc, tags, registry=registry)
        # lables括号中是给标签tags中赋值，set括号是给指标赋值
        g.labels(port, name, version, default_role, site, tenant_id, prd_region, cpu_count, entity_id).set(value)
        push_to_gateway(prometheus_url, job=flag, registry=registry)
        logger.debug("指标: {}推送完成。".format(index_name))
    else:
        logger.error("获取实例信息异常！===========>scheduler/conn_prometheus.py conn_gateway()")
