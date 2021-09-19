class Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self.maxID=0

    def insert(self, vaccine):
        if self.maxID<vaccine.id:
            self.maxID=vaccine.id
        self._conn.execute("""
               INSERT INTO vaccines (id,date,supplier,quantity)
            VALUES (?,?,?,?)""", [vaccine.id,vaccine.date,vaccine.supplier,vaccine.quantity])


    def update(self, id1, amount, quantity):
        self._conn.execute("""
                UPDATE vaccines Set quantity=?   Where id==?""", (quantity-amount,id1,))

    def delete(self, id1):
        self._conn.execute("""
                       DELETE FROM vaccines Where id==?""", (id1,))


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id,name,logistic)
            VALUES (?,?,?)""", [supplier.id,supplier.name,supplier.logistic])


class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""INSERT INTO clinics (id,location,demand,logistic)
            VALUES (?,?,?,?)""", [clinic.id,clinic.location,clinic.demand,clinic.logistic])

    def update(self, location1, numberofvaccines):
        c=self._conn.cursor()
        c.execute('SELECT demand FROM clinics where location=?', (location1,))
        one=c.fetchone()
        self._conn.execute("""
                UPDATE clinics Set demand=?   Where location=?""", (one[0]-numberofvaccines,location1,))


class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""INSERT INTO logistics (id,name,count_sent,count_received)
            VALUES (?,?,?,?)""", [logistic.id,logistic.name,logistic.count_sent,logistic.count_received])

    def updateReceive(self, logistic, numberofvaccines):
        c = self._conn.cursor()
        c.execute('SELECT * FROM logistics WHERE id=?', (logistic,))
        currentCount_receive = c.fetchone()
        self._conn.execute('UPDATE logistics Set count_received=?   Where id=?', (currentCount_receive[3]+numberofvaccines,logistic,))

    def updateSent(self, logistic, numberofvaccines):
        c = self._conn.cursor()
        c.execute('SELECT * FROM logistics where id=?', (logistic,))
        currentCount_sent = c.fetchone()
        self._conn.execute('UPDATE logistics Set count_sent=?   Where id=?', (currentCount_sent[2]+numberofvaccines,logistic,))
