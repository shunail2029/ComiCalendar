import datetime


def log(message):
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    ms = message.strip('\n').split('\n')
    with open('log.txt', mode='a') as f:
        for m in ms:
            f.write('[' + str(now) + '] ' + m + '\n')
