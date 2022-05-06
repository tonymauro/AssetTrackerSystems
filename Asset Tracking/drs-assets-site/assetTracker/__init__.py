import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'assetTracker.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from assetTracker.database import db_session
    
    from . import database
    database.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')
    
    #Not currently properly functioning:
    from . import tracker
    app.register_blueprint(tracker.bp)
    #app.add_url_rule('/tracker/', endpoint='tracker/index')
    
        
    return app

