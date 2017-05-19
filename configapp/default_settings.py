import os
DEBUG = True
PROPAGATE_EXCEPTIONS = True
KEY = '\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16'
SECRET_KEY = os.environ.get('SECRET_KEY', KEY)
HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
IMAGE_PATH = 'test_images/'
IMAGE_SUFFIX = '.png'
DATASET_PATH = '../../test_data'
IMAGES_TO_PREDICT_PATH = '../../test_data'
MASK_PATH = '../../masks'
PREDICTION_PATH = '../../predictions'
