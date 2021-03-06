import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

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
        return {"ID":I[0],"NOMBRE":I[1],"CORREO":I[2],"CLAVE":I[3]}

@app.get('/api/paciente/{cedula}/{nombre}/{apellido}/{email}/{sexo}/{fecha}/{alergias}/{id_doctor}/{zodiac}/{sangre}')
def paciente(cedula: str, nombre: str, apellido: str, email:str, sexo:str, fecha:str, alergias:str, id_doctor:str, zodiac:str, sangre:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()

    info=(cedula,nombre,apellido,email,sexo,fecha,alergias,id_doctor,zodiac,sangre)
    sql= ''' INSERT INTO PACIENTE (CEDULA,NOMBRE,APELLIDO,EMAIL,SEXO,FECHA,ALERGIAS,ID_DOCTOR, ZODIACO,SANGRE) VALUES (?,?,?,?,?,?,?,?,?,?) '''
    registro.execute(sql,info)
    conexion.commit()
    return {"PACIENTE REGISTRADO"}

@app.get('/api/consultar/{id_doctor}/{paciente_id}/{fecha}/{seguro}/{motivo}/{diagnostico}/{nota}/{monto}')
def consultar(id_doctor:str, paciente_id: str , fecha:str , seguro:str , motivo:str , diagnostico:str , nota:str,monto:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM PACIENTE WHERE ID_PACIENTE='"+paciente_id+"'")
    datos=registro.fetchall()
    for i in datos:
        nombre=i[2]
        sexo=i[5]
        fecha_p=i[6]
        cedula=i[1]
    info=(id_doctor,paciente_id,fecha,seguro,motivo,diagnostico,nota,nombre,sexo,fecha_p,cedula,monto)
    sql='''INSERT INTO CONSULTA (ID_DOCTOR,PACIENTE_ID,FECHA,SEGURO,MOTIVO,DIAGNOSTICO,NOTA,NOMBRE_P,SEXO_P,FECHA_P,CEDULA,MONTO) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) '''
    registro.execute(sql,info)
    conexion.commit()
    return {"DATOS INSETADOS"}

@app.get('/api/consultar_f/{fecha}/{id_doctor}')
def consultar_f(fecha: str,id_doctor:str):
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM CONSULTA WHERE FECHA ='"+fecha+"' and ID_DOCTOR='"+id_doctor+"'")
    conexion.commit()
    datos =registro.fetchall()
    for i in datos:
        a.append({"NOMBRE":i[3],"Sexo":i[4],"FECHA_P":i[5],"CEDULA":i[6],"FECHA_C":i[7]})
    return a

@app.get('/api/consultar_zodiaco/{id_doctor}')
def consultar_z(id_doctor: str):
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT CEDULA, NOMBRE, APELLIDO, ZODIACO FROM PACIENTE WHERE ID_DOCTOR='"+ id_doctor +"'")
    conexion.commit()
    datos = registro.fetchall()
    for i in datos:
        a.append({"CEDULA": i[0], "NOMBRE": i[1], "APELLIDO":i[2], "ZODIACO": i[3]})

    return a

@app.get('/api/consultar_fecha/{id_paciente}')
def consultar_visitas(id_paciente: str):
    A=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT NOMBRE_P, COUNT(PACIENTE_ID) FROM CONSULTA WHERE  ID_DOCTOR ='"+id_paciente+"' GROUP BY NOMBRE_P")
    conexion.commit()
    datos=registro.fetchall()
    for i in datos:
        A.append({"NOMBRE":i[0],"VISITAS":i[1]})
    return A

@app.get('/api/actualizar_paciente/{campo}/{cambios}/{doctor_id}/{pasiente_id}')
def actualizar_paciente(campo: str, cambios: str, doctor_id:str,pasiente_id:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    query = f"UPDATE PACIENTE SET {campo.upper()}='"+cambios+"'WHERE ID_DOCTOR = '"+doctor_id+"' AND ID_PACIENTE='"+pasiente_id+"'"
    registro.execute(query)
    conexion.commit()
    return {'detail': 'Actualizados'}

@app.get('/api/actualizar_consulta/{campo}/{cambios}/{consulta_id}/{doctor_id}')
def actualizar_consultar(campo: str, cambios: str, consulta_id: str, doctor_id: str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    query = f"UPDATE CONSULTA SET {campo.upper()}='"+cambios+"'WHERE ID_CONSULTA = '"+consulta_id+"' AND ID_DOCTOR = '"+doctor_id+"'"
    registro.execute(query)
    conexion.commit()
    return {'detail': 'Actualizados'}

@app.get('/api/con_v/{id_doctor}')
def con_v(id_doctor:str):
    A=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM CONSULTA WHERE ID_DOCTOR='"+id_doctor+"'")
    conexion.commit()
    datos=registro.fetchall()
    for I in datos:
        A.append({"ID":I[0],"FECHA":I[7],"SEGURO":I[8],"MOTIVO":I[9],"DIAG":I[10],"NOTA":I[11],"MONTO":I[12]})
    return A
@app.get('/api/con_p/{id_doctor}')
def con_p(id_doctor:str):
    A=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM PACIENTE WHERE ID_DOCTOR ='"+id_doctor+"'")
    conexion.commit()
    datos=registro.fetchall()
    for I in datos:
        A.append({"ID":I[0],"CEDULA":I[1],"NOMBRE":I[2],"APELLIDO":I[3],"EMAIL":I[4],"SEXO":I[5],"ALERGIAS":I[7],"SANGRE":I[10],"FECHA":I[6]})
    return A
@app.get('/api/a_v/{id_doctor}/{id_c}')
def a_c(id_doctor:str,id_c:str):
    A=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM CONSULTA WHERE ID_DOCTOR='"+id_doctor+"' AND ID_CONSULTA='"+id_c+"'")
    conexion.commit()
    datos=registro.fetchall()
    for I in datos:
        A.append({"ID":I[0],"FECHA":I[7],"SEGURO":I[8],"MOTIVO":I[9],"DIAG":I[10],"NOTA":I[11],"MONTO":I[12]})
    return A
@app.get('/api/a_p/{id_doctor}/{id_p}')
def a_p(id_doctor:str,id_p:str):
    A=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM PACIENTE WHERE ID_DOCTOR ='"+id_doctor+"' AND ID_PACIENTE='"+id_p+"'")
    conexion.commit()
    datos=registro.fetchall()
    for I in datos:
        A.append({"ID":I[0],"CEDULA":I[1],"NOMBRE":I[2],"APELLIDO":I[3],"EMAIL":I[4],"SEXO":I[5],"ALERGIAS":I[7],"SANGRE":I[10]})
    return A

