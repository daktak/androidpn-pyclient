#!/usr/bin/env python3
import os,sys
import urllib
import configparser
import optparse
from urllib import request
output = []

def returnVal(one, two):
    if one is not None:
        if (one != ""):
            return one
    else:
        return two


def fix_str(news, replace):
    for j in range(0,len(replace)):
        news = news.replace("${"+str(j+1)+"}", replace[j])
    return news;

def config(configfile, replace=None):
    config = configparser.RawConfigParser()
    config.read(configfile)
    out= {}
    out['url'] = config.get('AndroidPN','url')
    out['broadcast'] = config.get('AndroidPN','broadcast')
    out['username'] = config.get('AndroidPN','username')
    return out

def opt():
    parser = optparse.OptionParser()
    parser.add_option('-i', help='Config file for default values', dest='configfile')
    parser.add_option('-r', help='Parse additional args to scripts', dest='replace')
    parser.add_option('-u', help='AndroidPN Server URL', dest='url')
    parser.add_option('-n', help='If directed to a specific user, username', dest='username')
    parser.add_option('-b', help='Broadcast Y/N', dest='broadcast')
    parser.add_option('-t', help='Message title', dest='title')
    parser.add_option('-m', help='Message body', dest='message')
    parser.add_option('-l', help='Message URI', dest='uri')
    (opts, args) = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = opt()
    if opts.configfile is not None:
        configfile=opts.configfile
    else:
        configfile='/etc/androidpn/androidpn.ini'
    cfg = config(configfile)

    try:
       print ('Notifying via AndroidPN')
       #curl --data "title=test&message=eu&action=send&broadcast=Y&uri=" http://192.168.1.10:7071/notification.do
       data = urllib.parse.urlencode({
       'title': opts.title.encode('utf-8'),
       'message': opts.message.encode('utf-8'),
       'action': "send",
       'broadcast': returnVal(opts.broadcast, cfg['broadcast']),
       'uri': opts.uri,
       'username': returnVal(opts.username, cfg['username']) 
       })
       data = data.encode('utf-8')
       req = urllib.request.Request(returnVal(opts.url, cfg['url']))
       handle = urllib.request.urlopen(req, data)
       handle.close()
    except  urllib.error.URLError as e:
      print ('Error sending AndroidPN Notification: %s' % e)

