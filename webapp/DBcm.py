import mysql.connector


class MyConnectionError(Exception):
    pass


class MyCredentialsError(Exception):
    pass


class MySQLError(Exception):
    pass


class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> 'cursor':
        try:
            self.connection = mysql.connector.connect(**self.configuration)
            self.cursor = self.connection.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise MyConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise MyCredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise MySQLError(exc_value)
        elif exc_type:
            print(exc_type, exc_value)
            raise exc_type(exc_value)
