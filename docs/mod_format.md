Mod format
==========
Every mod has a special format which is required for upTee to recognize the mods and set its default settings.    
Mod files are packed in _.tar_ or _.zip_ files.

Installation
------------
The complete mod file just gets uploaded in the admin panel of upTee. The website will check if its content is valid.

File structure
--------------
The following file structure __must__ be used:    
```
mod_name.tar(.zip)
  - data
    + mapres
    + maps
  config.cfg
  license.txt
  readme.txt
  teeworlds_srv
```
The _mapres_ directory __must__ be present for the server to start but it is recommended to leave it empty.   
The _maps_ directory contains all the default maps which should be shipped with the mod.    
The _config.cfg_ contains the default settings for the mod and __must__ be in a special [config format](https://github.com/upTee/upTee/blob/master/docs/config_format.md).    
The _license.txt_ and _readme.txt_ are not important but should be present.    
The _teeworlds_srv_ is the server binary (in Windows _teeworlds_srv.exe_). The file name of the binary can be changed in the website settings but it is not recommended to change.
