import os
import time
from telnetlib import Telnet
from django.core.cache import cache


class TelnetClient():

    def __init__(self, port, password, server_id):
        self.terminate = False
        self.server_id = server_id
        self.tn = Telnet('localhost', port)
        self.tn.read_until('Enter password:{0}'.format(os.linesep))
        self.tn.write(password + os.linesep)
        self.start_time = time.time()
        self.run()

    def read(self):
        try:
            return self.tn.read_eager()
        except:
            self.terminate = True
            return ''

    def write(self, line):
        try:
            self.tn.write(line.encode('UTF-8') + os.linesep)
        except:
            self.terminate = True

    def send_back(self, lines_to_send):
        key = 'server-{0}-out'.format(self.server_id)
        lines = cache.get(key, [])
        lines.extend(lines_to_send)
        cache.set(key, lines)

    def get_lines_from_cache(self):
        key = 'server-{0}-in'.format(self.server_id)
        lines = cache.get(key, [])
        cache.delete(key)
        return lines

    def ping(self):
        pingtime = cache.get('server-{0}-ping'.format(self.server_id))
        if not pingtime or time.time() - pingtime > 3:
            self.terminate = True

    def run(self):
        received_data = ''
        while True:
            # check if we should shut down the process
            self.ping()

            # terminate!!
            if self.terminate:
                break

            # receive lines from server
            received_data += self.read()
            lines = received_data.split(os.linesep)
            received_data = lines.pop()  # put tail back to buffer for next run

            # lines to send back to client
            if lines:
                self.send_back(lines)

            # lines to send to telnet server
            for line in self.get_lines_from_cache():
                self.write(line)

            time.sleep(0.2)  # be nice to CPU run only 5 times per sec
