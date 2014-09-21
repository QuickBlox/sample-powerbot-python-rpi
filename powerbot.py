#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    PowerBot: a chat bot that controls power sockets.
    (C) 2014 Taras Filatov, QuickBlox
    Chat bot based on the code from SleekXMPP project by Nathanael C. Fritz. (C) 2010 modified by Taras Filatov and Igor Khomenko.
    Energenie power sockets control code (C) Energenie and MiniGirlGeek: https://github.com/MiniGirlGeek/energenie-demo
    
    Distributed under Apache 2.0 open source license. See the file LICENSE for copying permission including bundled 3rd party codes.
"""



import sys
import logging
import getpass
import os
from optparse import OptionParser
import sleekxmpp
from sleekxmpp.xmlstream import ET
import subprocess
from energenie import switch_on, switch_off

"""
   IMPORTANT: for MUC auto-join to work, change these to your own script path and QuickBlox credentials.
   Also make sure you made this script executable (chmod -x testbot.py).
"""

selfPath = os.path.realpath(__file__)
qbAppID = "14628"
qbUserID = "1612594"
qbUserPass = "niichavo"

qbChatLogin = qbUserID + "-" + qbAppID + "@chat.quickblox.com"
qbChatNick = qbUserID

user_jid = qbChatLogin
user_password = qbUserPass
room_jid = "14628_541f4ab3535c124866028b17@muc.chat.quickblox.com"
room_nick = qbChatNick

counter = 0

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class MUCBot(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will greet those
    who enter the room, and acknowledge any messages
    that mention the bot's nickname.
    """

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)
        
        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

        # The groupchat_presence event is triggered whenever a
        # presence stanza is received from any chat room, including
        # any presences you send yourself. To limit event handling
        # to a single room, use the events muc::room@server::presence,
        # muc::room@server::got_online, or muc::room@server::got_offline.
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)


    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        #self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        maxhistory="1",
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    def message(self, msg):
        """
        [ 1:1 CHATS. In this section we handle private (1:1) chat messages received by our bot. These may include system messages such as MUC invitations. ]
        """
        
        """
        1:1 message test auto-reply
        Uncomment the code lines below to make chat bot reply to any incoming 1:1 chat messages by quoting them
        """
        
        """
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
        """
        
        """
        MUC auto-join:
        Let's listen for any MUC invites and join the corresponding MUC rooms once invited.
        """
        
        """if msg['mucnick'] != self.nick and "created a group" in msg['body']:"""
        if msg['mucnick'] != self.nick and "Create new chat" in msg['body']:
            from bs4 import BeautifulSoup
            y = BeautifulSoup(str(msg))
            roomToJoin = y.xmpp_room_jid.string
            print ("Got an invite to join room")
            """os.system(selfPath + " -d -j " + qbChatLogin + " -r " + str(roomToJoin) + " -n " + qbChatNick + " -p " + qbUserPass)"""
            """subprocess.call(selfPath + " -d -j " + qbChatLogin + " -r " + str(roomToJoin) + " -n " + qbChatNick + " -p " + qbUserPass, shell=True)"""
            botId = subprocess.Popen([selfPath + " -d -j " + qbChatLogin + " -r " + str(roomToJoin) + " -n " + qbChatNick + " -p " + qbUserPass], shell=True)
            print "spawned new bot ID="
            print botId
    
            self.send_message(mto=msg['from'].bare,
                          mbody="Thank you for your kind invitation, joining your new room now!",
                          mtype='groupchat')



    def muc_message(self, msg):
        """
        [ MUC CHATS. In this section we handle messages from MUC (multi-user chat rooms) our bot participates in. ]
        """
        
        #
        # Ignore messages from offline storage, track only real time messages
        #
        delay_element  = msg.xml.find('{urn:xmpp:delay}delay')
        if delay_element is not None:
            return

        #
        # Reply to help request (any message containing "powerbot" in it)
        #
        if msg['mucnick'] != self.nick and "powerbot" in msg['body']:

            reply_test_message = self.make_message(mto=msg['from'].bare,
                      mbody="Powerbot is greeting you, %s! Usage: [powerbot] lamp [on|off] to control socket 1, [powerbot] all [on:off] to control all sockets. Example: 'lamp on' switched socket 1 on." % msg['mucnick'],
                      mtype='groupchat')
            self.copy_dialog_id(msg, reply_test_message)
            reply_test_message.send()
            print "Sent help text: " + str(reply_test_message)

        #
        # Handle "lamp on" command
        #
        if msg['mucnick'] != self.nick and "lamp on" in msg['body']:
            
            switch_on(lampSocket)
            confirmation_message = self.make_message(mto=msg['from'].bare,
                                                   mbody="Lamp has been switched on, %s." % msg['mucnick'],
                                                   mtype='groupchat')
            self.copy_dialog_id(msg, confirmation_message)
            confirmation_message.send()
            print "Lamp switched on, sent confirmation: " + str(confirmation_message)


        #
        # Handle "lamp off" command
        #
        if msg['mucnick'] != self.nick and "lamp off" in msg['body']:
            
            switch_off(lampSocket)
            confirmation_message = self.make_message(mto=msg['from'].bare,
                                                     mbody="Lamp has been switched off, %s." % msg['mucnick'],
                                                     mtype='groupchat')
            self.copy_dialog_id(msg, confirmation_message)
            confirmation_message.send()
            print "Lamp switched off, sent confirmation: " + str(confirmation_message)


        #
        # Handle "all on" command
        #
        if msg['mucnick'] != self.nick and "all on" in msg['body']:
            
            switch_off(lampSocket)
            confirmation_message = self.make_message(mto=msg['from'].bare,
                                                     mbody="All sockets have been switched on, %s." % msg['mucnick'],
                                                     mtype='groupchat')
            self.copy_dialog_id(msg, confirmation_message)
            confirmation_message.send()
            print "All sockets switched on, sent confirmation: " + str(confirmation_message)


        #
        # Handle "all off" command
        #
        if msg['mucnick'] != self.nick and "all off" in msg['body']:
            
            switch_off(lampSocket)
            confirmation_message = self.make_message(mto=msg['from'].bare,
                                                     mbody="All sockets have been switched off, %s." % msg['mucnick'],
                                                     mtype='groupchat')
            self.copy_dialog_id(msg, confirmation_message)
            confirmation_message.send()
            print "All sockets switched off, sent confirmation: " + str(confirmation_message)



    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')


    def copy_dialog_id(self, origin_message, new_message):
        """
        Copy a dialog_id from a received message to a replay message
        """
        dialog_id_in = origin_message.xml.find('{jabber:client}extraParams/{jabber:client}dialog_id')

        if dialog_id_in is not None:
            extra_params_out = ET.Element('{jabber:client}extraParams')
            dialog_id_out = ET.Element('{}dialog_id')
            dialog_id_out.text = dialog_id_in.text
            extra_params_out.append(dialog_id_out)
            new_message.append(extra_params_out)


if __name__ == '__main__':

    try:
        from local_settings import *
    except ImportError:
        print "No custom config found, use default settings"
    else:
        print "Use custom settings"


    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is not None:
        user_jid = opts.jid
    if user_jid is None:
        user_jid = raw_input("Username: ")

    if opts.password is not None:
        user_password = opts.password
    if user_password is None:
        user_password = getpass.getpass("Password: ")

    if opts.room is not None:
        room_jid = opts.room
    if room_jid is None:
        room_jid = raw_input("MUC room: ")

    if opts.nick is not None:
        room_nick = opts.nick
    if room_nick is None:
        room_nick = raw_input("MUC nickname: ")

    print "initial jid: " + user_jid
    print "initial password: " + user_password
    print "initial room: " + room_jid
    print "initial nick: " + room_nick

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot(user_jid, user_password, room_jid, room_nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
