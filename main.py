import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import urllib.request
import datetime
from datetime import date

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api')
def read_root():
    return {'detail': 'Welcome to this app'}

@app.post('/api/Registrar_P/{cedula}/{vacuna}/{provincia}/{fecha_v}')
def Registrar_P(cedula: str, vacuna: str, provincia: str, fecha_v: str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    respuesta = urllib.request.urlopen('https://api.adamix.net/apec/cedula/'+cedula+'')
    data = json.loads(respuesta.read())
    query = registro.execute ("SELECT * FROM VACUNADO Where CEDULA = '"+cedula+"'")
    datos = query.fetchall()
    for dato in datos:
        if dato[1] == cedula:
            sql =("UPDATE VACUNADO SET FECHA_S = '"+fecha_v+"' WHERE CEDULA = '"+cedula+"'")
            registro.execute(sql)
            registro.execute("UPDATE VACUNA SET CANTIDAD = CANTIDAD-1 WHERE MARCA = '"+vacuna+"'")
            conexion.commit()
            return {"mensaje":"Segunda dosis agregada","nombre": dato[2],"apellido":dato[3], "fecha_p":dato[7] }
    if datos == []: 
        try:     
            if data['Cedula']==cedula:
                info= (data['Cedula'],data['Nombres'],data['Apellido1'],datetime.datetime.strptime(data['FechaNacimiento'], '%Y-%m-%d %H:%M:%S.%f').date(),vacuna,provincia,fecha_v)
                sql=''' INSERT INTO VACUNADO(CEDULA,NOMBRE,APELLIDO,FECHA_N,VACUNA,PROVINCIA,FECHA_P) VALUES (?,?,?,?,?,?,?) '''
                registro.execute(sql,info)
                registro.execute("UPDATE VACUNA SET CANTIDAD = CANTIDAD-1 WHERE MARCA = '"+vacuna+"'")
                conexion.commit()
                return {"mensaje": "Registro Exitoso"}
        except:
            return{'Cedula invalida'}
@app.post('/api/Registrar_v/{marca}/{cantidad}')
def Registrar_v(marca: str, cantidad: int):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    info = (marca,cantidad)
    query = ''' INSERT INTO VACUNA(MARCA,CANTIDAD) VALUES (?,?) '''
    registro.execute(query,info)
    conexion.commit()
    return {'Registro Completo'}



            



