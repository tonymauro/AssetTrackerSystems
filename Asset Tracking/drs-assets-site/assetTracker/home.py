from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from assetTracker.database import db_session

from assetTracker.dbCommands import (
    returnStringTest, addStringTest, clearStringTest
)

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    
    stringList = []
    count = 0
    stmt = returnStringTest()
    with db_session() as conn:
        for row in conn.execute(stmt):
            stringList.append(row)
            count += 1
    
    return render_template('home/index.html', stringList=stringList)

@bp.route('/doubleTest')
def doubleTest():
    addStringTest("Test String", db_session)
    return redirect(url_for('index'))

@bp.route('/clearStrings')
def clearStrings():
    clearStringTest(db_session)
    return redirect(url_for('index'))

@bp.route('/checkReader')
def checkReader():
    reader = mercury.Reader("")
    reader.set_region("NA2")
    reader.set_read_plan([1], "GEN2")
    stringName = str(reader.read())
    
    addStringTest(stringName, db_session)
    
    return redirect(url_for('index'))