Wardriving PKP
==============

This software is built for practise with wardriving, only for academic reasons.
Tested only with python 3 but it may work with python 2 too.

What is this
------------
The script receives a KML file as input and stores it in a relational database.
Synchronize, create new and merge placemarks is basically what it does.

Installation
------------
```git clone https://github.com/maxpowel/wdpkp.git```

```cd wdpkp```

```pip install -r requirements.txt```

That's all, next step is configure your database

Configuration
-------------
I use a mysql but you can use everything supported by sqlalchemy. Copy the file parameters.yml.dist

```cp config/parameters.yml.dist config/parameters.yml```

Now edit the file config/parameters.yml and write your own database configuration

Once you have configured your database you need to create the database schema

```python create_schema.py```


Usage
-----
```python main.py filename.kml```

If everything went fine, the count of processed entries are shown