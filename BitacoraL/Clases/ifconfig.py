# -*- coding: utf-8 *-*
'''
Created on 27/03/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import re
import os
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import encriptador
# ------------------------------
# Funcion principal del Programa
""" Controlador de la Interfaz de la Tarjeta de Red"""
# ------------------------------

class ifconfig():
    def __init__(self,sistemaop):
        "Clase para Llamar a ifconfig y obtener IP de Tarjeta de Red"

        if sistemaop == "linux2":
            archivo = "/opt/BitacoraL/src/files/profile4"
        else:
            archivo = "C:/Program Files/Bitacora/src/files/profile4"

        # Configuracion del Objeto a la Instancia de la Clase
        self.lista_tags = ["[Interface]"]

        # Instancia para el Encriptador
        self.encriptador = encriptador.Encriptador(sistemaop,self.lista_tags,archivo)        
        # Guardamos La interfaz de Red 
        tmp = self.encriptador.leer_datos()
        self.interfaz = tmp[0]
        
        self.ip = "0.0.0.0"
        if sistemaop == "linux2":
            self.archivo = "/tmp/ifconfig.txt"
        else:
            self.archivo = "Clases/ifconfig.txt"
            
    def guardar_ip(self):
        f = self.abrir_archivo(self.archivo, "r")
        if f is None:
            print "No se Pudo Abrir el Archivo"
        else:
            find_interfaz = 0
            try:
                # Leemos todo el Archivo hasta encontrar la ultima linea
                linea = f.readline()
                while linea!="":
                    if linea.find(self.interfaz) >= 0:
                        # Habilitamos Bandera de haber encontrado el Dispositivo de Red
                        linea = f.readline()
                        if linea.find("inet") >=0: 
                            tmp = re.search(' addr:(\d+\.\d+.\d+.\d+)', linea)
                            if tmp:
                                tmp2 = tmp.group()
                                self.ip = tmp2[tmp2.find(':')+1:]
                                break
                        else:
                            print "No Encontramos Inet Buscamos mas adelante"
                            linea = f.readline()
                    linea = f.readline()
            except (Exception), e:
                print "****Error al leer Archivo ifconfig.txt"
                print "Tipo de Error:"
                print e
            f.close() 
        
    def crear_archivo(self):
        "Metodo para Llamar a la funcion  ifconfig y guardar su salida en un archivo"
        os.system("clear")
        os.system("ifconfig > /tmp/ifconfig.txt")        
        
    def abrir_archivo(self,archivo,modo):
        "Metodo para Abrir un Archivo"
        try:
            f = open(archivo,modo)
        except (Exception), e:
            print "Error al Abrir el Archivo"
            print "Tipo de Error:"
            print e
            f = None
        return f

    def get_IP(self):
        return self.ip

if __name__ == "__main__":
    seg = ifconfig()
    seg.guardar_ip()