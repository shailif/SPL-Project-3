# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from repository import _Repository

from dto import Vaccine, Supplier, Clinic, Logistic

def mainexecute():
    with open(sys.argv[1], encoding='UTF-8') as file_in:
        lines= []
        for line in file_in:
            lines.append(line)
        indexofline=1


        for i in range(1,int(lines[0].split(',')[0])+1):
            repo.vaccines.insert(Vaccine(int(lines[indexofline].split(',')[0]),lines[indexofline].split(',')[1],int(lines[indexofline].split(',')[2]),int(lines[indexofline].split(',')[3])))
            indexofline=indexofline+1
        for i in range(1,int(lines[0].split(',')[1])+1):
            repo.suppliers.insert(Supplier(int(lines[indexofline].split(',')[0]),lines[indexofline].split(',')[1],int(lines[indexofline].split(',')[2])))
            indexofline = indexofline + 1
        for i in range(1,int(lines[0].split(',')[2])+1):
            repo.clinics.insert(Clinic(int(lines[indexofline].split(',')[0]),lines[indexofline].split(',')[1],int(lines[indexofline].split(',')[2]),int(lines[indexofline].split(',')[3])))
            indexofline=indexofline+1
        for i in range(1, int(lines[0].split(',')[3]) + 1):
            repo.logistics.insert(Logistic(int(lines[indexofline].split(',')[0]), lines[indexofline].split(',')[1],int(lines[indexofline].split(',')[2]),int(lines[indexofline].split(',')[3])))
            indexofline=indexofline+1

    with open(sys.argv[2], encoding='UTF-8') as file_in:
        lines2= []
        for line in file_in:
            lines2.append(line)
        f = open(sys.argv[3], "w+")
        total_inventory=repo._conn.cursor().execute('SELECT SUM(quantity) FROM vaccines').fetchone()[0]
        total_demand=repo._conn.cursor().execute('SELECT SUM(demand) FROM clinics').fetchone()[0]
        total_received=0
        total_sent=0
        for i in range(0,len(lines2)):
            if lines2[i].count(',')==1:
                SendShipment(lines2[i].split(',')[0],int(lines2[i].split(',')[1]))
                total_sent=total_sent+int(lines2[i].split(',')[1])
                total_demand=total_demand-int(lines2[i].split(',')[1])
                total_inventory=total_inventory-int(lines2[i].split(',')[1])
                f.write(str(total_inventory)+","+str(total_demand)+","+str(total_received)+","+str(total_sent))
                f.write("\n")

            elif lines2[i].count(',')==2:
                ReceiveShipment(lines2[i].split(',')[0], int(lines2[i].split(',')[1]),lines2[i].split(',')[2])
                total_received=total_received+int(lines2[i].split(',')[1])
                total_inventory=total_inventory+int(lines2[i].split(',')[1])
                f.write(str(total_inventory)+","+str(total_demand)+","+str(total_received)+","+str(total_sent))
                f.write("\n")

    f.close()

def SendShipment(location1, amount):
    c = repo._conn.cursor()
    c.execute('SELECT * FROM clinics WHERE location=?', (location1,))
    logisticId = c.fetchone()
    repo.logistics.updateSent(int(logisticId[3]), amount)
    repo.clinics.update(location1,amount)

    while amount > 0:
        c.execute('SELECT * FROM vaccines order by date')
        all=c.fetchall()
        id1 = all[0][0]
        quantity1=all[0][3]
        if quantity1>amount:
            repo.vaccines.update(id1,amount, quantity1)
            amount=0
        elif quantity1==amount:
            repo.vaccines.update(id1, amount,amount)
            repo.vaccines.delete(id1)
            amount=0
        else:
            repo.vaccines.delete(id1)
            amount=amount-quantity1


def ReceiveShipment(name,amount,date):
    c = repo._conn.cursor()
    c.execute('SELECT * FROM suppliers where name=?', (name,))
    supplier = c.fetchone()
    repo.vaccines.insert(Vaccine(repo.vaccines.maxID+1,date,supplier[0],amount))
    repo.logistics.updateReceive(supplier[2], amount)



if __name__ == '__main__':
    repo = _Repository()
    mainexecute()
    repo._close()


