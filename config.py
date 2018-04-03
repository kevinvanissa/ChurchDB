import os

basedir = os.path.abspath(os.path.dirname(__file__))

SERVER_BASE="http://localhost"
UPLOAD_FOLDER = basedir+'/app/static/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

CRSF_ENABLED = True
SECRET_KEY= 'fsfsfafasfN?*sfsdf'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
