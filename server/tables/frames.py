from sqlalchemy import Column, ForeignKey, Integer, String
from .const import BASE

class Frames(BASE):
    __tablename__ = 'frames'

    os_frame_path = Column(String, primary_key=True)
    os_video_path = Column(String, ForeignKey("videos.os_video_path"))
    frame_index = Column(Integer)
    metadata_id = Column(Integer, ForeignKey("metadata.metadata_id"))