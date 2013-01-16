Setting up a development server
===============================
Setting up a development server is important if you want to help with the development of upTee.

Installation
------------
###Install all requirements    
Be sure to install all requirements shown in the [README](https://github.com/upTee/upTee/blob/master/README.md).    
```
pip install -r requirements.txt
```
If an error appears install the missing packages. The error messages are obvious.    
In windows download packages which fails from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/).
Repeat the command until the installation finishes successfully!

###Set up the project
To set up the project copy the _settings_local.py.example_ and rename the new file to _settings_local.py_.    
Now edit the settings how u like. You can find an example for a development server [here](https://github.com/upTee/upTee/blob/master/docs/settings_local.py).

###Install the database
Switch into the uptee folder and enter the following commands:    
```
python manage.py syncdb
```
It will ask to create a Superuser. Do that!    
```
python manage.py migrate
```

###Set up the port map
the port map is a list of available ports for the teeworlds servers. Be sure that the ports are not blocked by a firewall.    
```
python manage.py create_portmap 8300 8320
```
This command adds the ports 8300 till 8320 to upTee. Decide yourself which ports you want to use and how many you need.

###Start up the server
You will have to run two processes for starting up the Server.    
First you have to run the celery worker.    
```
python manage.py celery worker --loglevel=info
```
Be sure that the broker for celery is running (RabbitMQ is recommended).    
After celery is running, run the server itself.
```
python manage.py runserver
```
The website is now availableunder __http://localhost:8000/__
