#!/usr/bin/python3
# -*- coding:utf-8 -*-


class opstores_log:
    time = ""
    system = ""
    thread = ""
    level = ""
    logger = ""
    file = ""
    content = ""

    def __init__(self, array):
        self.time = array[0]
        self.system = array[1]
        self.thread = array[2]
        self.level = array[3]
        self.logger = array[4]
        self.file = array[5]
        self.content = array[6]
