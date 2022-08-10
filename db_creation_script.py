from sqlalchemy import create_engine
# local imports
from tables.videos import Videos
from tables.metadata import Metadata
from tables.frames import Frames
from tables.const import BASE

engine = create_engine("postgresql://postgres:postgrespw@localhost:55000")
BASE.metadata.create_all(engine)