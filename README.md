sample-powerbot-python-rpi
==========================

QuickBlox PowerBot.<br />
Allows to control power sockets via chat. In current implementation <a href="https://energenie4u.co.uk/index.php/catalogue/product/ENER314">Energenie RF controlled power sockets</a> are used along with <a href="http://q-municate.com/">Q-municate open source IM / chat app</a> by QuickBlox, this chat bot running on Raspberry Pi model B.

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



