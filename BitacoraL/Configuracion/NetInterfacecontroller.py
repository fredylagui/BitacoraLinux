# -*- coding: utf-8 *-*
'''
Created on 16/06/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import pygame
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import NetInterfaceConfigView
import Clases.encriptador
# ------------------------------
# Funcion principal del Programa
""" Controlador de la Interfaz de la Tarjeta de Red"""
# ------------------------------


class NetInterfaceController:
    def __init__(self,sistemaop):
        # Guardamos el SO
        self.sistemaop = sistemaop    
                
        # Instancia para la VISTA
        self.vista = NetInterfaceConfigView.NetInterfaceConfigView(sistemaop)

        if sistemaop == "linux2":
            archivo = "/opt/BitacoraL/src/files/profile4"
        else:
            archivo = "C:/Program Files/Bitacora/src/files/profile4"

        # Configuracion del Objeto a la Instancia de la Clase
        self.lista_tags = ["[Interface]"]
        # Instancia para el Encriptador
        self.encriptador = Clases.encriptador.Encriptador(sistemaop,self.lista_tags,archivo)

        # Cargamos todo lo relacionado a pygame
        pygame.init() 

    """---------------------------------------Metodos-------------------------------------------------------"""
    def crear_interfaz(self):
        self.vista.crear_interfaz()
        
    def actualizar_datos(self):
        "Metodo para Configurar la Interfaz de Red"
        mensaje = ""
        interface = self.vista.t_interfaz.getTxt()
        if interface != "":
            tmp = ""
            for caracter in interface:
                entero = ord(caracter)
                tmp += chr(entero)
            lista_newdata = [tmp]
            self.encriptador.actualizar_archivo(lista_newdata)
            mensaje = "Nombre de Interfaz Actualizado"
        else:
            mensaje = "Ingresar Nombre de Interfaz"
        self.vista.mensaje.update_prompt(mensaje)
        return
            #tmp ="cadena"


    """--------------------------------------Eventos-------------------------------------------------------"""
    def eventos_config(self):
        "Metodo para Los Eventos en la Vista de la Tarjeta de Red"
        res = ""
        band_write = 1
        while True:
            # Empezamos a capturar la lista de Eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.vista.mensaje.update_prompt("")                    
                    # Dependiendo de la zona donde se hizo click se realiza una accion
                    x, y = event.pos
                    if x>= 45 and x <= 295 and y >= 75 and y<= 100:
                        # Click en Textbox usuario
                        band_write = 1
                    
                    elif self.vista.actualizar.collidepoint(x, y):
                        # Click en Boton Actualizar
                        self.actualizar_datos()

                    elif self.vista.regresar.collidepoint(x, y):
                        # Click en Boton Regresar
                        return
                    else:
                        band_write = 0
                    
            if band_write == 1:
                # Se ingresan datos en el TextBox de la Interfaz de Red
                self.vista.t_interfaz.update(events,self.sistemaop)
            self.vista.surface()
            self.vista.refresh_display()