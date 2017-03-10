from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from mapped_config.loader import YmlLoader

# Just load configuration from configuration file.
# Check https://github.com/maxpowel/mapped_config for doc
database_config_schema = {
    "database": {
        "driver": None,
        "database": None,
        "hostname": "localhost",
        "username": "root",
        "password": "123456",
    }

}

yml_loader = YmlLoader()
config = yml_loader.load_config("config/config.yml", "config/parameters.yml")
mapped_config = yml_loader.build_config(config, [database_config_schema])
database_config = mapped_config.database

# Create database connection
engine = create_engine('{driver}://{username}:{password}@{host}/{dbname}'.format(
    driver=database_config.driver,
    username=database_config.username,
    password=database_config.password,
    host=database_config.hostname,
    dbname=database_config.database
), echo=False)

Session = sessionmaker(bind=engine)

# Avoid load again and again same objects. A simple cache manager
class CachedFinder(object):
    def __init__(self, session):
        self.session = session
        self.cache = {}

    def get(self, model, name):
        cache_key = str(model) + "_" + name
        if cache_key not in self.cache:
            try:
                device_type = self.session.query(model).filter(model.name == name).one()
            except NoResultFound:
                device_type = model(name=name)
                self.session.add(device_type)

            self.cache[cache_key] = device_type

        return self.cache[cache_key]