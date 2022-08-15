from sqlalchemy import create_engine
# local imports
from server.tables.videos import Videos
from server.tables.metadata import Metadata
from server.tables.frames import Frames
from server.tables.const import BASE

engine = create_engine("postgresql://postgres:postgrespw@localhost:55000")
#engine = create_engine("sqlite:///tempdb.db")
BASE.metadata.create_all(engine)