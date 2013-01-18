![upTee](https://raw.github.com/upTee/upTee/master/uptee/static/img/logo_75.png)
upTee - Readme
=============================
upTee is an open source software aiming to simplify all the work for hosing a [teeworlds](https://teeworlds.com) game server by providing a simple web interface.    
The software is written with [django](https://www.djangoproject.com/) and uses many other python modules.    
The project was founded by Sascha "SushiTee" Weichel to speed up the map development of [teeworlds](https://teeworlds.com). He convinced David "Fisico" Gruber to make the website beautiful.

General requirements
--------------------
* [python](http://www.python.org/) - a programming language that you should dive into
* [setuptools](http://pypi.python.org/pypi/setuptools) - Python module to install packages <sup>[1]</sup>
* [RabbitMQ](http://www.rabbitmq.com/) - AMQP messaging system, backend for celery <sup>[2]</sup>

Production requirements
-----------------------
* [nginx](http://nginx.org/) - high-performance HTTP server <sup>[2]</sup>
* [uwsgi](http://projects.unbit.it/uwsgi/) - application container server <sup>[2]</sup>
* [PostgreSQL](http://www.postgresql.org/) - The world's most advanced open source database <sup>[2]</sup>

Optional requirements
---------------------
* [memcached](http://memcached.org/) - cache backend <sup>[3]</sup>

Links
-----
* __[Beta page](http://uptee.sushitee.de)__
* __[Github repository](https://github.com/upTee/upTee/)__
* __[Issues](https://github.com/upTee/upTee/issues)__
* __[License](https://github.com/upTee/upTee/blob/master/LICENSE)__
* __[Contributors](https://github.com/upTee/upTee/blob/master/CONTRIBUTORS.md)__

Help
-----
* __[Setting up a development server](https://github.com/upTee/upTee/blob/master/docs/development_server.md)__
* __[Setting up a production server](https://github.com/upTee/upTee/blob/master/docs/production_server.md)__
* __[Mod format](https://github.com/upTee/upTee/blob/master/docs/mod_format.md)__
* __[Config format](https://github.com/upTee/upTee/blob/master/docs/config_format.md)__

### Contact
* __IRC__ - [Webchat](http://webchat.quakenet.org/?channels=teeworlds-dev)<br>___irc://irc.quakenet.org/#teeworlds-dev___<br>#teeworlds-dev at irc.quakenet.org

Notes
-----
__<sup>[1]</sup>__ Required to install all python packages needed<br>
__<sup>[2]</sup>__ Other configuration possible but not recommend<br>
__<sup>[3]</sup>__ recommend but another cached backend possible

-----

upTee – © 2012 - 2013 [upTee](http://uptee.sushitee.de/about/)
