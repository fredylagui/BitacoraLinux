'''
Created on 14/04/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import pygame
from pygame.locals import *
# -----------
# Constantes
# -----------
S_WIDTH = 480
S_HEIGHT = 250
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import Clases.eztext
# ------------------------------
# Descripcion de la Clase
""" Clase para la Interfaz del Usuario"""
# ------------------------------

class ConfigView():
    def __init__(self,sistemaop):
        "Definimos los Atributos de la Clase"
        # Guardamos el SO
        self.sistemaop = sistemaop
        
        # Cargamos todo lo relacionado a pygame
        pygame.init()
        
        # Cargamos el Tipo de Fuente a Usar
        self.fuente = pygame.font.SysFont("Arial", 14, bold=True, italic=False)
        
    def crear_interfaz(self):
        self.dimencionar_ventana()
        self.cargar_imagenes()
        self.cargar_textbox()
        self.cargar_botones()

    def cargar_imagenes(self):
        "Metodo para Cargar las Imagenes a la Interfaz"
        # Cargamos el fondo y las imagenes para la Ventana UserView
        if self.sistemaop == "linux2":
            imagenconfig_interface = "/opt/BitacoraL/src/images/configuracion.png"
            imagenbConfiguracion = "/opt/BitacoraL/src/images/Entrar.png"
            imagenbCerrar = "/opt/BitacoraL/src/images/Cerrar.png"
            imagenbApagar = "/opt/BitacoraL/src/images/Apagar.png"
        else:
            imagenconfig_interface = "C:/Program Files/Bitacora/src/images/config_submenu.png"
            imagenbConfiguracion = "C:/Program Files/Bitacora/src/images/Entrar.png"
            imagenbCerrar = "C:/Program Files/Bitacora/src/images/Cerrar.png"
            
        self.config_interface = pygame.image.load(imagenconfig_interface).convert()
        self.bsuper_usuario = pygame.image.load(imagenbConfiguracion).convert_alpha()
        self.badmin = pygame.image.load(imagenbConfiguracion).convert_alpha()
        self.bbd = pygame.image.load(imagenbConfiguracion).convert_alpha()
        self.bnet = pygame.image.load(imagenbConfiguracion).convert_alpha()
        self.bmod = pygame.image.load(imagenbConfiguracion).convert_alpha()        
        self.bsalir = pygame.image.load(imagenbCerrar).convert_alpha()
        self.bApagar = pygame.image.load(imagenbApagar).convert_alpha()
        
    def cargar_textbox(self):
        "Metodo para cargar TextBox y Textos a la Interfaz"
        # Cargamos Item para los Mensajes al Usuario
        self.t_super_usuario = Clases.eztext.Input(x=35, y=56, font = self.fuente, maxlength=20, color=(109,110,113), prompt='Configuracion de Administrador')
        self.t_admin = Clases.eztext.Input(x=35, y=95, font = self.fuente, maxlength=20, color=(109,110,113), prompt='Config. de Usuarios con privilegios')
        self.t_bd = Clases.eztext.Input(x=35, y=133, font = self.fuente, maxlength=20, color=(109,110,113), prompt='Configurar Conexion Base de Datos')
        self.t_mod = Clases.eztext.Input(x=35, y=172, font = self.fuente, maxlength=20, color=(109,110,113), prompt='Configurar Modulo Asistencia')  
        self.t_net = Clases.eztext.Input(x=35, y=210, font = self.fuente, maxlength=20, color=(109,110,113), prompt='Configurar Interfaz de Red')              

    def cargar_botones(self):
        "Metodo para cargar Botones a la Interfaz"
        # Cargamos los Botones para la Interfaz
        self.salir = self.bsalir.get_rect(center=(414, 85))
        self.super_usuario = self.bsuper_usuario.get_rect(center=(341, 65))
        self.admin = self.badmin.get_rect(center=(341, 105))
        self.bd = self.bbd.get_rect(center=(341, 142))
        self.mod = self.bmod.get_rect(center=(341, 180))
        self.net = self.bnet.get_rect(center=(341, 220))
        self.Apagar = self.bApagar.get_rect(center=(432, 235))
        

    def dimencionar_ventana(self):
        "Metodo Para Dimencionar la Ventana"
        # Modo Resizable para Usuario
        self.screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Configuracion")

    def refresh_display(self):
        # refresh the display
        pygame.display.flip()
            
    def surface(self):
        "Metodo para Agregar los Surface a la Ventana Usuario"
        self.screen.blit(self.config_interface, (0,0))
        #self.screen.blit(self.bsalir, self.bsalir.get_rect(center=(425, 100)))
        #self.screen.blit(self.bsuper_usuario, self.bsuper_usuario.get_rect(center=(250, 35)))
        #self.screen.blit(self.badmin, self.badmin.get_rect(center=(250, 75)))
        #self.screen.blit(self.bbd, self.bbd.get_rect(center=(250, 115)))
        #self.screen.blit(self.bnet, self.bnet.get_rect(center=(250, 155)))
        #self.screen.blit(self.bmod, self.bmod.get_rect(center=(250, 195)))
        self.t_super_usuario.draw(self.screen)
        self.t_admin.draw(self.screen)
        self.t_bd.draw(self.screen)
        self.t_net.draw(self.screen)
        self.t_mod.draw(self.screen)