import sys
import requests
import json
import socket
import re
import irc

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


x = irc.irc()
x.connect()
x.login("ChromaBot", "8", "Herena", "Python socket RAW IRC BOT")

buffer = b""
while True:
    buffer += x.IRC.recv(2048)
    while b"\r\n" in buffer:
        line_data, buffer = buffer.split(b"\r\n", 1)
        ld = decode(line_data)
        re_line = irc_line_re.match(ld)
        data = ld.split()
        print(re_line.groups())
        if re_line is None:
            continue

        prefix, command, params, content_raw = re_line.groups()

        if command == "PING":
            if content_raw:
                ping_text = ":" + content_raw
                #           else:
                #               ping_text = command_params[0]
            x.send_data("PONG %s" % ping_text)
        elif command == "004":
            print("Join")
            x.join("#chromatic")
