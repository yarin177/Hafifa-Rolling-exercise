from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# local imports
from tables.videos import Videos
from tables.metadata import Metadata
from tables.frames import Frames
from tables.const import BASE

class DBHandler:
    def __init__(self):
        engine = create_engine("sqlite:///../tempdb.db")
        Session = sessionmaker(bind=engine)

        self.session = Session()

    def add_video(self, os_video_path, view_name, frame_count):
        video = Videos(os_video_path=os_video_path,view_name=view_name,frame_count=frame_count)
        self.session.add(video)
        self.session.commit()

    def add_metadata(self,metadatas):
        for metadata in metadatas:
            fov, azimuth, elevation = metadata[0]
            is_tagged = metadata[1]
            #ID?