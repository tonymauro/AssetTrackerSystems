import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///test", echo=False, future=True)
#dialect+driver://username:password@host:port/database
#for sqlite because it is local it's just dialect+driver:///database
#note that this will create a db file called test if it doesn't already exist, with thonny it created it in Downloads
#That might just be because that's where this file was when I ran it though
#Not totally sure the created file actually knows it is a database but also not sure that matters cause of sqlAlchemy's
#connection method
#Also, since this connection connects locally only, the way the website would work would be that the server also hosts the
#database and executes these commands. It seems with connecting via host@port for stuff other than sqlite can connect to the
#database over the internet directly, which probably runs faster overall. Since we're running it through flask it might
#already be that all these commands are executed on the server and it doesn't matter anyway as the database will only be directly
#accessed from the server host
#UPDATE: It also seems that flask has a similar database routing system, so maybe the reason that the group picked this pair of
#programs was because they interact well? Either that or using them both is redundant. 
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import MetaData
metadata_obj = MetaData()
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Index
#I've imported some stuff I might not be using but I might use it eventually. 

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
    
from sqlalchemy import select

from sqlalchemy import insert

from sqlalchemy import subquery

from sqlalchemy import update

def addArea(areaName):
    with engine.connect() as conn:
        conn.execute(insert(area_table).values(name= areaName))
        conn.commit()
        print(areaName + " added to database.")


#THIS COMMAND MAY BE INCOMPLETE DO NOT USE!
#UPDATE, I'm about 80% sure this thing works fine, pretty sure I used it to add a reader, haven't seen this code in bit
#trying to figure out how it all works again.
def addReader(firstAreaId, secondAreaId):
    with engine.connect() as conn:
        result1 = -1
        result2 = -1
        for row in conn.execute(select(area_table.c.id).where(area_table.c.id == firstAreaId)):
            result1 = row[0]
        for row in conn.execute(select(area_table.c.id).where(area_table.c.id == secondAreaId)):
            result2 = row[0]
            
        if result1 != -1 and result2 != -1:
            
            for row in conn.execute(select(area_table.c.name).where(area_table.c.id == firstAreaId)):
                r1Name = row[0]
            for row in conn.execute(select(area_table.c.name).where(area_table.c.id == secondAreaId)):
                r2Name = row[0]
            
            readerName = (r1Name + "/" + r2Name)
            stmt = insert(reader_table).values(name = readerName, area_1_id = result1, area_2_id = result2)
            conn.execute(stmt)
            conn.commit()
            print("A reader connecting " + r1Name + " and " + r2Name + " has been added.")
            
        else:
            print("Invalid area id(s) entered.")
    
def addAsset(assetName, currentArea):
    #print("This does nothing right now")
    #Gonna want to make this SIGNIFIGANTLY more customizable, but probably on a higher level of abstraction than this script
    with engine.connect() as conn:
        conn.execute(insert(asset_table).values(name= assetName, current_area= currentArea))
        conn.commit()


#for manipulating the reader_log index during moveArea:
def cycleArea(AssetId, ReaderId):
    print("This does nothing right now")

def moveArea(AssetId, ReaderId):
    #precondition, asset has non-null location. TO DO: FIX THIS
    #precondition, asset has location valid to reader. TO DO: FIX THIS
    #TO DO: See if I can cut this down to size even further. It still looks super unwieldly and there seems to be a fair bit that could
    #be subqueries instead. 
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
        #Not sure if you have to intialize like this but that changing scope thing always makes me nervous
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
            print("Valid Reader")
            lconn.execute(update(asset_table).where(asset_table.c.id == AssetId).
                values(
                    current_area= select(readerArea).scalar_subquery(),
                    last_reader=ReaderId
                )
            )
            #these are just placeholder names that should be easy to recognize as an error if they come up. 
            assetName = "PLACEHOLDER_REPLACE_FAILURE"
            startRoomName = "PLACEHOLDER_REPLACE_FAILURE"
            endRoomName = "PLACEHOLDER_REPLACE_FAILURE"
            for lrow in lconn.execute(select(asset_table.c.name).where(asset_table.c.id == AssetId)):
                assetName = lrow[0]
            for lrow in lconn.execute(select(area_table.c.name).where(area_table.c.id == rL1)):
                if startArea == 1:
                    startRoomName = lrow[0] #row 0 is the names
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
            print("\nReader does not map directly to current believed location, attmept to move unsuccessful unless otherwise stated\n")
            LastReaderId = "THIS SHOULD BE A NUMBER"
            for lrow in lconn.execute(select(asset_table.c.last_reader).where(asset_table.c.id == AssetId)):
                LastReaderId = lrow[0]
            for lrow in lconn.execute(select(reader_table).where(reader_table.c.id == LastReaderId)):
                print(lrow)
            areaIds = [-1,-1,-1,-1]
            #there is a way to use a join or something to assign all 4 ids in a single execute but I'm not sure how quite yet
            #New Reader's ids first, Last Reader's ids second,  (0,1) (2,3)
            #at the very least the different reader ids could be loaded into a list and looped through
            for lrow in lconn.execute(select(reader_table.c.area_1_id).where(reader_table.c.id == ReaderId)):
                areaIds[0] = lrow[0]
            for lrow in lconn.execute(select(reader_table.c.area_2_id).where(reader_table.c.id == ReaderId)):
                areaIds[1] = lrow[0]
            for lrow in lconn.execute(select(reader_table.c.area_1_id).where(reader_table.c.id == LastReaderId)):
                areaIds[2] = lrow[0]
            for lrow in lconn.execute(select(reader_table.c.area_2_id).where(reader_table.c.id == LastReaderId)):
                areaIds[3] = lrow[0]
            
            firstArea = False
            secondArea = False
            if areaIds[0] == areaIds[2] or areaIds[0] == areaIds[3]:
                firstArea = True
            if (areaIds[1] == areaIds[2]) or (areaIds[0] == areaIds[3]):
                secondArea = True
            if firstArea and secondArea:
                print("\nLocation still unknown, both reader have same area pair \n")
            elif firstArea:
                print("placeholder")
            
                #convert the validReader function above into a subfunction or something and put it here.
                #Maybe add some prints to each after it to clarify area find method
            elif secondArea:
                print("placeholder")
            if not validReader:
                print("\nReaders almost certainly not connected, unknown physical or code error/problem\n")
            
            
        lconn.commit()

def returnAssets():
    stmt = select(asset_table.c.id, asset_table.c.tag_id, asset_table.c.tag_tid,
                  asset_table.c.name, asset_table.c.current_area,
                  asset_table.c.last_reader, asset_table.c.description)
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

def returnAll():
    returnAssets()
    returnReaders()
    returnAreas()

print("Connection might be established correctly. This message doesn't actually know anything.")