import pandas as pd
from sqlalchemy import create_engine
TABLE_NAME = 'heroes'

engine = create_engine('mysql+pymysql://root:Root123456@rm-cn-4xl3gmscg000cxpo.rwlb.rds.aliyuncs.com/python_db')


def read_from_db(name):
    df = None
    try:
        query = "SELECT * FROM " + name
        df = pd.read_sql(query, engine)
    except Exception as e:
        print("Error")
    return df


def read_from_csv(path):
    df = pd.read_csv(path)
    return df


def save_to_db(df, name):
    try:
        df.to_sql(name, engine, if_exists='replace')
    except Exception as e:
        print("Error")


def save_to_csv(df, path):
    df.to_csv(path, index=False)