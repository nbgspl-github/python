# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# from paradigmatic.app.v1.core import config
#
# engine = create_engine(
#     config.SQLALCHEMY_DATABASE_URI,
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()

# Dependency
def get_db():
    pass
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
