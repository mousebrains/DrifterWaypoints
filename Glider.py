#! /usr/bin/env python3
#
# Read in a glider dialog and update glider table in the database
#
# July-2020, Pat Welch, pat@mousebrains.com

import logging
from datetime import datetime, timedelta
import re
import sqlite3
import argparse
import math

class Glider():
    def __init__(self, dbName:str, logger:logging.Logger) -> None:
        self.dbName = dbName
        self.logger = logger
        self.db = sqlite3.connect(dbName)
        self.glider = None
        self.tDialog = None
        self.__reGlider = re.compile(r"Vehicle Name:\s(\w+)")
        self.__reTDialog = re.compile(
                r"Curr Time:\s+\w+\s+(\w+\s+\d+\s+\d+:\d+:\d+\s+\d+)\s+MT:\s+\d+")
        self.__reLatLon = re.compile(
                r"GPS Location:\s+([+-]?\d+[.]\d+)\s+[NS]\s+([+-]?\d+[.]\d+)\s+[EW]\s+measured\s+(\d+[.]\d+)\s+secs ago")
        self.__reVX = re.compile(
                r"sensor:m_final_water_vx[(]m/s[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
        self.__reVY = re.compile(
                r"sensor:m_final_water_vy[(]m/s[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
        self.__reWptLat = re.compile(
                r"sensor:x_last_wpt_lat[(]lat[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
        self.__reWptLon = re.compile(
                r"sensor:x_last_wpt_lon[(]lon[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
        self.__reSensorSpeed = re.compile(
                r"sensor:m_avg_speed[(]m/s[)]=([+-]?\d+[.]\d+)\s+(\d+[.]\d+)\s+secs ago")
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

    def __glider(self, line:str) -> bool:
        a = self.__reGlider.fullmatch(line)
        if a is None: return False
        self.glider = a[1]
        return True

    def __tDialog(self, line:str) -> bool:
        a = self.__reTDialog.fullmatch(line)
        if a is None: return False
        self.tDialog = datetime.strptime(a[1], "%b %d %H:%M:%S %Y")
        return True

    def __dbInsert(self, tblName:str, names:tuple, vals:tuple) -> bool:
        items = ["name", "t"]
        items.extend(names)
        values = [self.glider]
        values.extend(vals)

        sql = "INSERT OR REPLACE INTO " + tblName + "(" + ",".join(items) + ") VALUES("
        sql+= ",".join(["?"] * len(items)) + ");"
        self.logger.debug("sql=%s vals=%s", sql, values)
        cur = self.db.cursor()
        cur.execute(sql, values)
        self.db.commit()
        return True

    @staticmethod
    def __mkDegrees(x:str) -> float:
        ''' deg*100 + minutes -> decimal degrees '''
        x = float(x)
        y = abs(x)
        deg = math.floor(y / 100)
        minutes = y % 100
        pm = 1 if x >= 0 else -1
        return pm * (deg + minutes / 60)

    def __latLon(self, line:str) -> bool:
        a = self.__reLatLon.fullmatch(line)
        if a is None: return False
        lat = self.__mkDegrees(a[1])
        lon = self.__mkDegrees(a[2])
        dt = timedelta(seconds=float(a[3]))
        return self.__dbInsert("gliderPos", ("lat", "lon"), (self.tDialog - dt, lat, lon))

    def __vel(self, line:str, pattern, tbl:str) -> bool:
        a = pattern.fullmatch(line);
        if a is None: return False
        v = float(a[1]);
        dt = timedelta(seconds=float(a[2]))
        return self.__dbInsert(tbl, ("v",) , (self.tDialog - dt, v))

    def __vx(self, line:str) -> bool:
        return self.__vel(line, self.__reVX, "gliderVX")

    def __vy(self, line:str) -> bool:
        return self.__vel(line, self.__reVY, "gliderVY")

    def __sensorSpeed(self, line:str) -> bool:
        return self.__vel(line, self.__reSensorSpeed, "gliderSpeed")

    def __wpt(self, line:str, pattern, tbl:str) -> bool:
        a = pattern.fullmatch(line)
        if a is None: return False
        x = self.__mkDegrees(a[1])
        dt = timedelta(seconds=float(a[2]))
        return self.__dbInsert(tbl, ("val",) , (self.tDialog - dt, x))

    def __wptLat(self, line:str) -> bool:
        return self.__wpt(line, self.__reWptLat, "gliderWptLat")

    def __wptLon(self, line:str) -> bool:
        return self.__wpt(line, self.__reWptLon, "gliderWptLon")

    def __speed(self, line:str) -> bool:
        a = self.__reSpeed.fullmatch(line)
        if a is None: return False
        spd = float(a[1])
        return self.__dbInsert("gliderSpeed", ("speed",) , (self.tDialog, spd))

    def __complete(self, line:str) -> bool:
        a = self.__reComplete.fullmatch(line)
        if a is None: return False
        print(line)
        return self.__dbInsert("gliderComplete", [], (datetime.now(),))

    def parse(self, line:str) -> None:
        line = line.strip()
        if self.__glider(line): return
        if self.__tDialog(line): return
        if self.__latLon(line): return
        if self.__vx(line): return
        if self.__vy(line): return
        if self.__wptLat(line): return
        if self.__wptLon(line): return
        if self.__sensorSpeed(line): return
        if self.__speed(line): return
        if self.__complete(line): return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse glider dialogs and store in a database')
    parser.add_argument('--db', type=str, metavar='filename', required=True,
            help='SQLite3 database name')
    parser.add_argument('--logger', type=str, metavar='filename', 
            help='Where to write log records to')
    parser.add_argument('--verbose', action='store_true', help='Enable debug messages')
    parser.add_argument('fn', nargs='+', metavar='logfiles', help='Glider dialog files')
    args = parser.parse_args()

    logger = logging
    logging.basicConfig(filename=args.logger,
            level=logging.DEBUG if args.verbose else logging.INFO)

    gld = Glider(args.db, logger)
    for fn in args.fn:
        with open(fn, 'r') as fp:
            for line in fp:
                gld.parse(line)
