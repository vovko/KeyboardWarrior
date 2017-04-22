import os

path_to_file = '/home/vovko/PycharmProjects/KeyboardWarrior/keylogger/log/keys.log'

while True:
    print(os.stat(path_to_file).st_mtime)