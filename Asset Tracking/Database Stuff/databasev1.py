import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
#dialect+driver://username:password@host:port/database
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import MetaData
metadata_obj = MetaData()
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey

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
  Column('description', String)
)


metadata_obj.create_all(engine)

from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy.orm import relationship

class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    tag_id = Column(String)
    tag_tid = Column(String)
    name = Column(String)
    description = Column(String)
    
    current_area = Column(ForeignKey('area.id'))
    last_reader = Column(ForeignKey('reader.id'))

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
    
from sqlalchemy import select

from sqlalchemy import insert
with engine.connect() as conn:
    result = conn.execute(
        insert(area_table),
        [
            {"name": "closetA"},
            {"name": "hallwayA"},
            {"name": "warehouseA"}
        ]
    )
    conn.commit()

from sqlalchemy import subquery

with engine.connect() as conn:
    result = conn.execute(
        insert(asset_table).
        values(name= 'tiger', current_area= select(area_table.c.id).where(area_table.c.id == '2').scalar_subquery(), description= 'the big orange cat')
    )
    conn.commit()
    
with engine.connect() as conn:
    result = conn.execute(
        insert(reader_table).
        values(name= 'closetA/hallwayA', area_1_id= select(area_table.c.id).where(area_table.c.id == '1').scalar_subquery(), area_2_id= select(area_table.c.id).where(area_table.c.id == '2'))
    )
    conn.commit()
with engine.connect() as conn:
    result = conn.execute(
        insert(reader_table).
        values(name= 'hallwayA/warehouseA', area_1_id= select(area_table.c.id).where(area_table.c.id == '2').scalar_subquery(), area_2_id= select(area_table.c.id).where(area_table.c.id == '3'))
    )
    conn.commit()

from sqlalchemy import update


def moveArea(AssetId, ReaderId):
    #precondition, asset has non-null location. TO DO: FIX THIS
    #precondition, asset has location valid to reader. TO DO: FIX THIS
    with engine.connect() as lconn:
        validReader = False #this is a way to establish a framework for when the code can catch errors
        cAID = int(0)
        rL1 = int(0)
        rL2 = int(0)
        for lrow in lconn.execute(select(asset_table.c.current_area).where(asset_table.c.id == AssetId)):
            cAID = lrow[0]
        for lrow in lconn.execute(select(reader_table.c.area_1_id).where(reader_table.c.id == ReaderId)):
            rL1 = lrow[0]
        for lrow in lconn.execute(select(reader_table.c.area_2_id).where(reader_table.c.id == ReaderId)):
            rL2 = lrow[0]
        print("\n\nTHE IDS SHOULD BE HERE:")
        print(cAID)
        print(rL1)
        print(rL2)
        
        #Initializing readerArea and startArea
        startArea = 1
        lstmt = select(reader_table.c.area_2_id)
        readerArea = lstmt.subquery()
        print(readerArea)
        
        #Determining which switch to make
        if cAID == rL1:
            validReader = True
            print("Equal to rL1")
            lstmt = select(reader_table.c.area_2_id).where(reader_table.c.id == ReaderId)
            readerArea = lstmt.subquery()
            startArea = 1
            
        if cAID == rL2:
            validReader = True
            print("Equal to rL2")
            lstmt = select(reader_table.c.area_1_id).where(reader_table.c.id == ReaderId)
            readerArea = lstmt.subquery()
            startArea = 2
        
        #Making the switch and outputting feedback
        if validReader:
            print("Placeholder")
            lconn.execute(update(asset_table).where(asset_table.c.id == AssetId).
                values(
                    current_area= select(readerArea).scalar_subquery(),
                    last_reader=ReaderId
                )
            )
            
            assetName = "to do"
            startRoomName = "to do"
            endRoomName = "to do"
            for lrow in lconn.execute(select(asset_table.c.name).where(asset_table.c.id == AssetId)):
                assetName = lrow[0]
            for lrow in lconn.execute(select(area_table.c.name).where(area_table.c.id == rL1)):
                if startArea == 1:
                    startRoomName = lrow[0]
                else:
                    endRoomName = lrow[0]
            for lrow in lconn.execute(select(area_table.c.name).where(area_table.c.id == rL2)):
                if startArea == 2:
                    startRoomName = lrow[0]
                else:
                    endRoomName = lrow[0]
            
            
            print("\n" + assetName + " moved from " + startRoomName + " to " + endRoomName + ".\n")
            
        #Current failsafe that outputs if things are invalid, will enventually include the routing logic
        else:
            print("\nReader was invalid\n")
        
        
        lconn.commit()

def returnAssets():
    stmt = select(asset_table)
    print(stmt)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)
        
def returnReaders():
    stmt = select(reader_table)
    print(stmt)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

def returnAreas():
    stmt = select(area_table)
    print(stmt)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)