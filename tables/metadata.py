from sqlalchemy import Column, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from .const import BASE

class Metadata(BASE):
    __tablename__ = 'metadata'

    metadata_id = Column(Integer, primary_key=True)
    tagged = Column(Boolean)
    camera_fov = Column(Float)
    azimuth = Column(Float)
    elevation = Column(Float)
    frames = relationship('Frames', backref='metadata')