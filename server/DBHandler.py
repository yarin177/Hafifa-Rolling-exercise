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

    def add_metadatas(self,metadatas):
        metas_to_frames = {}
        for metadata in metadatas:
            #add counter here 
            fov, azimuth, elevation = metadata[0]
            is_tagged = metadata[1]
            meta = Metadata(tagged=is_tagged, camera_fov=fov, azimuth=azimuth, elevation=elevation)
            if meta in metas_to_frames:
                metas_to_frames['']
            self.session.add(meta)
            metas.append(meta)

        self.session.commit()
        return metas
    
    def add_frames(self,metadatas,frame_paths,os_video_path):
        for index, (frame_path,metadata) in enumerate(zip(frame_paths,metadatas)):
            fr = Frames(os_frame_path=frame_path, os_video_path=os_video_path, frame_index=index,metadata_id=metadata.metadata_id)
            self.session.add(fr)

        self.session.commit()

