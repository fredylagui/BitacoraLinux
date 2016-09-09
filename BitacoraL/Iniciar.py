#!/usr/bin/env python
# -*- coding: utf-8 *-*
'''
Created on 08/04/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
#import logging
import sys
#sys.path.append("..")
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import Main
# ------------------------------
# Funcion principal de la Aplicacion
# ------------------------------
"Script de Inicio para la Aplicacion"

if __name__ == "__main__":
    sistemaop = sys.platform
    # Se imprime Codificacion Usada
    if sistemaop == "win32":
        print sys.getdefaultencoding()
    elif sistemaop == "linux2":
        reload(sys)
        print sys.getdefaultencoding()
    inicio = Main.Main()
    inicio.main()
    inicio.iniciar()
