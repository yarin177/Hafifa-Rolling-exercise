from sqlalchemy import create_engine
# local imports
from tables.videos import Videos
from tables.metadata import Metadata
from tables.frames import Frames
from tables.const import Base

engine = create_engine("postgresql://postgres:postgrespw@localhost:55000")
table_objects = [Videos.__table__, Metadata.__table__, Frames.__table__]
Base.metadata.create_all(engine, tables=table_objects)