#!/usr/bin/env python
# -*- coding: utf-8 *-*
'''
Created on 30/04/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import argparse
import sys
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
# ------------------------------
# Funcion principal
# ------------------------------
"Busqueda de Caracteres Especiales y se Borran"

class cleaner():
    def __init__ (self,file):
        "Init de la Clase"
        # Archivo de Entrada
        self.file = file
        
        # Archivo de Salida
        self.fileN = file+".tmp"
        
        # Apuntador al Archivo de Entrada
        self.f = None
        
        # Apuntador al Archivo de Salida
        self.fN = None
        
        # Modos de Abrir el Archivo
        self.modo_lectura = 'r'
        self.modo_escritura = 'w'        
        
        # Rangos Aceptados de Caracteres (Min,Max)
        self.text = (32,126)
        # Valores a Considerar
        self.especiales = (10)
        
        print "Se inicializo correctamente el Objeto Cleaner"
        
    def abrir_archivo(self):
        "Metodo para Abrir el Archivo"
        try:
            self.f = open(self.file,self.modo_lectura)
            print "Se Abre Archivo Entrada"
        except (Exception), e:
            print "****Error Al abrir el Archivo ",str (self.file)
            print "Tipo de Error:"
            print e
            sys.exit(2)

    def crear_archivo(self):
        "Metodo para Abrir el Archivo"
        try:
            self.fN = open(self.fileN,self.modo_escritura)
            print "Se Abre Archivo de Salida"
        except (Exception), e:
            print "****Error Al abrir el Archivo ",str (self.fileN)
            print "Tipo de Error:"
            print e
            sys.exit(2)
        
    def crear_contenido(self):
        "Metodo para crear el Nuevo archivo"
        linea_nueva = ""
        try:
            # Leemos todo el Archivo hasta encontrar la ultima linea
            linea = self.f.readline()
            contador = 1
            while linea!="":
                print "(", contador,") ",linea
                for caracter in linea:
                    value = int (ord(caracter))
                    if value >= 32 and value <= 126 or value == 10:
                        linea_nueva += caracter
                        print "[",str(value) ,"]", value
                    else:
                        print "[",str(value) ,"]", value , "<- *** ATENCION ***"
                print "Linea Nueva: ",linea_nueva
                self.fN.write(linea_nueva)                
                linea_nueva = ""
                linea = self.f.readline()
                contador+=1
                
            # Obtenemos el Ultimo ID respaldado
            print "****Se Leyo todo El Archivo"
        except (Exception), e:
            print "****Error al Leer El Archivo"
            print "Tipo de Error:"
            print e
        self.f.close()
        

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Backup de la Base de Datos kabl.')
    parser.add_argument('-f',   '--file', default='no_string', help='Nombre del Archivo', metavar='file.py')
    args = vars(parser.parse_args())    

    if args['file'] != 'no_string':
        print "Parametro Valido"
        file =  str(args['file'])
        limpiador = cleaner(file)
        limpiador.abrir_archivo()
        limpiador.crear_archivo()
        limpiador.crear_contenido()
        sys.exit()
