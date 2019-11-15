import os

from flask import Flask

def create_app(test_config=None):
    # This function creates and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.mssql'),
    )

    # Configuration file
    if test_config is None:
        # Load configuration file if not passed.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load configuratin file if passed
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    
    return app