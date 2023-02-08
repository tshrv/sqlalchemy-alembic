"""
This is the project entrypoint, brining together the UserModel and UserService
"""
from sqlalchemy import create_engine, text
from loguru import logger


def main():
    """Project Entrypoint"""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    with engine.connect() as conn:        
        result = conn.execute(text("select 'hello world'"))
        print(result)
        print(result.all())
        # as there is no conn.commit(), once the set of instructions end, ROLLBACK is triggered

if __name__ == '__main__':
    main()