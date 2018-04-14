# -*- coding: cp1252 -*-
import vtk, qt, ctk, slicer
##import os
##from slicer.ScriptedLoadableModule import *
##import logging

#Este bloque genera los textos de ayuda y de autores, además le da el nombre
#al módulo ("Registro") y la categoría("Práctica 3")
class REGISTRO2:
  def __init__(self, parent):
    parent.title = "Registro" 
    parent.categories = ["Practica_3"]
    parent.dependencies = []
    parent.contributors = ["Luis David Cardona, Luz Bandy Naranjo (Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
    Práctica 3, procesamiento digital de imágenes, 2017-2.
    Este módulo permite la selección de un volumen 4D previamente cargado en Slicer 3D que registra todos los demás volúmenes cargados.
    """
    parent.acknowledgementText = """
    Este módulo fue desarrollado por Luis David Cardona y Luz Bandy Naranjo, para la materia Procesamiento digital de imágenes en el 2017-2
""" 
    self.parent=parent
class REGISTRO2Widget:
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

    ##    # Se crea una sección de parámetros en una pestaña desplegable
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parametros"
    self.layout.addWidget(parametersCollapsibleButton)

    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)


    #Se crea una ventana desplegable en la cual se ingresa el volumen 4D de
    #entrada que se quiere registrar, este volumen debe ser de tipo
    #"vtkMRMLMultiVolumeNode", además si se tienen varios multivolumenes cargados
    #se puede elegir entre ellos el que se desea registrar
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = True
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = True
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Volumen 4D: ", self.inputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputSelector, 'setMRMLScene(vtkMRMLScene*)')


    # Botón de Registro
    #Este botón solo se activa si el multivolumen ha sido seleccionado en la
    #ventana desplegable de Volumen 4D. Al presionarlo, el algoritmo
    #realiza el registro de los diferentes volumenes en el volumen 4D
    self.applyButton = qt.QPushButton("Registrar")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # Conexiones necesarias para el algoritmo
    #entrega al algoritmo el volumen 4D de entrada y conecta la función del botón
    #con la ejecución del registro
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode()

  def onApplyButton(self):
    logic = REGISTROLogic()
    logic.run(self.inputSelector.currentNode())


class REGISTROLogic:
  
  def run(self, inputVolume):
    """
    Run the actual algorithm
    """
    #se obtiene la escena y se obtiene el volumen 4D a partir del Volumen 4D de
    #entrada de la ventana desplegable
    escena = slicer.mrmlScene
    imagenvtk4D = inputVolume.GetImageData()
    #Se obtiene el número de volúmenes que tiene el volumen 4D
    numero_imagenes = inputVolume.GetNumberOfFrames()
    print('imagenes: ' + str(numero_imagenes))
    #filtro vtk para descomponer un volumen 4D
    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(imagenvtk4D)
    #matriz de transformación
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    #le solicitamos al volumen original que nos devuelva sus matrices
    inputVolume.GetRASToIJKMatrix(ras2ijk)
    inputVolume.GetIJKToRASMatrix(ijk2ras)
    #creo un volumen nuevo
    volumenFijo = slicer.vtkMRMLScalarVolumeNode()
    volumenSalida = slicer.vtkMRMLScalarVolumeNode()
    #le asigno las transformaciones
    volumenFijo.SetRASToIJKMatrix(ras2ijk)
    volumenFijo.SetIJKToRASMatrix(ijk2ras)
    #le asigno el volumen 3D fijo
    imagen_fija = extract1.SetComponents(0)
    extract1.Update()
    volumenFijo.SetName('fijo')
    volumenFijo.SetAndObserveImageData(extract1.GetOutput())
    #anado el nuevo volumen a la escena
    escena.AddNode(volumenFijo)
    #se crea un vector para guardar el número del volumen que tenga un
    #desplazamiento de mas de 4mm en cualquier dirección
    v=[]

    #se hace un ciclo for para registrar todos los demás volúmenes del volumen 4D
    #con el primer volumen que se definió como fijo
    for i in range(numero_imagenes-1):
      # extraigo la imagen móvil en la posición i+1 ya que el primero es el fijo
      imagen_movil = extract1.SetComponents(i+1) #Seleccionar un volumen i+1
      extract1.Update()
      #Creo el volumen móvil, y realizo el mismo procedimiento que con el fijo
      volumenMovil = slicer.vtkMRMLScalarVolumeNode();
      volumenMovil.SetRASToIJKMatrix(ras2ijk)
      volumenMovil.SetIJKToRASMatrix(ijk2ras)
      volumenMovil.SetAndObserveImageData(extract1.GetOutput())
      volumenMovil.SetName('movil '+str(i+1))
      escena.AddNode(volumenMovil)
      #creamos la transformada para alinear los volúmenes
      transformadaSalida = slicer.vtkMRMLLinearTransformNode()
      transformadaSalida.SetName('Transformadaderegistro'+str(i+1))
      slicer.mrmlScene.AddNode(transformadaSalida)
      #parámetros para la operación de registro
      parameters = {}
      #parameters['InitialTransform'] = transI.GetID()
      parameters['fixedVolume'] = volumenFijo.GetID()
      parameters['movingVolume'] = volumenMovil.GetID()
      parameters['transformType'] = 'Rigid'
      parameters['outputTransform'] = transformadaSalida.GetID()
      parameters['outputVolume']=volumenSalida.GetID()
      #Realizo el registro
      cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
      #obtengo la transformada lineal que se usó en el registro
      transformada=escena.GetFirstNodeByName('Transformadaderegistro'+str(i+1))
      #Obtengo la matriz de la transformada, esta matriz es de dimensiones 4x4
      #en la cual estan todos los desplazamientos y rotaciones que se hicieron
      #en la transformada, a partir de ella se obtienen los volumenes que se
      #desplazaron mas de 4mm en cualquier direccion
      
      Matriz=transformada.GetMatrixTransformToParent()

            
      LR=Matriz.GetElement(0,3)#dirección izquierda o derecha en la fila 1, columna 4
      PA=Matriz.GetElement(1,3)#dirección anterior o posterior en la fila 2, columna 4
      IS=Matriz.GetElement(2,3)#dirección inferior o superior en la fila 3, columna 4
      #Se mira si el volumen "i" en alguna dirección tuvo un desplazamiento
      #mayor a 4mm, en caso de ser cierto se guarda en el vector "v"
      if abs(LR)>4:
        v.append(i+2)
      elif abs(PA)>4:
        v.append(i+2)
      elif abs(IS)>4:
        v.append(i+2)
    print('Registro completo')
    #al terminar el ciclo for con todos los volúmenes registrados se genera una
    #ventana emergente con un mensaje("Registro completo!") y mostrando los
    #volúmenes que se desplazaron mas de 4mm
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Registro completo!\nVolumenes con movimiento mayor a 4mm:\n'+str(v))
    return True

