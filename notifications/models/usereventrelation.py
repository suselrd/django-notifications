# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

#Auxiliar model for obtaining users with their associated role


class UserEventRelation(object):
    def __init__(self, user=None, role=''):
        self.user = user
        self.role = role


