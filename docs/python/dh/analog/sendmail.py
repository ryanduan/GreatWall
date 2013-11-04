#!/usr/bin/python
#-*- coding: utf-8 -*-
# Author: Ryan 2013-10-24
# Update: 2013-11-04

from readlog import Readlog, analysislog, Writelog
from datetime import datetime as dt
from connectsmtp import Connectsmtp as connect

# This is the absolute path of the log file
logpath = "/var/log/whereis/your.log"

# This is the program logfile
mylogs = ''

# Start
mylogs += "\n%s Start to analysis your log \n" % dt.now()
logconts = Readlog(logpath)
if logconts:
    mylogs += '\t%s Successful to read and analysis logs\n' % dt.now()
    ntime, ninfo, nwarn, nerror, errors = analysislog(logconts)
    longerror = ''.join(errors)
    msglog = "\t%s\nINFO:%s\nWARNING:%s\nERROR:%s\n" % (ntime, ninfo, nwarn, nerror)
    consmtp = connect()
    if consmtp:
        mylogs += "\t%s Successful to connect and login gmail server\n" % dt.now()
        dhlog = "yourlog%s.txt" % dt.now().date()
        if consmtp.sendit(msglog, longerror, dhlog):
            mylogs += "\t%s Successful to send mail to tech\n" % dt.now()
        else:
            mylogs += "\t%s Fail to send mail\n" % dt.now()
    else:
        mylogs += "\t%s Fail to connect and login gmail server \n" % dt.now()
else:
    mylogs += "\t%s Fial to read and analysis log\n" % dt.now()

# write the program log
wlog = Writelog()
wlog.writeit(mylogs)
