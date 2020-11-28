import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

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

@app.get('/api/registrar/{nombre}/{email}/{clave}')
def registrar(nombre:str,email:str,clave:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    info = (nombre,email,clave)
    sql=''' INSERT INTO DOCTOR(NOMBRE,EMAIL,CLAVE) VALUES (?,?,?)  '''
    registro.execute(sql,info)
    conexion.commit()
    return {"Registro Exitoso"}

@app.get('/api/login/{email}/{clave}')
def login(email:str, clave:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM DOCTOR WHERE EMAIL = '"+email+"' AND '"+clave+"' ")
    conexion.commit()
    datos=registro.fetchall()
    for I in datos:
        return {"ID":I[0],"NOMBRE":I[1]}

@app.get('/api/paciente/{cedula}/{nombre}/{apellido}/{email}/{sexo}/{fecha}/{alergias}/{id_doctor}')
def paciente(cedula: str, nombre: str, apellido: str, email:str, sexo:str, fecha:str , alergias:str, id_doctor:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    info=(cedula,nombre,apellido,email,sexo,fecha,alergias,id_doctor)
    sql= ''' INSERT INTO PACIENTE (CEDULA,NOMBRE,APELLIDO,EMAIL,SEXO,FECHA,ALERGIAS,ID_DOCTOR) VALUES (?,?,?,?,?,?,?,?) '''
    registro.execute(sql,info)
    conexion.commit()
    return {"PACIENTE REGISTRADO"}

@app.get('/api/consultar/{id_doctor}/{paciente_id}/{fecha}/{seguro}/{motivo}/{diagnostico}/{nota}')
def consultar(id_doctor:str, paciente_id: str , fecha:str , seguro:str , motivo:str , diagnostico:str , nota:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    info=(id_doctor,paciente_id,fecha,seguro,motivo,diagnostico,nota)
    sql='''INSERT INTO CONSULTA (ID_DOCTOR,PACIENTE_ID,FECHA,SEGURO,MOTIVO,,DIAGNOSTICO,NOTA) VALUES (?,?,?,?,?,?,?) '''
    registro.execute(sql,info)
    conexion.commit()
    return {"DATOS INSETADOS"}





