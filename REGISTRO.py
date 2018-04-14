# -*- coding: cp1252 -*-
import vtk, qt, ctk, slicer
try:
  NUMPY_AVAILABLE = True
  import vtk.util.numpy_support
except:
  NUMPY_AVAILABLE = False
from MultiVolumeImporterLib.Helper import Helper
##import os
##from slicer.ScriptedLoadableModule import *
##import logging

#Este bloque genera los textos de ayuda y de autores, además le da el nombre
#al módulo ("Registro") y la categoría("Práctica 3")
class REGISTRO:
  def __init__(self, parent):
    parent.title = "Registro" 
    parent.categories = ["Procesamiento"]
    parent.dependencies = []
    parent.contributors = ["Yulieth Katerine Muñoz Zapata, John Fredy Ochoa, Mateo Ramirez(Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
    P
    Este módulo permite la selección de un volumen 4D previamente cargado en Slicer 3D que registra todos los demás volúmenes cargados.
    """
    parent.acknowledgementText = """
    
""" 
    self.parent=parent
class REGISTROWidget:
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
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)

    # Conexiones necesarias para el algoritmo
    #entrega al algoritmo el volumen 4D de entrada y conecta la función del botón
    #con la ejecución del registro
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
##    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

###Selector de volumen donde se guardara el volumen de la direccion
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    parametersFormLayout.addRow("Output node:", self.outputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.outputSelector, 'setMRMLScene(vtkMRMLScene*)')  



    # Add vertical spacer
##    self.layout.addStretch(1)

    # Refresh Apply button state
##    self.onSelect()

  def cleanup(self):
    pass

##  def onSelect(self):
##    self.applyButton.enabled = self.inputSelector.currentNode()
##    self.applyButton.enabled = self.outputSelector.currentNode()

##  def onApplyButton(self):
##    logic = REGISTROLogic()
##    logic.run(self.inputSelector.currentNode())
##
##
##class REGISTROLogic:
##  
  def onApplyButton(self):
    mvNode = self.outputSelector.currentNode()
    inputVolume= self.inputSelector.currentNode()
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
    volumenSalida = slicer.vtkMRMLMultiVolumeNode()
    
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
    frameLabelsAttr=''
    frames = []
    volumeLabels = vtk.vtkDoubleArray()
    
    volumeLabels.SetNumberOfTuples(numero_imagenes)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_imagenes)
    
    for i in range(numero_imagenes):
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
      frames.append(volumenMovil)
##      parameters['outputVolume']=volumenSalida.GetID()
      #Realizo el registro
      cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
      #obtengo la transformada lineal que se usó en el registro
      transformada=escena.GetFirstNodeByName('Transformadaderegistro'+str(i+1))
      #Obtengo la matriz de la transformada, esta matriz es de dimensiones 4x4
      #en la cual estan todos los desplazamientos y rotaciones que se hicieron
      #en la transformada, a partir de ella se obtienen los volumenes que se
      #desplazaron mas de 4mm en cualquier direccion
      
      frameId = i;
      volumeLabels.SetComponent(i, 0, frameId)
      frameLabelsAttr += str(frameId)+','


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
    print("MovilExtent: "+str(volumenMovil.GetImageData().GetExtent()))
##    print("valor de f: "+ str(volumenMovil))
    frameLabelsAttr = frameLabelsAttr[:-1]


    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumenMovil.GetImageData().GetExtent())##Se le asigna la dimensión del miltuvolumen   
    mvImage.AllocateScalars(volumenMovil.GetImageData().GetScalarType(), numero_imagenes)##Se le asigna el tipo y número de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen

    mat = vtk.vtkMatrix4x4()

    ##Se hace la conversión y se obtiene la matriz de transformación del nodo
    volumenMovil.GetRASToIJKMatrix(mat)
    mvNode.SetRASToIJKMatrix(mat)
    volumenMovil.GetIJKToRASMatrix(mat)
    mvNode.SetIJKToRASMatrix(mat)

    print("frameId: "+str(frameId))
    print("# imag: "+str(numero_imagenes))
##    print("Long frame1: "+str(len(frame)))
    print("Long frames: "+str(len(frames)))

## 
    for frameId in range(numero_imagenes):
      # TODO: check consistent size and orientation!
      frame = frames[frameId]
      frameImage = frame.GetImageData()
      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
      mvImageArray.T[frameId] = frameImageArray

##Se crea el nodo del multivolumen
    
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
    mvNode.SetAndObserveImageData(mvImage)
    mvNode.SetNumberOfFrames(numero_imagenes)

    mvNode.SetLabelArray(volumeLabels)
    mvNode.SetLabelName('na')
    mvNode.SetAttribute('MultiVolume.FrameLabels',frameLabelsAttr)
    mvNode.SetAttribute('MultiVolume.NumberOfFrames',str(numero_imagenes))
    mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagName','NA')
    mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagUnits','na')

    mvNode.SetName('MultiVolume Registrado')
    Helper.SetBgFgVolumes(mvNode.GetID(),None)
    

    
    print('Registro completo')
    #al terminar el ciclo for con todos los volúmenes registrados se genera una
    #ventana emergente con un mensaje("Registro completo!") y mostrando los
    #volúmenes que se desplazaron mas de 4mm
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Registro completo!\nVolumenes con movimiento mayor a 4mm:\n'+str(v))
    return True

