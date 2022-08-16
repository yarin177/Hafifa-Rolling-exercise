from sqlalchemy import create_engine
# local imports
from server.tables.videos import Videos
from server.tables.metadata import Metadata
from server.tables.frames import Frames
from server.tables.const import BASE

engine = create_engine("postgresql://postgres:postgrespw@host.docker.internal:55000")
BASE.metadata.create_all(engine)