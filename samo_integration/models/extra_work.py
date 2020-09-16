import psycopg2


class ExcportPrices:
    '''
    Extra work to extract samo prices in the format of BGTO system
    '''

    def __init__(self, host, login, password, database, shema=None):
        self.host = host
        self.login = login
        self.password = password
        self.database = database
        self.shema = shema
        connection = psycopg2.connect(user=login,
                                      password=password,
                                      host=host,
                                      port="5432",
                                      database=database)

    def connect(self):
        connection = psycopg2.connect(user=self.login,
                                      password=self.password,
                                      host=self.host,
                                      port="5432",
                                      database=self.database)
        return connection.cursor()


def main():
    print('hello , lets go to business , connecting to database  \n')
    print('start by providing connection environnement \n')
    host = '127.0.0.1'
    login = 'openpg'
    passw = 'openpgpwd'
    database = 'samo'
    obj = ExcportPrices(host, login, passw, database)
    curs = obj.connect()
    curs.execute("SELECT version();")
    record = curs.fetchone()
    print("You are connected to - ", record, "\n")
    curs.execute("select name,pcount,adult,child,infant from samo_allocation")
    for x in curs.fetchall():
        print(
            "name : {0} , pcount: {1}, adult : {2} , child : {3} , infant :  {4}".format(x[0], x[1], x[2], x[3], x[4]))


if __name__ == '__main__':
    main()
