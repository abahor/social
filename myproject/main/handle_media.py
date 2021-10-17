import string
from random import *

from flask import current_app


def handle(data):
    ext = data.filename.split('.')[-1]
    character = string.digits + string.ascii_letters
    while True:
        try:
            x = "".join(choice(character) for x in range(randint(1, 2)))
            # if os.path.isfile(current_app.root_path + '/static/media/' + x + secure_filename(data.filename)):

            path = '/protected/' + str(x) + '.' + ext
            data.save(current_app.root_path + path)
            if True:
                break
        except:
            pass
    images = ['png', 'jpg', 'gif']
    ges = ['mp4', 'mkv']
    if ext.lower() in images:
        m = 'b'
    elif ext.lower() in ges:
        m = 'v'
    if True:
        return [str(x) + '.' + ext, m]
    # for i in data:
    #     names += ' ' + secure_filename(i.filename)
    # return names