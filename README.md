# MQTT Scroller for the Pimoroni Stellar Unicon with Pi Pico W

MQTT Scroller and Laser Cut Front for the 
[Pimoroni Stellar Unicon with Pi Pico W](https://shop.pimoroni.com/products/space-unicorns?variant=40842632953939)

This is an edited version of the Pimoroni Text Scroll to connect to Wifi and subscribe to an MQTT feed, enabling messages to be scrolled via any MQTT broker. 

The code is set up around our THE: Time, Headlines and Envivronmental Information stream, this links in feeds from our own MQTT server, providing details on the time, news, weather and earthquake information. You can choose to leave this in place (good for a first test) or add your own MQTT feed. The code uses different coloured backgrounds for different text in feeds - ie News, Weather, Time, you can edit these accordingly to match your own feed. Our feed updates every couple of minutes, for a constant stream of information.

![Screen](https://github.com/ucl-casa-ce/Stellar-Unicorn-MQTT-Scroller/blob/main/StellarUnicornMQTT.png)

Copy all the files to your Stellar Unicon using Thonny - edit config.py to add your Wifi and MQTT broker credentials.

![Case](https://www.digitalurban.org/wp-content/uploads/2023/08/StellarParts.jpg)

## The Case

Three files are provided to laser cut:

1) The laser cut front as pictured with Etching (THE: Time, Headlines, Environmental)
2) The laser cut front, minus text
3) Front cut for the clear acrylic

Created as part of work at the [Connected Environments Group at the Centre for Advanced Spatial Analysis](https://connected-environments.org/), University College London.
