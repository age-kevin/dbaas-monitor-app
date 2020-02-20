from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# 数据库地址
engine = create_engine('oracle://qhdbmon:Lahmy11c@139.198.16.188:1521/test1', encoding='utf-8', echo=True)
# 数据库连接
DBSession = sessionmaker(bind=engine)
session = DBSession()
