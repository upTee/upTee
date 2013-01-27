Config format
=============
Every mod uploaded to uptee uses a default config. In the config is defined which server commands and tunings are allowed to change and how they will look like. Also it defines the default settings and votes for the mod.    
The user cannot add or remove commands or tunings, only it's values.

Installation
------------
The default config is part of every mod and is required. The config __must__ have the filename _config.cfg_ and is located in the root folder of each mod.

Widgets
-------
The widgets define how the config option is shown on the website. The widget is written after each config option.    
Unknown widget or missing widget will be automatically recognized as _text_ widget.    
Every widget defintion starts with __#widget:__    
The following widgets are available:

###[text] - a string value. Used for strings and integer options. (default widget)    
```
sv_name " upTee Testserver" #widget:text
```
###[textarea] - a multiline string. Line breaks get converted automatically on the website.    
```
sv_motd "upTee Testserver - Vanilla\n\nThis server is a test\n\nHosted by Sushi" #widget:textarea
```
###[password] - a string value. Values on the website are hidden.    
```
sv_rcon_password "example" #widget:password
```
###[checkbox] - boolean value. Used for integer values limited to 0 and 1.    
```
sv_powerups 0 #widget:checkbox
```

Commands
--------
With the _#command:_ command you can add rcon commands which should be available for putting inside of the config.    
You can put more than one command after the command seperated by a space.    
It is important that there is no space after the _":"_ and no space between the _"#"_ and _"command"_.    
The user can add all allowed commands to the config via the website.    
```
#command:mod_command
#command:add_vote change_map
```

Example
-------
The following example shows a vanilla 0.7 config. All commands and tunings written down are allowed to change by the user. The votes get added.
```
# basic settings
sv_name " upTee Testserver"
sv_motd "upTee Testserver - Vanilla\n\nThis server is a test server.\nNo warranties.\n\nHosted by Sushi" #widget:textarea
sv_map ctf3
sv_max_clients 16

# limit settings
sv_max_clients_per_ip 2
sv_rcon_max_tries 3
sv_rcon_bantime 5
sv_inactivekick_time 2
sv_inactivekick 1

# password
password "" #widget:password
sv_rcon_password "examplerc" #widget:password

# game
sv_scorelimit 0
sv_timelimit 0
sv_gametype sur
sv_spectator_slots 10
sv_warmup 0
sv_teamdamage 0 #widget:checkbox
sv_match_swap 0 #widget:checkbox
sv_powerups 0 #widget:checkbox
sv_tournament_mode 1 #widget:checkbox
sv_strict_spectate_mode 0 #widget:checkbox
sv_player_ready_mode 0 #widget:checkbox

# votes
add_vote "Restart round" restart 15
add_vote "Reload map" reload
add_vote "Move all players to spectators" set_team_all -1
add_vote "Swap teams" swap_teams
add_vote "Shuffle teams" shuffle_teams
add_vote "10 spectator slots" sv_spectator_slots 10
add_vote "12 spectator slots" sv_spectator_slots 12
#add_vote "change score limit to 600" sv_scorelimit 600
#add_vote "change score limit to 1000" sv_scorelimit 1000

```
