#! /usr/bin/env python3
#
# Load a pattern into a class and do transforms on it
#

import yaml
import math
import logging

class Pattern:
    def __init__(self, fn:str, logger:logging.Logger) -> None:
        self.fn = fn
        self.logger = logger
        self.qRotate = False
        self.vertices = None
        self.__loadPattern()

    def __repr__(self) -> str:
        return "qRotate={}, vertices={}".format(self.qRotate, self.vertices)
        
    def __loadPattern(self) -> None:
        ''' Load a YAML pattern file, then normalize and rotate it '''
        try:
            with open(self.fn, 'r') as fp:
                info = yaml.load(fp)
                self.qRotate = info['qRotate'] if 'qRotate' in info else False
                self.__mkPattern(info)
        except:
            self.logger.exception('Error loading %s', self.fn)

    def __mkPattern(self, info:dict) -> None:
        ''' Transform info into a pattern, scaled and rotated '''

        if 'polygon' not in info:
            raise Exception('No polygon in {}'.format(self.fn))

        print(info)
        polygon = info['polygon']

        if not isinstance(polygon, list):
            raise Exception('Polygon in {} is not a list, {}'.format(self.fn, polygon))

        if len(polygon) < 2:
            raise Exception('Polygon in {} must have at least two points, {}'.format(
                self.fn, polygon))

        if len(polygon) > 7:
            raise Exception('Polygon in {} has more than 7 points, {}'.format(
                self.fn, polygon))

        
        norm = info['normalization'] if 'normalization' in info else None
        theta = info['rotation_angle'] if 'rotation_angle' in info else None

        norm  = 1 if norm  is None else norm
        theta = 0 if theta is None else theta

        if norm == 0:
            raise Exception('Normalization in {} is zero'.format(self.fn))

        vertices = []

        theta = math.radians(theta)
        stheta = math.sin(theta)
        ctheta = math.cos(theta)

        for vertex in polygon:
            if not isinstance(vertex, list):
                raise Exception('Polygon vertices in {} are not all lists, {}'.format(
                    self.fn, polygon))
            if len(vertex) != 2:
                raise Exception('Polygon vertices in {} are not of length 2, {}'.format(
                    self.fn, polygon))
            (x, y) = vertex
            if not isinstance(x, (int, float)):
                raise Exception('x({}) is not a number in polygon vertices in {}, {}'.format(
                    x, self.fn, polygon))
            if not isinstance(y, (int, float)):
                raise Exception('y({}) is not a number in polygon vertices in {}, {}'.format(
                    y, self.fn, polygon))
            if norm != 1: # Scale vertices if needed
                x *= norm
                y *= norm
            if theta != 0: # Rotate vertices
                xx = x * ctheta - y * stheta
                yy = x * stheta + y * ctheta
                vertices.append((xx, yy))
            else:
                vertices.append((x, y))

        self.vertices = vertices
                

if __name__ == "__main__":
    import sys

    logging.basicConfig()

    for fn in sys.argv[1:]:
        a = Pattern(fn, logging)
        print(a)
