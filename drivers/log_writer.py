import os 
from datetime import date

def log_message(log_name, err=None):
    dir_name = '../logs'
    today = date.today().isoformat()
    if os.path.exists(dir_name):
        f = open(dir_name + '/%s.txt' % (log_name), 'w')
        if err:
            f.write('%s:%s process unsuccessful! error:%s', (log_name, today, err)) 
        else:
            f.write('%s:%s process successful!' % (log_name, today))

        f.close()
        print "processing done!"
