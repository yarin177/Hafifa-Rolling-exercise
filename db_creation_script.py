from sqlalchemy import create_engine
# local imports
from tables.const import BASE

engine = create_engine("postgresql://postgres:postgrespw@localhost:55000")
BASE.metadata.__videos__.drop()
#BASE.metadata.create_all(engine)