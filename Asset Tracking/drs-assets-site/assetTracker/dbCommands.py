from sqlalchemy import Table, Column, Integer, String, ForeignKey, Index
from sqlalchemy import select, insert, subquery, update
from assetTracker.database import Base
from assetTracker import models
from assetTracker.models import Asset, Reader, Area
from sqlalchemy.orm import Session


#Currently to delete the database and its data just go to drs-assets-site/instance and delete it manually.
def constructTestObjects(impSession):
    
    with impSession() as conn:
        conn.execute(insert(Area).values(name= 'closetA'))
        conn.execute(insert(Area).values(name= 'hallwayA'))
        conn.execute(insert(Area).values(name= 'warehouseA'))
        conn.commit()

    with impSession() as conn:
        result = conn.execute(
            insert(Asset).
            values(name= 'tiger', current_area= select(Area.id).where(Area.id == int(2)).scalar_subquery(), description= 'the big orange cat')
        )
        conn.commit()
        
    with impSession() as conn:
        result = conn.execute(
            insert(Reader).
            values(name= 'closetA/hallwayA', area_1_id= select(Area.id).where(Area.id == int(1)).scalar_subquery(), area_2_id= select(Area.id).where(Area.id == int(2)).scalar_subquery())
        )
        conn.commit()
    with impSession() as conn:
        result = conn.execute(
            insert(Reader).
            values(name= 'hallwayA/warehouseA', area_1_id= select(Area.id).where(Area.id == int(2)).scalar_subquery(), area_2_id= select(Area.id).where(Area.id == int(3)).scalar_subquery())
        )
        conn.commit()


def printAssets(impSession):
    stmt = select(Asset.id, Asset.tag_id, Asset.tag_tid,
                  Asset.name, Asset.current_area,
                  Asset.last_reader, Asset.description)
    print(stmt)
    with impSession() as conn:
        for row in conn.execute(stmt):
            print(row)
            
#These next two are NOT returning every columun in each Reader or Area, instead they are just returning their
# __repr__(self). This is different from using a connection where it would do that, with a session this is the
#default
#def returnReaders(impSession):
#    stmt = select(Reader)
#    print(stmt)
#    with impSession() as conn:
#        for row in conn.execute(stmt):
#            print(row)
#
#def returnAreas(impSession):
#    stmt = select(Area)
#    print(stmt)
#    with impSession() as conn:
#        for row in conn.execute(stmt):
#            print(row)

#These should correctly return them as I use them
#Each of the 'rows' itself contains seperate rows of all the columns in the object that was selected

def printReaders(impSession):
    stmt = select(Reader.id, Reader.name, Reader.area_1_id, Reader.area_2_id)
    print(stmt)
    with impSession() as conn:
        for row in conn.execute(stmt):
            print(row)

def printAreas(impSession):
    stmt = select(Area.id, Area.name)
    print(stmt)
    with impSession() as conn:
        for row in conn.execute(stmt):
            print(row)            

def printAll(impSession):
    printAssets(impSession)
    printReaders(impSession)
    printAreas(impSession)
    print("That should have just printed all assets, readers, and areas and all their data.")
    
def returnAssets():
    stmt = select(Asset.id, Asset.tag_id, Asset.tag_tid, Asset.name, Asset.current_area, Asset.last_reader, Asset.description)
    return stmt
# Id: 0, Tag Id: 1, Tag True Id: 2, Name: 3, Current Area: 4, Last Reader: 5, Description: 6

def returnReaders():
    stmt = select(Reader.id, Reader.name, Reader.area_1_id, Reader.area_2_id)
    return stmt

def returnAreas():
    stmt = select(Area.id, Area.name)
    return stmt




#These below this are imported functions from databasev1TESTPERMA and probably don't work and might even stop the
#whole program from working

def addArea(areaName, impSession):
    with impSession() as conn:
        conn.execute(insert(Area).values(name= areaName))
        conn.commit()
        print(areaName + " added to database.")


#THIS COMMAND MAY BE INCOMPLETE DO NOT USE!
#UPDATE, I'm about 80% sure this thing works fine, pretty sure I used it to add a reader, haven't seen this code in bit
#trying to figure out how it all works again.
def addReader(firstAreaId, secondAreaId, impSession):
    with impSession() as conn:
        result1 = -1
        result2 = -1
        for row in conn.execute(select(Area.id).where(Area.id == firstAreaId)):
            result1 = row[0]
        for row in conn.execute(select(Area.id).where(Area.id == secondAreaId)):
            result2 = row[0]
            
        if result1 != -1 and result2 != -1:
            
            for row in conn.execute(select(Area.name).where(Area.id == firstAreaId)):
                r1Name = row[0]
            for row in conn.execute(select(Area.name).where(Area.id == secondAreaId)):
                r2Name = row[0]
            
            readerName = (r1Name + "/" + r2Name)
            stmt = insert(Reader).values(name = readerName, area_1_id = result1, area_2_id = result2)
            conn.execute(stmt)
            conn.commit()
            print("A reader connecting " + r1Name + " and " + r2Name + " has been added.")
            
        else:
            print("Invalid area id(s) entered.")
    
def addAsset(assetName, currentArea, impSession):
    #print("This does nothing right now")
    #Gonna want to make this SIGNIFIGANTLY more customizable, but probably on a higher level of abstraction than this script
    with impSession() as conn:
        conn.execute(insert(Asset).values(name= assetName, current_area= currentArea))
        conn.commit()