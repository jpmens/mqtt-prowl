#!/usr/bin/env python

# Copyright (C) 2013, Jan-Piet Mens <jpmens()gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import mosquitto
import sys, time
from ConfigParser import SafeConfigParser

# prowlpy is from https://github.com/jacobb/prowlpy
try:
    from prowlpy import prowlpy
except ImportError:
    import prowlpy

def config(inifile):
    cf = SafeConfigParser()
    cf.read(inifile)

    return cf

def on_connect(mosq, userdata, rc):
    print "Connected"
    for topic in userdata['topics']:
        print "Subscribing to " + topic
        mqttc.subscribe(topic, 0)

def on_message(mosq, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    prowl = userdata['prowl']
    cf = userdata['cf']
    application = cf.get('prowl', 'application')

    try:
        prowl.post(application,
            event=str(msg.topic),
            description=str(msg.payload),
            priority=0, url=None)
    except Exception, msg:
        print msg


def on_subscribe(mosq, userdata, mid, granted_qos):
    pass

def on_disconnect(mosq, userdata, rc):
    print "OOOOPS! disconnect"
    time.sleep(10)


cf = config('mqtt-prowl.ini')

topics = []
for key, topic in cf.items('topics'):
    topics.append(topic)

apikey = cf.get('prowl', 'apikey')

userdata = {
    'cf' : cf,
    'prowl' : prowlpy.Prowl(apikey),
    'topics' : topics,
}

mqttc = mosquitto.Mosquitto(userdata=userdata)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe

mqttc.will_set('clients/mqtt-growl', payload="Adios!", qos=0, retain=False)

mqttc.connect(cf.get('mqtt', 'broker'), cf.getint('mqtt', 'port'), 60)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    sys.exit(0)

