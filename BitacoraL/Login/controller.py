# -*- coding: utf-8 *-*
#!/usr/bin/env python
'''
Created on 28/01/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import os
import sys
import pygame
from pygame.locals import *
from datetime import datetime
import socket
# -----------
# Constantes
# -----------
apagarL = "shutdown -h now"
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import model
import LoginView
import Clases.filtro
import Clases.ifconfig
import Clases.encriptador
# ------------------------------
# Funcion principal del Programa
""" Controlador del Login"""
# ------------------------------


class controlador:
    
    def __init__(self,sistemaop,usuario):
        # Guardamos la instancia del objeto Usuario
        self.usuario = usuario
        
        # Guardamos el SO
        self.sistemaop = sistemaop        

        # Instancia a la Clase Encriptador
        self.lista_tags = ("")
        self.archivo = ""
        
        self.encriptador = Clases.encriptador.Encriptador(self.sistemaop,self.lista_tags,self.archivo)

        # Definimos los Tags para cada Archivo a usar por el Encriptador
        self.tags_super = ("[user]","[pwd]")
        self.tags_admin = ("[user]","[pwd]")
        self.tags_db = ("[host]","[port]","[user]","[pwd]","[db]")
        
        if sistemaop == "linux2":
            self.archivo = "/opt/BitacoraL/src/files/profile3"
        else:
            self.archivo = "C:/Program Files/Bitacora/src/files/profile3"
        self.encriptador.actualizar_nombre_archivo(self.archivo)
        self.encriptador.actualizar_lista_tags(self.tags_db)
        
        d = self.encriptador.leer_datos()
        
        # Instancia para el Modelo
        self.modelo = model.modelo(d)

        # Instancia para la VISTA
        self.vista = LoginView.LoginView(sistemaop,usuario)
        
        # Diccionario con los Tipos de Usuario del Sistema
        self.tipo_usuarios = {"profesor":"prof","asistente":"asist","alumno":"alum","administrador":"admin"}
        
        # Instancia a la Clase filtro
        self.filtro = Clases.filtro.filtro()
        
        # Cargamos todo lo relacionado a pygame
        pygame.init()        
        
    """---------------------------------------Metodos-------------------------------------------------------"""
    def crear_interfaz(self):
        "Metodo para llamar todos los componentes para crear la Vista"
        self.vista.crear_interfaz()
        
    def configurar_inicio(self):
        "Se prepara todo para el Inicio de la Aplicacion"
        # Reseteamos los Imputs de la Vista
        self.vista.reset_inputs()
        
        # Reseteamos la Informacion del Usuario
        self.usuario.reset_usuario()

    def obtener_IP(self):
        "Se Obtiene la IP del Equipo por medio del hostname"
        # Creamos la instancia a la Clase ifconfig
        ob_ifconfig = Clases.ifconfig.ifconfig(self.sistemaop)
        ob_ifconfig.crear_archivo()
        # Obtenemos la IP del Equipo
        ob_ifconfig.guardar_ip()
        ip = ob_ifconfig.get_IP()
        if ip == "0.0.0.0":
            return "FALIED_GET_IP"
        else:
            self.usuario.set_IP(ip)
            return "SUCCESS"
    
    def obtener_Hora_Servidor(self):
        "Se Verifica la Hora del Servidor"
        consulta,edo_consulta = self.modelo.hora_sistema()
        if edo_consulta == "SUCCESS":
            self.usuario.set_hora_inicio(consulta[0][0])
        return edo_consulta

    def registrar_inicio (self):
        "Se Registra el Inicio de Sesion"
        return self.modelo.registrar_inicio(self.usuario.clvUsu,self.usuario.hora_inicio,self.usuario.IP_Equipo)

    def ingresar_sistema(self):
        "Metodo para El Ingreso del Usuario"
        # Tipo de Acceso
        access = "Login"
        mensaje = ""
        res = ""
        
        # Se valida el Usuario ingresado
        res = self.validar_usuario(self.vista.usuario.getTxt(), self.vista.pwd.getTxt())
        # Si el usuario es el Admin se cierra la Aplicacion
        if res == "super":
            print "Usuario Super"
            sys.exit(0)
        elif res == "Config":
            print "Usuario Config"
            access = "Config"
        elif res == "SUCCESS":
            # Si el Usuario es valido
            respuesta = self.obtener_IP()
            if respuesta == "FALIED_GET_IP":
                mensaje = "Fallo Al Obtener la IP del Equipo"
                access = "Login"
            else:
                respuesta = self.obtener_Hora_Servidor()
                if respuesta == "FAILED_GET_HOUR":
                    mensaje = "Hora No Valida"
                    access = "Login"
                else:
                    respuesta = self.registrar_inicio()
                    if respuesta == "FAILED_QUERY_REGISTER":
                        mensaje = "No se Realizo el Inicio de Sesion"
                        access = "Login"
                    else:
                        # Se Realizo Correctamente el Inicio de Sesion
                        mensaje = ""
                        access = "Usuario"
        elif res == "USER_NO_VALIDO":
            # Si el Usuario no es valido se manda mensaje a la Ventana
            mensaje =  "Usuario o Pwd no valido"
            access = "Login"
        elif res == "FAILED_VALIDATE":
            # Fallo Al realizar la Consulta
            "Fallo en Realizar Consulta"
            mensaje = "No se puede Consultar el Usuario"
            access = "Login"
        self.vista.mensaje.update_prompt(mensaje)
        return access

    def validar_usuario(self,usuario,pwd):
        "Click en Boton Iniciar Sesion"
        # Se obtienen los datos ingresados en el formulario de Logeo
        self.usuario.usuario = self.filtro.filtrar_cadena(usuario) 
        self.usuario.pwd = self.filtro.filtrar_cadena(pwd)
        
        if self.sistemaop == "linux2":
            self.archivo = "/opt/BitacoraL/src/files/profile1"
        else:
            self.archivo = "C:/Program Files/Bitacora/src/files/profile1"
        self.encriptador.actualizar_nombre_archivo(self.archivo)
        self.encriptador.actualizar_lista_tags(self.tags_super)
        d = self.encriptador.leer_datos()
        # Se compara el usuario y pwd ingresado con los del Super Usuario
        #return "Config"
        if self.usuario.usuario == d[0] and self.usuario.pwd == d[1]:
            return "super"
        else:
            if self.sistemaop == "linux2":
                self.archivo = "/opt/BitacoraL/src/files/profile2"
            else:
                self.archivo = "C:/Program Files/Bitacora/src/files/profile2"
            self.encriptador.actualizar_nombre_archivo(self.archivo)
            self.encriptador.actualizar_lista_tags(self.tags_super)
            d = self.encriptador.leer_datos()
            acceso_root = self.usuario.get_user_unix()
            if self.usuario.usuario == d[0] and self.usuario.pwd == d[1] and acceso_root == True:
                return "Config"
            else:
                # Buscamos en Cada Tipo de Usuario los Datos Ingresados
                for key in self.tipo_usuarios.keys():
                    if self.tipo_usuarios[key] == "alum":
                        # Primero se verifica que sea un Alumno
                        consulta,edo_consulta = self.modelo.validar_usuario_alumno(self.usuario.usuario,self.usuario.pwd)
    
                    elif self.tipo_usuarios[key] == "asist":
                        # Se verifica que sea un Asistente
                        consulta,edo_consulta = self.modelo.validar_usuario_tecaux(self.usuario.usuario,self.usuario.pwd)
    
                    elif self.tipo_usuarios[key] == "prof":
                        # Se verifica que sea un Profesor 
                        consulta,edo_consulta = self.modelo.validar_usuario_profesor(self.usuario.usuario,self.usuario.pwd)
                        
                    # Si la Consulta Falla enviamos el Mensaje a la Vista
                    if edo_consulta == "FAILED_VALIDATE":
                        return edo_consulta
                    else:
                        if len(consulta) > 0:
                            for registro in consulta:
                                print self.tipo_usuarios[key]                            
                                # Guardamos la informacion recibida desde la BD
                                if self.tipo_usuarios[key] == "alum":
                                    nombre_usuario = registro[1]+' '+registro[2]+' '+registro[3]
                                    #self.usuario.guardar_datos(tipo_usuario,nombre,apePat,apeMat,graAca,clvUsu,nombre_usuario)
                                    self.usuario.guardar_datos(self.tipo_usuarios[key],registro[1],registro[2],registro[3],"",registro[0],nombre_usuario)
                                elif self.tipo_usuarios[key] == "prof" or self.tipo_usuarios[key] == "asist":
                                    nombre_usuario = registro[4]+' '+registro[1]+' '+registro[2]+' '+registro[3]
                                    #self.usuario.guardar_datos(tipo_usuario,nombre,apePat,apeMat,graAca,clvUsu,nombre_usuario)
                                    self.usuario.guardar_datos(self.tipo_usuarios[key],registro[1],registro[2],registro[3],registro[4],registro[5],nombre_usuario)
                            break
                            
        if len(consulta) > 0:
            return edo_consulta
        else:
            return "USER_NO_VALIDO"
        
    def ApagarEquipo(self):
        "Click en Boton Apagar Equipo"
        os.system(apagarL)
            
    """--------------------------------------Eventos-------------------------------------------------------"""
    def eventos_loginview(self):
        "Metodo para Los Eventos en la Vista Login"
        # Iniciamos con el foco en el textbox del Usuario
        band_write = 1
        
        while True:
            # Empezamos a capturar la lista de Eventos
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    # Para iterar entre los dos TextBox de Usuario y Pwd
                    if event.key == pygame.K_TAB:
                        #print "Click en tecla TAB"
                        if band_write < 2:
                            band_write += 1
                        elif band_write == 2:
                            band_write = 1
                    if event.key == K_KP_ENTER or event.key == K_RETURN:
                        #Click en Tecla Enter
                        access = self.ingresar_sistema()
                        if access == "Usuario" or access == "Config":
                            return access
        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Borramos Mensaje para el Usuario
                    self.vista.mensaje.update_prompt("")

                    # Dependiendo de la zona donde se hizo click se realiza una accion 
                    x, y = event.pos
                    #if x>= 505 and x <= 755 and y >= 360 and y<= 385:
                    if x>= 610 and x <= 800 and y >= 428 and y<= 452:
                        # Click en Textbox usuario
                        band_write = 1
                    #elif x>= 505 and x <= 755 and y >= 410 and y<= 440:
                    elif x>= 610 and x <= 800 and y >= 480 and y<= 504:
                        # Click en Textbox pwd
                        band_write = 2
                    elif self.vista.entrar.collidepoint(x, y):
                        # Click en Boton Entrar
                        access = self.ingresar_sistema()
                        if access == "Usuario" or access == "Config":
                            return access
        
                    elif self.vista.apagar.collidepoint(x, y):
                        # Click en Boton Apagar
                        self.controlador.ApagarEquipo()

            if band_write == 1:
                # Se ingresan datos en el TextBox del Usuario
                self.vista.usuario.update(events,self.sistemaop)
            elif band_write == 2:
                # Se ingresan datos en el TextBox del Pwd
                self.vista.pwd.update(events,self.sistemaop)

            self.vista.surface()
            self.vista.refresh_display()