import re
import json
import struct
import socket
import requests


RESPONSE_TIMEOUT = 3
MAX_UDP_BUFFER_SIZE = 65535
CITRA_WEB_API_URL = 'https://api.citra-emu.org'


class GameServer:
    def __init__(self, host='localhost', port=2303, response_timeout=RESPONSE_TIMEOUT):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.response_timeout = response_timeout
        self.set_status_unknown()

    def set_status_unknown(self):
        self.name = 'Unknown'
        self.player_count = 0
        self.max_player_count = 0
        self.player_list = []
        self.is_online = False
    
    def update_status(self):
        raise NotImplementedError


class CitraServer(GameServer):
    def update_status(self):
        try:
            response = requests.get(f'{CITRA_WEB_API_URL}/lobby', timeout=self.response_timeout)
            data = json.loads(response.content)

            for room in data['rooms']:
                if room['address'] == self.host and room['port'] == self.port:
                    break
            else:
                raise RuntimeError
            
            self.name = room['name']
            self.player_count = len(room['players'])
            self.max_player_count = room['maxPlayers']
            self.player_list = []
            for player in room['players']:
                self.player_list.append({
                    'name': player['nickname'],
                    'game-name': player['gameName'] if player['gameName'] else 'Not playing'
                })
            self.is_online = True
        except (requests.exceptions.RequestException, ValueError, RuntimeError):
            self.set_status_unknown()


class SteamServer(GameServer):
    basic_info_request = 'ÿÿÿÿTSource Engine Query\0'.encode('iso-8859-1')
    player_info_request = 'ÿÿÿÿUÿÿÿÿ'.encode('iso-8859-1')
    player_info_challenge_prefix = 'ÿÿÿÿU'.encode('iso-8859-1')

    def __init__(self, host='localhost', port=2303, response_timeout=3):
        super().__init__(host, port, response_timeout)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.settimeout(response_timeout)
        self.link = f'steam://connect/{self.host}:{self.port}'

    def get_basic_info(self):
        self.client.sendto(self.basic_info_request, self.address)
        response, _ = self.client.recvfrom(MAX_UDP_BUFFER_SIZE)
        challenge = self.basic_info_request
        challenge += response[-4:]
        self.client.sendto(challenge, self.address)
        response, _ = self.client.recvfrom(MAX_UDP_BUFFER_SIZE)
        return response

    def get_player_info(self):
        self.client.sendto(self.player_info_request, self.address)
        response, _ = self.client.recvfrom(MAX_UDP_BUFFER_SIZE)
        challenge = self.player_info_challenge_prefix
        challenge += response[-4:]
        self.client.sendto(challenge, self.address)
        response, _ = self.client.recvfrom(MAX_UDP_BUFFER_SIZE)
        return response


class Arma3Server(SteamServer):
    basic_info_pattern = re.compile(b'.*?\x11(?P<name>.*?)\x00(?P<world>.*?)'
                                    b'\x00.*?\x00(?P<mission>.*?)\x00{3}'
                                    b'(?P<player_count>.)'
                                    b'(?P<max_player_count>.)')
    player_info_pattern = re.compile(b'\x00(?P<name>.*?)\x00(?P<score>.).{3}'
                                     b'(?P<time>.{4})')

    def set_status_unknown(self):
        self.world = 'Unknown'
        self.mission = 'Unknown'
        super().set_status_unknown()

    def update_status(self):
        self.player_list = []
        try:
            # Parse basic info
            response = self.get_basic_info()
            matches = self.basic_info_pattern.search(response)
            self.name = matches.group('name').decode('utf8', 'replace')
            self.world = matches.group('world').decode('utf8', 'replace')
            self.mission = matches.group('mission').decode('utf8', 'replace')
            self.player_count = int.from_bytes(matches.group('player_count'),
                                               'big')
            self.max_player_count = int.from_bytes(matches.group(
                                                   'max_player_count'), 'big')
            self.is_online = True

            # Parse player info
            response = self.get_player_info()
            for match in self.player_info_pattern.finditer(response):
                player = {}
                player['name'] = match.group('name').decode('utf8', 'replace')
                player['score'] = int.from_bytes(match.group('score'), 'big')
                player['time'] = int(struct.unpack('f', match.group('time'))[0])
                self.player_list.append(player)
        except (socket.timeout, AttributeError):
            self.set_status_unknown()

