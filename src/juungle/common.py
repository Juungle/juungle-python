"""Common module"""
import os.path
import configparser

config = configparser.ConfigParser()
# if os.path.isfile('user-config.py'):
config.read('user-config.ini')
# else:
#     sys.exit('Please create user-config.ini')

LOGIN_USERNAME = config['DEFAULT']['LOGIN_USERNAME']
LOGIN_PASSWORD = config['DEFAULT']['LOGIN_PASSWORD']
