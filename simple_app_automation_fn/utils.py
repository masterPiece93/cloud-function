from flask import request
from database import *

# Utils
class Utils:
    
    @staticmethod
    def get_notifications():
        messages = DBUtils.get_messages()
        nofication_messages=messages[request.path][request.method].copy()
        messages[request.path][request.method].clear()
        DBUtils.set_messages(messages)
        return nofication_messages
    
    @staticmethod
    def set_notifications(path, method, message):
        messages = DBUtils.get_messages()
        messages[path][method] += [message]
        DBUtils.set_messages(messages)
