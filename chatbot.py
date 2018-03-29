'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests

MY_USERNAME = 'muchmoonies'
MY_CLIENT_ID = 'kc9tgri2pcv7tw7w2dz4umxjkrz4xi'
MY_OAUTH_TOKEN = 'ygmjzcl623ubwv2pjt2hcd8khu44g4'
CHANNEL = 'muchmoonies'

NUTCOIN_COMMANDS = ['nutcoins', 'top', 'bet', 'gamble', 'hrs']
SONG_COMMANDS = ['song', 'songrequest', 'sr', 'songlist', 'skip', 'wrongsong', 'ws']
LINKS_COMMANDS = ['discord', 'snapchat', 'twitter', 'youtube',  'sub']
INFO_COMMANDS = ['howtobet', 'changes', 'subday', 'specs', 'giveaway', 'followage']
GAME_COMMANDS = ['battletag', 'battlenet', 'wowserver', 'rank', 'rankof']
FUN_COMMANDS = ['gender', 'defcon', 'defcon1', 'defcon2', 'ban', 'slap', '8ball']
REMOVED_COMMANDS = ['shadowed', 'pubg', 'highlight', 'tshirt']
BUSTIN_COMMANDS = NUTCOIN_COMMANDS + SONG_COMMANDS + LINKS_COMMANDS + INFO_COMMANDS + GAME_COMMANDS + FUN_COMMANDS + REMOVED_COMMANDS


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # TODO test api calls
        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print 'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def on_welcome(self, c, e):


        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')

        print 'Joining ' + self.channel
        c.join(self.channel)
        print 'Successfully connected!'

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd.lower() not in BUSTIN_COMMANDS:
                print 'Received command: ' + cmd
                cmd = cmd.lower()
                self.do_command(e, cmd)

        return

    # TODO add recognization for @mentiona
    # TODO recognize the sender for responses
    # TODO implement a timer for command cooldowns

    def do_command(self, e, cmd):
        c = self.connection

        if cmd in BUSTIN_COMMANDS:
            message = ''
            # ignore, nutmod will take care of it

        # Poll the API to get current game.
        elif cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # spam 46 nutsquads
        elif cmd == "nutsquad":
            message = ''
            for i in range(45):
                message += 'nutSquad '
            message += 'nutSquad'
            print 'sending ' + cmd
            c.privmsg(self.channel, message)
        elif cmd == "test":
            message = "Test1"
            print 'sending ' + message
            c.privmsg(self.channel, message)
        elif cmd == 'nuttest':
            message = 'nutSquad'
            print 'sending' + message
            c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            print "ERROR, the following command was unrecognized: " + cmd


def main():
    if len(sys.argv) != 1:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit('arguments = ' + str(len(sys.argv)))

    # TODO remove redundancies
    username = MY_USERNAME
    client_id = MY_CLIENT_ID
    token = MY_OAUTH_TOKEN
    channel = CHANNEL

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()


if __name__ == "__main__":
    main()
