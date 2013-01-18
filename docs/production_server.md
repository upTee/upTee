Setting up a production server
==============================
A production server is a server for use.    
The following manual shows how to install upTee on a linux server using nginx and uWSGI.

Installation
------------
###Install all requirements
Be sure to install all requirements shown in the [README](https://github.com/upTee/upTee/blob/master/README.md).    
__Do not install uWSGI yet!__    
In case the command _pip_ is not available after installing _setuptools_ run the following command:    
```shell
$ easy_install pip
```

  &nbsp;&nbsp;1\. Create a new user and be sure to make him the owner of the virtualenv which will be created in the next step.    

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this manual the user __uptee__ is used!    

  &nbsp;&nbsp;2\. Create a virtualenv. This will house a complete Python environment, and the compiled uwsgi binary.    

```shell
$ easy_install virtualenv
$ virtualenv uptee
$ cd uptee/
$ . bin/activate
```

  &nbsp;&nbsp;3\. Download the uWSGI tarball into a pkg/ directory.

```shell
$ mkdir pkg && cd pkg/
$ wget 'http://projects.unbit.it/downloads/uwsgi-1.4.4.tar.gz'
```

  &nbsp;&nbsp;4\. Compile uWSGI. _You may have to install missing packages to compile uWSGI._

```shell
$ tar -xzvf uwsgi-1.4.4.tar.gz
$ cd uwsgi-1.4.4/
$ make
```

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The last command creates the uwsgi binary which must be moved to the bin folder.

```shell
$ mv uwsgi $VIRTUAL_ENV/bin/uwsgi
```

###Configuration

  &nbsp;&nbsp;1\. Clone upTee    

```shell
$ git clone git://github.com/upTee/upTee.git web
```

  &nbsp;&nbsp;2\. Install all requirements    

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Switch into the _web_ directory and run the following command:    
```shell
$ pip install -r requirements.txt
```
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If an error appears install the missing packages. The error messages are obvious.    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In windows download packages which fails from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/).    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Repeat the command until the installation finishes successfully!    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If there are still problems with some modules have a look at the [Troubleshooting section](https://github.com/upTee/upTee/blob/master/docs/production_server.md#troubleshooting).    

  &nbsp;&nbsp;3\. Set up the website    

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Switch into the _uptee_ directory.    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To set up the project copy the _settings_local.py.example_ and rename the new file to _settings_local.py_.    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Now edit the settings how u like. You can find an example for a production server [here](https://github.com/upTee/upTee/blob/master/docs/settings_production/settings_local.py).    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Copy _browscap.csv.example_ and rename the new file to _browscap.csv_.    
  
  &nbsp;&nbsp;4\. Install the database    

```shell
$ python manage.py syncdb
```
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It will ask to create a Superuser. Do that!    
```shell
$ python manage.py migrate
```

  &nbsp;&nbsp;5\. Set up the port map    

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The port map is a list of available ports for the teeworlds servers. Be sure that the ports are not blocked by a firewall.    
```shell
$ python manage.py create_portmap 8300 8320
```
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This command adds the ports 8300 till 8320 to upTee. Decide yourself which ports you want to use and how many you need.   

  &nbsp;&nbsp;6\. Set up nginx   

  Create the _sock_ folder.    
```shell
mkdir $VIRTUAL_ENV/sock
```

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Open the nginx config file and add the following code to the _http_ section:    
```
# uWSGI serving Django.
upstream django {
  # Distribute requests to servers based on client IP. This keeps load
	# balancing fair but consistent per-client. In this instance we're
	# only using one uWGSI worker anyway.
	ip_hash;
	server unix:/path/to/virtualenv/sock/uwsgi.sock;
}

server {
	listen 80;
	server_name example.org www.example.org # your domain here!
	underscores_in_headers on;

	# Django admin media.
	location /media/admin/ {
		alias /path/to/virtualenv/lib/python2.7/site-packages/django/contrib/admin/static/admin/;
	}

	# Your project's static media.
	location /media/ {
		alias /path/to/virtualenv/web/uptee/media/;
	}

	# Your project's static media.
	location /static/ {
		alias /path/to/virtualenv/web/uptee/static/;
	}

	# Finally, send all non-media requests to the Django server.
	location / {
    # touch /path/to/virtualenv/web/downtime to set the page down
		if (-f /path/to/virtualenv/web/downtime) {
			return 503;
		}

		uwsgi_pass  django;
		include     uwsgi_params;
		uwsgi_read_timeout 1800;
	}

	error_page 502 503 504 @maintenance;
	location @maintenance {
		root /path/to/virtualenv/web/uptee/templates/;
		rewrite ^(.*)$ /502.html break;    
	}
}
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure to change the path to the virtualenv and put your own domain.    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To finish the nginx configuration restart nginx:    
```shell
$ /etc/init.d/nginx restart
```

###Start up everything
Starting up everything means to run some processes. There are scripts to make everything easy.        

  &nbsp;&nbsp;1\. Create the _log_ directory    
```shell
mkdir -p $VIRTUAL_ENV/var/log
```

  &nbsp;&nbsp;2\. Get the scripts    

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Download the [start](https://github.com/upTee/upTee/blob/master/scripts/start) script and copy into the virtualenv directory.    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Download the [uptee](https://github.com/upTee/upTee/blob/master/scripts/uptee) script and copy into the virtualenv directory.    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Download the [uptee init.d](https://github.com/upTee/upTee/blob/master/scripts/init.d/uptee) script and copy into _/etc/init.d/_.

  &nbsp;&nbsp;3\. Edit the scripts    

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Open every script and change the path to the actual virtualenv directory.    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure every script is executable!

  &nbsp;&nbsp;4\. Activate the init.d script    

```shell
$ update-rc.d uptee defaults
```

  &nbsp;&nbsp;5\. Start upTee

```shell
$ /etc/init.d/uptee start
```

###Miscellaneous
The init.d script allows it to start/stop/restart upTee.    
```shell
$ /etc/init.d/uptee {start|stop|restart}
```

To update uptee simply update the git repository.    
```shell
$ git pull origin master
```
After updating the website needs to be restarted to make the changes take effect!

Troubleshooting
---------------
###error: Unable to find vcvarsall.bat
Some modules need a C/C++ compiler to build parts of the module for performance reasons.    
In windows it may happen that it will not find the compiler or it might be even not installed.    
If this is the case just download module from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/) and install it. After the installation you may still get the same error.    
Just comment out the concerned module in the _requirements.txt_.    
Example:    
```
# PIL>=1.1.7
```
