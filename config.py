import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1837196166539923',
        'secret': 'b686b5a304e204587536042acc1fc566'
     },
    'twitter': {
        'id': '5AX8vQD41aF7btSPLJkIiuJKd',
        'secret': 'aQNQRQsPfRD3Fpz0pSgwiwyftlOZWp22b5alipQzeCakxXLM3t'
    }
}

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
