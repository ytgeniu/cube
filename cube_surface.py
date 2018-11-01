#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def minus(self, other):
        ret = Point()
        ret.x = self.x - other.x
        ret.y = self.y - other.y
        ret.z = self.z - other.z
        return ret
    def multiply(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

	
default_surfase = ((1, 1), (-1, 1), (-1, -1), (1, -1))

class Cube_Surfase:
    def __init__( self, surfase_index = 0, length = 0.5, pos_index = [0, 0], rank = 1):
        self.m_surfase_index = surfase_index
        self.m_length = length
        self.m_pos_index = pos_index
        self.m_pointlist  = []
        self.m_isSelected = False
        if (1 == rank):
            interval = 0
        else:
            interval = 0.01
        global default_surfase
        for p in default_surfase:
            if (0 == surfase_index):
                 ponit = Point((p[0] + pos_index[0] * 2) * length - p[0] * interval, (p[1] + pos_index[1] * 2) * length - p[1] * interval, length * rank)
            elif (1 == surfase_index):
                 ponit = Point((p[0] + pos_index[0] * 2) * length - p[0] * interval, (p[1] + pos_index[1] * 2) * length - p[1] * interval, -length * rank)
            elif (2 == surfase_index):
                 ponit = Point((p[0] + pos_index[0] * 2) * length - p[0] * interval, length * rank, (p[1] + pos_index[1] * 2) * length - p[1] * interval)
            elif (3 == surfase_index):
                 ponit = Point((p[0] + pos_index[0] * 2) * length - p[0] * interval, -length * rank, (p[1] + pos_index[1] * 2) * length - p[1] * interval)
            elif (4 == surfase_index):
                 ponit = Point(length * rank, (p[0] + pos_index[0] * 2) * length - p[0] * interval, (p[1] + pos_index[1] * 2) * length - p[1] * interval)
            elif (5 == surfase_index):
                 ponit = Point(-length * rank, (p[0] + pos_index[0] * 2) * length - p[0] * interval, (p[1] + pos_index[1] * 2) * length - p[1] * interval)
            else:
                print("surfase_index error")
            self.m_pointlist.append(ponit)