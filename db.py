import sqlalchemy as db
import pandas as pd


def connect_db(DATABASE_URL):
    """
    db 연결하기
    """
    engine = db.create_engine(DATABASE_URL)
    connection = engine.connect()
    metadata = db.MetaData()
    return engine, connection, metadata


def get_list_from_table(table_name, user_id, engine, connection, metadata):
    """
    table 이름을 입력 받아서 해당 데이터 전부 가져오기
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    # query = db.select([table])
    query = db.select([table.columns.book_id]).where(
        table.columns.user_id == user_id)
    result = connection.execute(query)
    result_set = result.fetchall()
    return result_set


def get_not_update_pd_from_table(table_name, table_name2, engine, connection, metadata):
    """
    table 이름을 입력 받아서 해당 데이터 dataframe으로 반환
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    table2 = db.Table(table_name2, metadata,
                      autoload=True, autoload_with=engine)
    sub_query = db.select([table2.columns.book_id])
    query = db.select([table]).where(
        table.columns.id.not_in(sub_query))
    result_set = pd.read_sql_query(query, connection, index_col=None, coerce_float=True,
                                   params=None, parse_dates=None, chunksize=None, dtype=None)
    return result_set


def get_pd_from_table(table_name, engine, connection, metadata):
    """
    table 이름을 입력 받아서 해당 데이터 dataframe으로 반환
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = db.select([table])
    result_set = pd.read_sql_query(query, connection, index_col=None, coerce_float=True,
                                   params=None, parse_dates=None, chunksize=None, dtype=None)
    return result_set


def delete_user_similar(table_name, user_id, engine, metadata):
    """
    user_id 에 해당하는 데이터 전부 삭제
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    try:
        query = table.delete().where(table.columns.user_id == user_id)
        engine.execute(query)
    except:
        pass


def delete_book_similar(table_name, book_id, engine, metadata):
    """
    user_id 에 해당하는 데이터 전부 삭제
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    try:
        query = table.delete().where(table.columns.book_id == book_id)
        engine.execute(query)
    except:
        pass


def insert_user_similar(table_name, user_id, book_id, engine, metadata):
    """
    유저별로 유사도가 높은 책 정보 업데이트
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = table.insert().values(user_id=user_id, book_id=book_id)
    engine.execute(query)


def insert_book_similar(table_name, book_id, book_similar_id, engine, metadata):
    """
    책별 유사도가 높은 책 정보 업데이트
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = table.insert().values(book_id=book_id, book_similar_id=book_similar_id)
    engine.execute(query)


def insert_movie_similar(table_name, book_id, movie_similar_id, engine, metadata):
    """
    책과 유사한 영화 정보 업데이트
    """
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = table.insert().values(book_id=book_id, movie_similar_id=movie_similar_id)
    engine.execute(query)
