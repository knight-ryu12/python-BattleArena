import sys
import requests
import json
import socket
import re
import irc

irc_line_re = re.compile(r"^(?::(\S+)\s)?(\S+)(?:\s(?!:)(.+?))?(?:\s:(.+))?$")
file = open("config.json", 'r')
config_json = json.load(file)
file.close()

def decode(bytestring):
    for codec in ('utf-8', 'iso-8859-1', 'shift_jis', 'cp1252', 'cp932'):
        try:
            return bytestring.decode(codec)
        except UnicodeDecodeError:
            continue
    return bytestring.decode('utf8', errors='ignore')

print("Welcome to Battle Arena Bot version 0.1 written by Chromaryu, Original is James \"Iyouboushi\"")
print(config_json)
if config_json != 1:
    try:
        print("The bot admin list is currently set to: %s" % config_json['botowner'])
    except KeyError:
        print("*** WARNING: There is no bot admin set. Please fix this now.")
        botowner = input("Please enter the bot admin's IRC nick:")
        config_json['botowner'] = botowner
        file = open("config.json",'w')
        file.write(json.dumps(config_json))
        file.close()
    try:
        print("The battle channel is currently set to: %s" % config_json['battle_channel'])
    except KeyError:
        print("*** WARNING: There is no battle channel set. Please fix this now.")
        battlechannel = input("Please enter the IRC channel you're using (include the #):")
        config_json['battle_channel'] = battlechannel
        file = open("config.json",'w')
        file.write(json.dumps(config_json))
        file.close()

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
            x.join("##ldtest")
