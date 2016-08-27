import sys
import requests
import json
import socket
import re

irc_line_re = re.compile(r"^(?::(\S+)\s)?(\S+)(?:\s(?!:)(.+?))?(?:\s:(.+))?$")
file = open("config.json", 'r')
config_json = json.load(file)


def decode(bytestring):
    for codec in ('utf-8', 'iso-8859-1', 'shift_jis', 'cp1252', 'cp932'):
        try:
            return bytestring.decode(codec)
        except UnicodeDecodeError:
            continue
    return bytestring.decode('utf8', errors='ignore')


class irc:
    def __init__(self):
        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.IRC.connect((config_json['server_address'], config_json['server_port']))

    def send_data(self, command):
        self.IRC.send((command + '\r\n').encode())
        print((command + '\r\n').encode())

    def join(self, channel):
        self.send_data("JOIN %s" % channel)

    def send_msg(self, channel, msg):
        self.send_data(("PRIVMSG %s :%s" % (channel, msg)))

    def get_user(self, channel):
        self.send_data(("WHO %s" % channel))

    def login(self, nickname, mode, hostname, realname):
        self.send_data(("USER %s %s %s :%s" % (nickname, mode, hostname, realname)))
        self.send_data(("NICK %s" % nickname))
