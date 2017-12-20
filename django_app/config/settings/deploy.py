# debug.py
# base.py에 있는 값을 불러옴 import *로 무조건 설정할것
from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

WSGI_APPLICATION = 'config.wsgi.deploy.application'

# aws server,s3 settings
AWS_ACCESS_KEY_ID = config_secret_deploy['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_deploy['aws']['secret_access_key']


# Static URLs
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')

# media URLs
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

DATABASES = config_secret_deploy['django']['databases']

INSTALLED_APPS += [
    # add your deploy apps

]

DEBUG = True
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']