"""
This is the project entrypoint, brining together the UserModel and UserService
"""
from sqlalchemy import create_engine, text, exc, Connection, Result
from sqlalchemy.orm import Session
from loguru import logger


def execute_and_print(conn: Connection, query: str) -> Result:
    res = conn.execute(text(query))
    print(res)
    try:
        return res
    except exc.ResourceClosedError:
        pass

def main():
    """Project Entrypoint"""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    # engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    
    # NON-AUTOCOMMITING
    # requires conn.commit() before the block ends
    # way: commit as you go
    with engine.connect() as conn:        
        create_table_query = """
        create table users (
            id int primary key,
            name varchar not null
        )
        """
        select_all_users_query = "select * from users"
        insert_users_query = """
        insert into users (id, name) values
        (1, 'Tushar'),
        (2, 'Ayush'),
        (3, 'Shishir')
        """
        insert_user_query = """
        insert into users (id, name) values (:id, :name)
        """

        execute_and_print(conn, create_table_query)
        execute_and_print(conn, select_all_users_query)
        execute_and_print(conn, insert_users_query)
        execute_and_print(conn, select_all_users_query)
        
        # executemany
        conn.execute(text(insert_user_query), [
            {'id': 4, 'name': 'Simran'},
            {'id': 5, 'name': 'Shivangi'},
            {'id': 6, 'name': 'Priyanshu'},
        ])
        execute_and_print(conn, select_all_users_query)
        # conn.commit()
    
    # AUTOCOMMITING
    # requires engine.begin() instead of engine.connect()
    # treats connect block as a TRANSACTION
    # way: begin once
    with engine.begin() as conn:
        select_all_users_query = "select * from users"
        insert_user_query = """
        insert into users (id, name) values (:id, :name)
        """

        execute_and_print(conn, select_all_users_query)        
        conn.execute(text(insert_user_query), [
            {'id': 4, 'name': 'Simran'},
            {'id': 5, 'name': 'Shivangi'},
            {'id': 6, 'name': 'Priyanshu'},
        ])
        rows = execute_and_print(conn, select_all_users_query)
        # conn.commit()     # not needed as a engine.begin block not a engine.connect block
        
        # Result.all()
        logger.info('Result.all()')
        logger.debug(rows)
        
        # tuple assignment
        logger.info('tuple assignment')
        for id, name in rows:
            logger.debug((id, name))
        
        # as integer index
        rows = execute_and_print(conn, select_all_users_query)
        logger.info('as integer index')
        for row in rows:
            logger.debug((row[0], row[1]))
    
        # as attributes of named tuples
        rows = execute_and_print(conn, select_all_users_query)
        logger.info('as named tuples')
        for user in rows:
            logger.debug((user.id, user.name))
        
        # as Mapping Access
        rows = execute_and_print(conn, select_all_users_query)
        logger.info('Mapping Access')
        for user_dict in rows.mappings():
            logger.debug((user_dict['id'], user_dict['name']))
    
        # Sending Parameters
        logger.info('Sending Parameters')
        result = conn.execute(text('select * from users where id=:id'), {'id': 4})
        for user in result:
            logger.debug(user)
        
    # Sending Multiple Parameters: executemany
    # For statements DML statements such as “INSERT”, “UPDATE” and “DELETE”,
    # we can send multiple parameter sets to the Connection.execute() method by passing
    # a list of dictionaries instead of a single dictionary,
    # which indicates that the single SQL statement should be invoked multiple times,
    # once for each parameter set. 
    logger.info('Sending multiple parameters: executemany')
    with engine.connect() as conn:
        res = conn.execute(
            text('insert into users(id, name) values (:id, :name)'),
            [
                {'id': 7, 'name': 'Vijay'},
                {'id': 8, 'name': 'Shubham'},
                {'id': 9, 'name': 'Ankit'},
            ]
        )
        conn.commit()
        for user in conn.execute(text('select * from users')):
            logger.debug(user)

    # Executing with an ORM Session
    # The fundamental transactional / database interactive object when using the ORM is 
    # called the Session. 
    # In modern SQLAlchemy, this object is used in a manner very similar to that of the Connection, 
    # and in fact as the Session is used, it refers to a Connection internally which it uses to emit SQL.
    # The Session has a few different creational patterns
    # Also, like the Connection, the Session features “commit as you go” behavior
    # using the Session.commit() method.
    logger.debug('Executing with an ORM Session')
    with Session(engine) as session:
        session.execute(text('update users set name="UnknownUser" where id > :id'), {'id': 7})
        users = session.execute(text('select * from users'))
        logger.info('within session')
        for user in users:
            logger.debug(user)
        session.commit()
        
    logger.info('outside session')
    # update user won't persist unless we do a session.commit() before ending the session / with block
    users = session.execute(text('select * from users'))
    for user in users:
        logger.debug(user)


if __name__ == '__main__':
    main()