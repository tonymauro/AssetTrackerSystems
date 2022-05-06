#this currently in development, may not work or may possibly break things if you attempt to run it

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///assetDB", echo=False, future=True)
from sqlalchemy.orm import Session
from sqlalchemy import text, MetaData, Table, Column, Integer, String, ForeignKey, Index
metadata_obj = MetaData()

area_table = Table(
  "area",
  metadata_obj,
  Column('id', Integer, primary_key=True),
  Column('name', String)
  #TO-DO: Set up column that is a list of readers if possible.
)

reader_table = Table(
  "reader",
  metadata_obj,
  Column('id', Integer, primary_key=True),
  Column('name', String),
  Column('area_1_id', ForeignKey('area.id'), nullable=False),
  Column('area_2_id', ForeignKey('area.id'), nullable=False)
)

asset_table = Table(
  "asset",
  metadata_obj,
  Column('id', Integer, primary_key=True),
  Column('tag_id', String),
  Column('tag_tid', String),
  Column('name', String),
  Column('current_area', ForeignKey('area.id')),
  Column('last_reader', ForeignKey('reader.id')),
  Column('description', String),
  
  Column('col1', ForeignKey('reader.id')),
  Column('col2', ForeignKey('reader.id')),
  Column('col3', ForeignKey('reader.id')),
  Column('col4', ForeignKey('reader.id')),
  Column('col5', ForeignKey('reader.id')),
  Index('reader_log', 'col1', 'col2', 'col3', 'col4', 'col5')
)

metadata_obj.create_all(engine)

from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy.orm import relationship

#If you're using an IDE, you'll get an error saying something like Variable "databasev1TESTPERMA.Base"
#is not valid as a type. That's just sqlAlchemy being difficult for IDEs to understand,
#and it's working fine. The other error on the same line that says Invalid base class "Base" is also fine.
#there are tons of false errors like this that will pop up, you'll have to learn which ones they are
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
        return f"Reader(id={self.id!r}, name={self.name!r})"

class Area(Base):
    __tablename__ = 'area'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)


