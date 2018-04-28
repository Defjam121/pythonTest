#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Filename:          funktionenTest.py
# Author:            macbook
# Date:              2018-04-28
# Version:           1.0
###
##------------------------------------------------------------------------
##    Bib
##------------------------------------------------------------------------
import psutil
import subprocess
import os
import sys
import time
##------------------------------------------------------------------------
##    Variablen
##------------------------------------------------------------------------

##------------------------------------------------------------------------
##    Funktionen
##------------------------------------------------------------------------
def getTimeZone():
    return time.strftime("%Z", time.gmtime())


def getTimeNow():
    now = time.strftime('%a %b %d %H:%M:%S %Y %Z', time.localtime(time.time()))
    return now

def getLoadAverage():
    if linux:
        import multiprocessing
        k = 1.0
        k /= multiprocessing.cpu_count()
        if os.path.exists('/proc/loadavg'):
            return [float(open('/proc/loadavg').read().split()[x]) * k for x in range(3)]
        else:
            tokens = subprocess.check_output(['uptime']).split()
            return [float(x.strip(',')) * k for x in tokens[-3:]]
    if mswindows:
        # TODO(Guodong Ding) get this field data like on Linux for Windows
        # print psutil.cpu_percent()
        # print psutil.cpu_times_percent()
        # print psutil.cpu_times()
        # print psutil.cpu_stats()
        return "%.2f%%" % psutil.cpu_percent()


def getMemory():
    v = psutil.virtual_memory()
    return {
        'used': v.total - v.available,
        'free': v.available,
        'total': v.total,
        'percent': v.percent,
    }


def getVirtualMemory():
    v = psutil.swap_memory()
    return {
        'used': v.used,
        'free': v.free,
        'total': v.total,
        'percent': v.percent
    }


def getUptime():
    uptime_file = "/proc/uptime"
    if os.path.exists(uptime_file):
        with open(uptime_file, 'r') as f:
            return f.read().split(' ')[0].strip("\n")
    else:
        return time.time() - psutil.boot_time()


def getUptime2():
    boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
    print ("system start at: %s" % (boot_time))
    uptime_total_seconds = time.time() - psutil.boot_time()
    uptime_days = int(uptime_total_seconds / 24 / 60 / 60)
    uptime_hours = int(uptime_total_seconds / 60 / 60 % 24)
    uptime_minutes = int(uptime_total_seconds / 60 % 60)
    uptime_seconds = int(uptime_total_seconds % 60)
    print ("uptime: %d days %d hours %d minutes %d seconds" % (uptime_days, uptime_hours, uptime_minutes, uptime_seconds))

    user_number = len(psutil.users())
    print ("%d user:" % user_number)
    print ("  \\")
    for user_tuple in psutil.users():
        user_name = user_tuple[0]
        user_terminal = user_tuple[1]
        user_host = user_tuple[2]
        user_login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user_tuple[3]))
        print ("  |- user online: %s, login from %s with terminal %s at %s" % (
            user_name, user_host, user_terminal, user_login_time))

    cpu_count = psutil.cpu_count()
    try:
        with open('/proc/loadavg', 'r') as f:
            loadavg_c = f.read().split(' ')
            loadavg = dict()
            if loadavg_c is not None:
                loadavg['lavg_1'] = loadavg_c[0]
                loadavg['lavg_5'] = loadavg_c[1]
                loadavg['lavg_15'] = loadavg_c[2]
                loadavg['nr'] = loadavg_c[3]
                loadavg['last_pid'] = loadavg_c[4]
        print ("load average: %s, %s, %s" % (loadavg['lavg_1'], loadavg['lavg_5'], loadavg['lavg_15']))
        if float(loadavg['lavg_15']) > cpu_count:
            print ("Note: cpu 15 min load is high!")
        if float(loadavg['lavg_5']) > cpu_count:
            print ("Note: cpu 5 min load is high!")
        if float(loadavg['lavg_1']) > cpu_count:
            print ("Note: cpu 1 min load is high!")
    except IOError:
        pass
##------------------------------------------------------------------------
##    Main
##------------------------------------------------------------------------
timemin=int(float(getUptime()))
uptime_days = int(timemin / 24 / 60 / 60)
uptime_hours = int(timemin / 60 / 60 % 24)
uptime_minutes = int(timemin / 60 % 60)
uptime_seconds = int(timemin % 60)
print("UptimeDay %d UptimeHour %d UptimeMin %d" % (uptime_days, uptime_hours, uptime_minutes))
print(getTimeNow())