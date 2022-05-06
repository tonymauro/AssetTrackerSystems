# AssetTrackerSystems
This to be further updated. 
This project uses Flask and SQLAlchemy to attempt to create the website and server side portions of the Asset Tracker System.

There are code comments litter about the code that give insight, some older than others. The code comments in drs-asset-tracking are more current, and contain plans and instructions on ideas of how best to go about things I haven't done yet. 

The folder within that folder that contains files that will be directly used in the final project is the drs-asset-tracking one, which is a flask app that is working towards being the website DRS asked for. The folder assetTracker within it is where all the code is store pretty much, the other directories are more for website operation, except for Tests, which is for tests. Not that I've used it for tests because I skipped that part of the tutorial. 

Flask is a more advanced framework for making websites with a natural integration of sql databases. 
SQLAlchemy is a tool for manipulating databases that will make you life easier in the long run. 

Database Stuff's databasev1TESTPERMA.py, while not in use directly, has had much of its code cut and paste into models.py and dbCommands.py, but much also hasn't and modified bits of it may be needed to make the program do everything it needs to. 

Before continuing with our work, first doing the SQLAlchemy and Flask tutorials will grant you the understanding of the two things that you need to easily understand what the code is doing, trying to do, and supposed to be doing. 

https://flask.palletsprojects.com/en/2.1.x/ 
From here you can find the installation instructions and tutorial. All other flask resources can also be found here. 

https://docs.sqlalchemy.org/en/20/tutorial/index.html
This is the tutorial directly for alchemy. They also have incredibly detailed documentation that can explain things with enough patience.

https://flask.palletsprojects.com/en/2.1.x/patterns/sqlalchemy/ 
In addition, this final bit of documentation on how to integrate alchemy and flask is very important. I used the stuff under "Declarative" 

