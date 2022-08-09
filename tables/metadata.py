from sqlalchemy import Column, Integer, Boolean, Float
from .const import Base

class Metadata(Base):
    __tablename__ = 'metadata'

    metadata_id = Column(Integer, primary_key=True)
    tagged = Column(Boolean)
    camera_fov = Column(Float)
    azimuth = Column(Float)
    elevation = Column(Float)