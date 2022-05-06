from sqlalchemy import Table, Column, Integer, String, ForeignKey, Index
from assetTracker.database import Base
import datetime
#Datetime is probably the best bet for creating events that are time based.
#https://docs.python.org/3/library/datetime.html

#A tag system might be useful to properly sort everything, but the biggest effective search method
#Is for names, names of area, and such.
#A balance of what human interaction is needed to make searching smooth must be found.
#Also make sure html escaping is used to prevent injection stuff purposeful or otherwise.

#For the tag system, using successive for loops to replicate multiple AND statements would work best.
#Furthermore, organizing tags by rarity and searching for the most rare first and then searching that list
#for the next rarest tag would run the fastest. 

class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    tag_id = Column(String)
    tag_tid = Column(String)
    name = Column(String)
    description = Column(String)
    
    current_area = Column(ForeignKey('area.id'))
    last_reader = Column(ForeignKey('reader.id'))
    
    col1 = Column(ForeignKey('reader.id'))
    col2 = Column(ForeignKey('reader.id'))
    col3 = Column(ForeignKey('reader.id'))
    col4 = Column(ForeignKey('reader.id'))
    col5 = Column(ForeignKey('reader.id'))
    reader_log = Index('col1', 'col2', 'col3', 'col4', 'col5')
    
    def __repr__(self):
        return f"Asset(id={self.id!r}, name={self.name!r})"
    
class Reader(Base):
    __tablename__ = 'reader'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    area_1_id = Column(ForeignKey('area.id'), nullable=False)
    area_2_id = Column(ForeignKey('area.id'), nullable=False)

    def __repr__(self):
        return f"Reader(id={self.id!r}, name={self.name!r}, area_1_id={self.area_1_id!r}, area_2_id={self.area_2_id!r})"

class Area(Base):
    __tablename__ = 'area'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Area(id={self.id!r}, name={self.name!r})"