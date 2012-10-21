
class Config:

    def __init__(self, path):
        self.path = path
        self.options = {}
        self.votes = []
        self.tunes = []

    def read(self):
        with open(self.path) as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if len(line.strip()) and line.strip()[0] != '#' and ' ' in line.strip()]
            options = [line for line in lines if line.split(' ', 1)[0] not in ['add_vote', 'tune']]
            tunes = [line.split(' ', 1)[1] for line in lines if line.split(' ', 1)[0] == 'tune']
            votes = [line.split(' ', 1)[1] for line in lines if line.split(' ', 1)[0] == 'add_vote']
            self.options = {line.split(' ', 1)[0] : (line.split(' ', 1)[1].rsplit(' ', 1)[0].strip('"'), line.rsplit(' ', 1)[1].split(':', 1)[1] if line.rsplit(' ', 1)[1][0] == '#' and '#widget:' in line.rsplit(' ', 1)[1] else 'text') for line in options}
            self.tunes = [{'command': line.rsplit().strip('"')[0], 'value': float(line.split().strip('"')[1])} for line in tunes]
            self.votes = [{'command': line.rsplit('" ', 1)[1].strip('"'), 'title': line.rsplit('" ', 1)[0].strip('"')} for line in votes if len(line.split('" ')) == 2]

    def write(self, path=None):
        if not path:
            path = self.path
        with open(path, 'w') as f:
            for key, value in self.options.iteritems():
                f.write('{0} "{1}" #widget:{2}\n'.format(key, value[0], value[1]))
            for tune in self.tunes:
                f.write('tune {0} {1}\n'.format(tune['command'], tune['value']))
            for vote in self.votes:
                f.write('add_vote "{0}" "{1}"\n'.format(vote['title'], vote['command']))

    def add_option(self, command, value, widget='text'):
        self.options[command] = (value, widget)

    def add_tune(self, command, value):
        self.tunes.append({'command': command, 'value': float(value)})

    def add_vote(self, command, title):
        self.votes.append({'command': command, 'title': title})
