#! /usr/bin/env python3
#
# Glider position, through water speed, and depth averaged current 
# from the glider's dialog

import logging
from datetime import datetime, timedelta
import re

class Glider():
    def __init__(self):
        self.qComplete = True
        self.glider = None
        self.t = None
        self.timestamp = None
        self.lat = None
        self.lon = None
        self.tLatLon = None
        self.speed = None
        self.vx = None
        self.vy = None
        self.tVX = None
        self.tVY = None
        self.__reGlider = re.compile(r"Vehicle Name:\s(\w+)")
        self.__reT = re.compile(r"Curr Time:\s+\w+\s+(\w+\s+\d+\s+\d+:\d+:\d+\s+\d+)\s+MT:\s+\d+")
        self.__reLatLon = re.compile(
                r"GPS Location:\s+([+-]?\d+[.]\d+)\s+[NS]\s+([+-]?\d+[.]\d+)\s+[EW]\s+measured\s+(\d+[.]\d+)\s+secs ago")
        self.__reVX = re.compile(
                r"sensor:m_final_water_vx[(]m/s[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
        self.__reVY = re.compile(
                r"sensor:m_final_water_vy[(]m/s[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
        self.__reSpeed = re.compile(r"m_avg_speed[(]m/s[)]\s+([+-]?\d+[.]\d+)")
        self.__reComplete = re.compile(r"Water Velocity Calculations COMPLETE")

    def __repr__(self) -> str:
        items = []
        items.append("glider: {}".format(self.glider))
        items.append("t: {} {}".format(self.t, self.timestamp))
        items.append("lat: {}".format(self.lat))
        items.append("lon: {}".format(self.lon))
        items.append("tLatLon: {}".format(self.tLatLon))
        items.append("speed: {}".format(self.speed))
        items.append("vx: {} {}".format(self.vx, self.tVX))
        items.append("vy: {} {}".format(self.vy, self.tVY))
        return "\n".join(items)

    def parse(self, line) -> None:
        self.timestamp = datetime.now() # Now
        self.qComplete = False
        line = line.strip()
        a = self.__reGlider.fullmatch(line)
        if a is not None:
            self.glider = a[1]
            return
        a = self.__reT.fullmatch(line)
        if a is not None:
            self.t = datetime.strptime(a[1], "%b %d %H:%M:%S %Y")
            return
        a = self.__reLatLon.fullmatch(line)
        if a is not None:
            self.lat = float(a[1])
            self.lon = float(a[2])
            self.tLatLon = self.t - timedelta(seconds=float(a[3]))
            return
        a = self.__reVX.fullmatch(line)
        if a is not None:
            self.vx = float(a[1])
            self.tVX = self.t - timedelta(seconds=float(a[2]))
            return
        a = self.__reVY.fullmatch(line)
        if a is not None:
            self.vy = float(a[1])
            self.tVY = self.t - timedelta(seconds=float(a[2]))
            return
        a = self.__reSpeed.fullmatch(line)
        if a is not None:
            self.speed = float(a[1])
            return
        a = self.__reComplete.fullmatch(line)
        if a is not None:
            self.qComplete = True
            return

if __name__ == "__main__":
    import sys

    for fn in sys.argv[1:]:
        with open(fn, 'r') as fp:
            gld = Glider()
            for line in fp:
                gld.parse(line)
            print(gld)
