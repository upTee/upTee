import socket


def int_unpack(input):
    added = 1
    sign = ord(input[0]) >> 6 & 1
    out = ord(input[0]) & 0x3f
    if (ord(input[0]) & 0x80) == 0:
        out ^= -sign
        return added, out
    out |= (ord(input[1]) & 0x7f) << 6
    added += 1

    if (ord(input[1]) & 0x80) == 0:
        out ^= -sign
        return added, out
    out |= (ord(input[2]) & 0x7f) << 13
    added += 1

    if (ord(input[2]) & 0x80) == 0:
        out ^= -sign
        return added, out
    out |= (ord(input[3]) & 0x7f) << 20
    added += 1

    if (ord(input[3]) & 0x80) == 0:
        out ^= -sign
        return added, out
    out |= (ord(input[4]) & 0x7f) << 27
    out ^= -sign
    added += 1
    return added, out


def string_unpack(input):
    for i in range(len(input)):
        if input[i] == '\x00':
            return i + 1, input[:i]
    return ''


class ServerInfo:

    SERVERINFO_FLAG_PASSWORD = 0x1

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 0))
        self.sock.settimeout(2)  # do this different later and in an extra task with higher timeout
        self.compressed_data = True
        self.data = ''
        self.server_info = {}

    def send(self, port=8300):
        data = '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffgie3\x01'
        try:
            address = ('127.0.0.1', port)
            self.sock.sendto(data, address)
            self.data, recv_address = self.sock.recvfrom(2048)
            if address == recv_address:
                self.handle_data()
        except socket.error:
            print 'Server is offline'

    def unpack_str(self):
        added, out = string_unpack(self.data)
        self.data = self.data[added:]
        return out

    def unpack_int(self):
        if self.compressed_data:
            added, num = int_unpack(self.data)
        else:
            added, num = string_unpack(self.data)
            num = int(num)
        self.data = self.data[added:]
        return num

    def handle_data(self):
        if len(self.data) < 14 or self.data[:14] != '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffinf3':
            return
        self.data = self.data[14:]
        added, token = int_unpack(self.data)
        if token != 1:  # test for old version
            added, token = string_unpack(self.data)
            if token == '1':
                self.data = self.data[added:]
                self.compressed_data = False
            else:
                return
        else:
            self.compressed_data = True
        self.data = self.data[added:]

        self.server_info['version'] = self.unpack_str()
        self.server_info['name'] = self.unpack_str()
        if self.compressed_data:
            self.server_info['hostname'] = self.unpack_str()
        self.server_info['map'] = self.unpack_str()
        self.server_info['gametype'] = self.unpack_str()
        self.server_info['flags'] = self.unpack_int()
        if self.compressed_data:
            self.server_info['skill_level'] = self.unpack_int()
        self.unpack_int()  # this value is not needed
        self.server_info['max_players'] = self.unpack_int()
        num_clients = self.unpack_int()
        self.server_info['max_clients'] = self.unpack_int()

        clients = []
        players = []
        for i in range(num_clients):
            client = {
                'name': self.unpack_str(),
                'clan': self.unpack_str(),
                'country': self.unpack_int(),
                'score': self.unpack_int(),
                'is_player': self.unpack_int()
            }
            clients.append(client)
            if client['is_player']:
                players.append(client)
        # sort players by score
        players = sorted(players, key=lambda k: k['score'], reverse=True)
        self.server_info['clients'] = clients
        self.server_info['players'] = players

        spectators = []
        for client in clients:
            if client not in players:
                spectators.append(client)
        # sort specs by name
        spectators = sorted(spectators, key=lambda k: k['name'])
        self.server_info['spectators'] = spectators

    @property
    def password(self):
        return True if self.server_info and self.server_info['flags'] & ServerInfo.SERVERINFO_FLAG_PASSWORD else False
