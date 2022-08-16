from ast import Return
from sqlalchemy import Column, Integer, Boolean, Float, true
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

    def already_exists(self,metadatas):
        """
        Checks if a Metadata object with the same values already exists in a list.

        Args:
            metadatas: A list of Metadata()

        Returns:
            The metadata_id(Int) of the found object, or -999 if a simillar object
            was not found.
        """
        
        for metadata in metadatas:
            if self.tagged == metadata.tagged and self.camera_fov == metadata.camera_fov and self.azimuth == metadata.azimuth and self.elevation == metadata.elevation:
                return metadata.metadata_id
        return -999