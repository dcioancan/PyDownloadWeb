#!/usr/bin/python
# -*- coding: utf-8 -*-
#dcioancan - 2014
 
import sys
import os
import threading
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog

# Cargar nuestro archivo .ui
form_class = uic.loadUiType("Main.ui")[0]

class MyWindowClass(QtGui.QMainWindow, form_class):
  def __init__(self, parent=None):
    QtGui.QMainWindow.__init__(self, parent)
    self.setupUi(self)
    self.btn_descargar.clicked.connect(self.btn_descargar_clicked)
    self.btn_seleccionar.clicked.connect(self.btn_seleccionar_clicked)
    self.btn_detener.clicked.connect(self.btn_detener_clicked)
 
  # Evento del boton
  def btn_descargar_clicked(self):
    if self.led_url.text() != "" :
      comando = self.generarComando()
      w = threading.Thread(target=self.ejecutarComando, args=(comando,)).start()
          
    else:
      QtGui.QMessageBox.information(self, "URL Vacia", "Debe ingresar la URL del sitio web que desea descargar.", QtGui.QMessageBox.Ok)

  def btn_seleccionar_clicked(self):  
    path = QFileDialog.getExistingDirectory(self,"Seleccione una carpeta", "/home/")
    self.led_destino.setText(path)
    print path
  
  def btn_detener_clicked(self):
    t = threading.Thread(target=self.ejecutarComando, args=("kill $(pidof wget)",)).start()

  def generarComando(self):
    output = "wget "
   
    #Pausa 20 sec  
    if self.cbx_w.isChecked():
      output += " --wait=20"

    #Liminar ratio de descarga  
    if self.cbx_l.isChecked():
      output += " --limit-rate=20K"
      
    #recursivo
    if self.cbx_r.isChecked():
      output += " -r"    

    #Prerequisitos  
    if self.cbx_p.isChecked():
      output += " -p"

    #Enlaces  
    if self.cbx_k.isChecked():
      output += " -k"

    #User Agent  
    if self.cbx_u.isChecked():
      output += " -U Mozilla"
    
    output += " -nv " + self.led_url.text() + " -P " + self.led_destino.text()
    return output

  def ejecutarComando(self, comando):
    print str(comando)
    os.system(str(comando))
    
app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()