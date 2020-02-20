from core import scheduler
from flask import Flask


def create_app():
    app = Flask(__name__)
    # 配置任务，不然无法启动任务
    app.config.update(
        {"SCHEDULER_API_ENABLED": True,
         "JOBS": [
             {
                 "id": "my_job",  # 任务ID
                 "func": "task:my_job",  # 任务位置
                 "trigger": "interval",  # 触发器
                 "seconds": 5  # 时间间隔
             }
            ]}
        )
    scheduler.init_app(app)
    scheduler.start()
    return app
