from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# local imports
from tables.videos import Videos
from tables.metadata import Metadata
from tables.frames import Frames
from tables.const import BASE

class DBHandler:
    def __init__(self):
        engine = create_engine("postgresql://postgres:postgrespw@host.docker.internal:55000")
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_video(self, os_video_path, view_name, frame_count):
        video = Videos(os_video_path=os_video_path,view_name=view_name,frame_count=frame_count)
        self.session.add(video)
        self.session.commit()

    def add_metadatas(self,metadatas):
        """
        This function iterates over a list of Metadata(),
        Assigning every Metadata to its Frames and adds
        the Metadata() to the Database.

        Args:
            metadatas: A list of Metadata()

        Returns:
            metas_to_frames(dict) a dictonary containing each metadata_id
            and its frames_index
            Example: {metadata_id : [frame_index]}
        """
        metas_to_frames = {}
        old_metadatas = []
        for frame_index, metadata in enumerate(metadatas):
            fov, azimuth, elevation = metadata[0]
            is_tagged = metadata[1]
            meta = Metadata(tagged=is_tagged, camera_fov=fov, azimuth=azimuth, elevation=elevation)
            found_id = meta.already_exists(old_metadatas)

            if found_id != -999:
                metas_to_frames[found_id].append(frame_index)
            else:
                self.session.add(meta)
                self.session.commit()
                metas_to_frames[meta.metadata_id] = [frame_index]
                old_metadatas.append(meta)

        return metas_to_frames
    
    def add_frames(self,metas_to_frames,frames_folder_path,os_video_path):
        """
        This function iterates over a dictonary and updates it in the Database.
        Every frame in the dictonary is assigned to its metadata_key.

        Args:
            metas_to_frames(dict): A dictonary of Metadata() to Frames()
            frames_folder_path(str): OS path location of the frames video' folder
            os_video_path(str): OS path location of the video
        """

        index_counter = 0
        for metadataID in metas_to_frames:
            frames_index = metas_to_frames[metadataID]
            for index in frames_index:
                fr = Frames(os_frame_path=f"{frames_folder_path}/{index_counter}.png", os_video_path=os_video_path, frame_index=index,metadata_id=metadataID)
                self.session.add(fr)
                index_counter += 1

        self.session.commit()