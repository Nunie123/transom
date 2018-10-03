import pymysql
from sqlalchemy import create_engine

from utilities.helpers import get_single_dict_from_json, get_full_path, get_connection_details


class ConnectionManager():
    def __init__(self, connection_name):
        self.connection_name = connection_name
        self.engine = None
        self.conn = None
        self.initialize_connection_details()

    def initialize_connection_details(self):
        connection_dict = get_connection_details(self.connection_name)
        self.host = connection_dict.get('host')
        self.port = connection_dict.get('port')
        self.db_type = connection_dict.get('db_type')
        self.username = connection_dict.get('username')
        self.password = connection_dict.get('password')
        self.default_db = connection_dict.get('default_db')

    def connect(self):
        try:
            self.engine = self.create_engine()
            self.conn = self.engine.connect()
        except ValueError:
            raise
        except:
            raise RuntimeError("Unable to connect to database {}".format(self.connection_name))

    def create_engine(self):
        if self.db_type == 'sqlite':
            return create_engine('sqlite:///{host}'.format(**self.__dict__))
        elif self.db_type == 'mysql':
            return create_engine('mysql+pymysql://{username}:{password}@{host}'.format(**self.__dict__))
        else:
            raise ValueError("Unsupported RDBMS: {}".format(self.db_type))

    def close(self):
        self.conn.close()
        self.engine.dispose()

    def closed(self):
        if self.conn:
            return self.conn.closed
        else:
            return None
    
    def __repr__(self):
        return f'ConnectionManager instance connected to {self.connection_name}.'


class ConnectionPool(object):

    def __init__(self, dbs=[]):
        self.pool = {}
        for db in dbs:
            self.add_connection(db)

    def connections(self):
        return self.pool.keys()

    def add_connection(self, db):
        if db not in self.connections():
            cm = ConnectionManager(db)
            cm.connect()
            self.pool[db] = cm
        return self.get(db)

    def get(self, db):
        return self.pool.get(db)

    def close(self, db):
        self.pool[db].close()

    def close_all(self):
        for conn in self.connections():
            self.close(conn)


if __name__ == '__main__':
    pass
