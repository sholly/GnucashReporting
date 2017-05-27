import piecash


class PieCashConnectionManager():
    def __init__(self, username, password, host, port='3306', database='gnucash'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.book = None
        self.session = None
        self._buildconnectionstring()

    def _buildconnectionstring(self):
        self.connString = "mysql://" + self.username + ":" + self.password + "@" + \
                          self.host + ":" + self.port + "/" + self.database

    def getBook(self):
        self.book = piecash.open_book(uri_conn=self.connString)
        return self.book

    def getSession(self):
        if self.book is None:
            self.getBook()
        self.session = self.book.session
        return self.session
