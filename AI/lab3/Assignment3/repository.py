# -*- coding: utf-8 -*-

from domain import *


class repository():
    def __init__(self, Map):
        self.__map = Map

    def getMap(self):
        return self.__map

