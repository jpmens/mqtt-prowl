
# MQTT-PROWL

Subscribes to any number of MQTT topics and notifies via [Prowl](http://www.prowlapp.com/).

Configuration is expected in the `mqtt-prowl.ini` file (a sample template is
provided, which has to be renamed):

```ini
[prowl]
apikey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
application=MQTT

[mqtt]
broker=localhost
port=1883

[topics]
topic1 = test/one
topic2 = twitter/emergency
topic3 = jp/#
```

You can specify any number of topics in the `[topics]` section; the key name
is ignored.

`mqtt-prowl` connect to the specified MQTT broker and subscribes to the list
of topics. For each message received on a topic, `mqtt-prowl` will notify
your Prowl device.

**Note**: there are limits on the number of Prowl notifications you may issue,
and additional cost may be involved; check the Prowl documentation and ask your
carrier.

Publish a test message to your broker, specifying one of the topics `mqtt-prowl` is
subscribed to:

```
mosquitto_pub -t test/one -m 'Introducing mqtt-prowl. :-)'
```

After a few seconds, you should see the result in your Prowl app:

![prowl.png]

## Requires

* A [Prowl](http://www.prowlapp.com/) account and API key
* [prowlpy](https://github.com/jacobb/prowlpy)
* The [Mosquitto Python](http://mosquitto.org/documentation/python/) module
* Access to an MQTT broker
