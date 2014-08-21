# coding=utf-8

#Auxiliar model for obtaining users with their associated role
class UserEventRelation(object):
    def __init__(self, user=None, role=''):
        self.user = user
        self.role = role


