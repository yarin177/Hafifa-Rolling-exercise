from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .const import BASE

class Videos(BASE):
    __tablename__ = 'videos'

    os_video_path = Column(String, primary_key=True)
    view_name = Column(String)
    frame_count = Column(Integer)
    frames = relationship('Frames', backref='videos')