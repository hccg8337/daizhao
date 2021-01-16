import os
import sys


if __name__ == '__main__':
    argv = sys.argv
    for dirpath in ['logs', 'medias']:
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
    os.system('python manage.py migrate')
    if argv[1] == 'service':
        os.system('gunicorn -c gunicorn.py daizhao.wsgi')
