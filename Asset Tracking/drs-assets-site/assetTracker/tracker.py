from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from assetTracker.database import db_session
from assetTracker.dbCommands import returnAssets
from assetTracker.models import Asset, Reader, Area

bp = Blueprint('tracker', __name__, url_prefix='/tracker')

@bp.route('/')
def index():
    #The best way to fully implement a sorting system would be to have the Alchemy
    #stmt be composed of several composite strings based on preferences that sort through all the tags and
    #stuff like that.
    #Would probably want to do some joining by default or something. 
    
    assetList = []
    count = 0
    stmt = returnAssets()
    with db_session() as conn:
        for row in conn.execute(stmt):
            assetList.append(row)
            count += 1
    
    return render_template('tracker/index.html', assetList=assetList)