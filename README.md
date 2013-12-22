Engelsystembot
==============

This is a quick and dirty bot, that checks every time it is called if there are new subscribers to a certain shift-type and messages them once.

**Usage**

Rename the config.json.dist-file to config.json and adjust to your desired settings.

The values for the filters can be taken directly from the engel-system.

The parameter "sendmessagesto" can be omitted - however if it is present, all messages will be sent to this user instead to the respective angels. To "go live" and send messages to their destinations, just remove the line completly.

In order to track the angels that have already been contacted, the script will create a angels.json-file. If you want to start sending messages to your angels after haveing done some testing, you should also remove this file.
