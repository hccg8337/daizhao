import os
import sys


if __name__ == '__main__':
    argv = sys.argv
    if not os.path.exists('logs'):
        os.mkdir('logs')
    os.system('python manage.py migrate')
    if argv[1] == 'service':
        os.system('gunicorn -c gunicorn.py daizhao.wsgi')
