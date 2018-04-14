# -*- coding: cp1252 -*-
import vtk, qt, ctk, slicer
##import os
##from slicer.ScriptedLoadableModule import *
##import logging

#Este bloque genera los textos de ayuda y de autores, adem�s le da el nombre
#al m�dulo ("Registro") y la categor�a("Pr�ctica 3")
class INTER:
  def __init__(self, parent):
    parent.title = "Registro" 
    parent.categories = ["Practica_3"]
    parent.dependencies = []
    parent.contributors = ["Luis David Cardona, Luz Bandy Naranjo (Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
    Pr�ctica 3, procesamiento digital de im�genes, 2017-2.
    Este m�dulo permite la selecci�n de un volumen 4D previamente cargado en Slicer 3D que registra todos los dem�s vol�menes cargados.
    """
    parent.acknowledgementText = """
    Este m�dulo fue desarrollado por Luis David Cardona y Luz Bandy Naranjo, para la materia Procesamiento digital de im�genes en el 2017-2
""" 
    self.parent=parent
class INTERWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):

    w = qt.QWidget();
    layout = qt.QGridLayout();
    w.setLayout(layout);
    self.layout.addWidget(w);
    w.show();
    self.layout = layout;

   
