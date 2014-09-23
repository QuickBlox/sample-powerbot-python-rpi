sample-powerbot-python-rpi
==========================

QuickBlox PowerBot. Allows to control power sockets via chat. In current implementation Energenie RF controlled power sockets are used along with Q-municate chat app by QuickBlox, chat bot running on Raspberry Pi model B.

<b>Usage</b><br />
powerbot.py -d -r &lt;QuickBlox MUC room to join&gt;
<br />
Example: powerbot.py -d -r 14628_541f4ab3535c124866028b17@muc.chat.quickblox.com

<b>Dependencies</b><br />
You may need to run these under root to install the missing packages on your Pi:<br />
apt-get install python-dev<br />
pip install sleekxmpp<br />
pip install dnspython<br />
pip install pyasn1 pyasn1-modules<br />



