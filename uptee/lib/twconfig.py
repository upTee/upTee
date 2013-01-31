

class Config:

    def __init__(self, path):
        self.path = path
        self.options = {}
        self.votes = []
        self.tunes = []
        self.available_rcon_commands = []
        self.rcon_commands = []

    def read(self):
        with open(self.path) as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if len(line.strip()) and ((line.strip()[0] != '#' and ' ' in line.strip()) or (len(line.strip()) > 9 and line.strip()[:9] == '#command:'))]
            options = [line for line in lines if line.split(' ', 1)[0] not in ['add_vote', 'tune'] and line.split(' ', 1)[0][0] != '#']
            tunes = [line.split(' ', 1)[1] for line in lines if line.split(' ', 1)[0] == 'tune']
            votes = [line.split(' ', 1)[1] for line in lines if line.split(' ', 1)[0] == 'add_vote']
            rcon_commands = [line[9:] for line in lines if line[:9] == '#command:']
            self.options = {}
            for line in options:
                command = line.split(' ', 1)[0]
                widget = line.rsplit(' ', 1)[1].split(':', 1)[1] if line.rsplit(' ', 1)[1][0] == '#' and '#widget:' in line.rsplit(' ', 1)[1] else 'text'
                line = line.split(' ', 1)[1]
                if ' ' in line and line.rsplit(' ', 1)[1][0] == '#' and '#widget:' in line.rsplit(' ', 1)[1]:
                    line = line.rsplit(' ', 1)[0]
                value = line.strip('"')
                # in case of select widget save the selections to the value
                if len(widget) >= 7:
                    if widget[:7] == 'select:' and len(widget[7:]):
                        selections = widget.split(':', 1)[1].split(',')
                        widget = 'select'
                        if value not in selections:
                            selections.append(value)
                        for selection in selections:
                            value += ',{0}'.format(selection)
                    elif widget[:7] == 'select:':
                        widget = 'text'
                self.options[command] = (value, widget)
            self.tunes = [{'command': line.rsplit()[0].strip('"'), 'value': float(line.split()[1].strip('"'))} for line in tunes]
            self.votes = [{'command': line.rsplit('" ', 1)[1].strip('"'), 'title': line.rsplit('" ', 1)[0].strip('"')} for line in votes if len(line.split('" ')) == 2]
            for line in rcon_commands:
                self.available_rcon_commands.extend([command for command in line.split() if command not in self.available_rcon_commands])

    def write(self, path=None):
        if not path:
            path = self.path
        with open(path, 'w') as f:
            for key, value in self.options.iteritems():
                f.write(u'{0} "{1}" #widget:{2}\n'.format(key, value[0], value[1]).encode('UTF-8'))
            for tune in self.tunes:
                f.write(u'tune {0} {1}\n'.format(tune['command'], tune['value']).encode('UTF-8'))
            for vote in self.votes:
                f.write(u'add_vote "{0}" "{1}"\n'.format(vote['title'], vote['command']).encode('UTF-8'))
            for rcon_command in self.rcon_commands:
                f.write(u'{0} {1}\n'.format(rcon_command['command'], rcon_command['value']).encode('UTF-8'))

    def add_option(self, command, value, widget='text'):
        if isinstance(value, int):
            value = str(value)
        self.options[command] = (value.replace('"', r'\"'), widget)

    def add_tune(self, command, value):
        self.tunes.append({'command': command, 'value': float(value)})

    def add_vote(self, command, title):
        self.votes.append({'command': command.replace('"', r'\"'), 'title': title.replace('"', r'\"')})

    def add_rcon_command(self, command, value):
        self.rcon_commands.append({'command': command.replace('"', r'\"'), 'value': value.replace('"', r'\"')})
