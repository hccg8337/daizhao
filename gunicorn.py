import multiprocessing


bind = '0.0.0.0:8000'

reload = False

workers = multiprocessing.cpu_count()

loglevel = 'info'

capture_output = True

accesslog = '-'

errorlog = '-'

timeout = 300

preload_app = True
