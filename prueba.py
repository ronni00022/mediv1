import sqlite3
cedula = input('hh: ')
conexion=sqlite3.connect('app1.db')
registro=conexion.cursor()
e = registro.execute ("SELECT * FROM VACUNADO Where CEDULA = '"+cedula+"'")
data = e.fetchall()
for dato in data:
    if dato[1] == cedula:
        print("hola")
if data == []:
    print("222")
