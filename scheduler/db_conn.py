from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


def conn(url):
    # 数据库地址
    db_engine = create_engine(url, encoding='utf-8', echo=True)
    # 数据库连接
    db_session = sessionmaker(bind=db_engine)
    session = db_session()
    return session

