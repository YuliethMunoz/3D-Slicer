import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
try:
  NUMPY_AVAILABLE = True
  import vtk.util.numpy_support
except:
  NUMPY_AVAILABLE = False
from MultiVolumeImporterLib.Helper import Helper

#
# HelloPython
#

class Registro_Imagenes(ScriptedLoadableModule):


  def __init__(self, parent):
    
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Registro"
    self.parent.categories = ["PDI"]
    self.parent.dependencies = []
    self.parent.contributors = ["Paula Morales, Katerine Munoz"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
""" 

class Registro_ImagenesWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    ScriptedLoadableModuleWidget.setup(self)

    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)


    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.inputSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.inputSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    parametersFormLayout.addRow("Node:", self.inputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputSelector, 'setMRMLScene(vtkMRMLScene*)')  

    self.typeComboBox=ctk.ctkComboBox()
##    self.typeComboBox.caption='Tipo de registro'
    self.typeComboBox.addItem('Rigid')
    self.typeComboBox.addItem('BSpline')
    self.typeComboBox.addItem('Affine')
    self.typeComboBox.addItem('Rigid-BSpline')
    self.typeComboBox.addItem('Rigid-Affine')
    parametersFormLayout.addRow('Tipo de registro:', self.typeComboBox)  



##Boton Registro
    self.buttonRegister = qt.QPushButton("Registrar")
    self.buttonRegister.toolTip = "Run the algorithm."
    self.buttonRegister.enabled = True
    parametersFormLayout.addRow(self.buttonRegister)

    self.buttonRegister.connect('clicked(bool)', self.registrarButton)
    ##self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

  def registrarButton(self):
    Tipo_registro=self.typeComboBox.currentText
    mvNode = slicer.vtkMRMLMultiVolumeNode()
    slicer.mrmlScene.AddNode(mvNode)
    escena = slicer.mrmlScene;
    volumen4D = self.inputSelector.currentNode()
    imagenvtk4D = volumen4D.GetImageData()
    numero_imagenes = volumen4D.GetNumberOfFrames()
    print('imagenes: ' + str(numero_imagenes))
    #filtro vtk para descomponer un volumen 4D
    #matriz de transformacion
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()  
    #le solicitamos al volumen original que nos devuelva sus matrices
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)
    
    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(imagenvtk4D)
##    print(extract1)
    
    #creo un volumen nuevo
    volumenFijo = slicer.vtkMRMLScalarVolumeNode();
    #le asigno las transformaciones
    volumenFijo.SetRASToIJKMatrix(ras2ijk)
    volumenFijo.SetIJKToRASMatrix(ijk2ras)
    #le asigno el volumen 3D fijo
    extract1.SetComponents(0)
    extract1.Update()
    volumenFijo.SetName('Fijo')
    volumenFijo.SetAndObserveImageData(extract1.GetOutput())
    #anado el nuevo volumen a la escena
    escena.AddNode(volumenFijo)
    
    vol_desp=[]
    

##    volumenSalida = self.volumeSelector.currentNode()
    volumenSalida = slicer.vtkMRMLScalarVolumeNode();
    slicer.mrmlScene.AddNode(volumenSalida)
    j=1;
    bandera=0

    Desp_LR1=0
    Desp_PA1=0
    Desp_IS1=0

    frameLabelsAttr=''
    frames = []
    volumeLabels = vtk.vtkDoubleArray()
    
    volumeLabels.SetNumberOfTuples(numero_imagenes)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_imagenes)
    
    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumenFijo.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumenFijo.GetImageData().GetScalarType(), numero_imagenes)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen

    mat = vtk.vtkMatrix4x4()

    ##Se hace la conversion y se obtiene la matriz de transformacion del nodo
    volumenFijo.GetRASToIJKMatrix(mat)
    mvNode.SetRASToIJKMatrix(mat)
    volumenFijo.GetIJKToRASMatrix(mat)
    mvNode.SetIJKToRASMatrix(mat)
##    
    for i in range(numero_imagenes):
      # extraigo la imagen movil
      extract1.SetComponents(i) #Seleccionar un volumen lejano
      extract1.Update()
      #Creo un volumen movil, y realizamos el mismo procedimiento que con el fijo
      volumenMovil = slicer.vtkMRMLScalarVolumeNode();
      volumenMovil.SetRASToIJKMatrix(ras2ijk)
      volumenMovil.SetIJKToRASMatrix(ijk2ras)
      volumenMovil.SetAndObserveImageData(extract1.GetOutput())
      volumenMovil.SetName('movil')
      escena.AddNode(volumenMovil)
      
##      slicer.util.saveNode(volumenMovil,'volumenMovil'+str(i+1)+'.nrrd')
      
      
      #creamos la transformada para alinear los volumenes
 
      transformadaSalidaBSpline=slicer.vtkMRMLBSplineTransformNode();
      transformadaSalidaBSpline.SetName('Transformada de registro BSpline'+str(i+1))
      slicer.mrmlScene.AddNode(transformadaSalidaBSpline)
    
      transformadaSalidaLinear=slicer.vtkMRMLLinearTransformNode()        
      transformadaSalidaLinear.SetName('Transformada de registro Lineal'+str(i+1))
      slicer.mrmlScene.AddNode(transformadaSalidaLinear)

      
      #parametros para la operacion de registro
      parameters = {}

      
      if Tipo_registro=='Rigid-BSpline':
        parameters['fixedVolume'] = volumenFijo.GetID()
        parameters['movingVolume'] = volumenMovil.GetID()
        parameters['transformType'] = 'Rigid'
        parameters['outputTransform'] = transformadaSalidaLinear.GetID()
        parameters['outputVolume']=volumenSalida.GetID()
      
        cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
        if bandera==0:
          bandera=1
          volumenFijo=volumenSalida
          
        parameters['fixedVolume'] = volumenFijo.GetID()
        parameters['movingVolume'] = volumenSalida.GetID()
        parameters['transformType'] = 'BSpline'
        parameters['outputTransform'] = transformadaSalidaBSpline.GetID()
        parameters['outputVolume']=volumenSalida.GetID()
      
        cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
        slicer.util.saveNode(volumenSalida,'volumenSalida'+str(i+1)+'.nrrd')

        frameImage = volumenSalida.GetImageData()
        frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
        mvImageArray.T[i] = frameImageArray
        
      elif Tipo_registro=='Rigid-Affine':
        
        parameters['fixedVolume'] = volumenFijo.GetID()
        parameters['movingVolume'] = volumenMovil.GetID()
        parameters['transformType'] = 'Rigid'
        parameters['outputTransform'] = transformadaSalidaLinear.GetID()
        parameters['outputVolume']=volumenSalida.GetID()
      
        cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
        
        Matriz=transformadaSalidaLinear.GetMatrixTransformToParent()
        Desp_LR1=Matriz.GetElement(0,3)
        Desp_PA1=Matriz.GetElement(1,3)
        Desp_IS1=Matriz.GetElement(2,3)
        print(Desp_LR1)
        
        if bandera==0:
          bandera=1
          volumenFijo=volumenSalida
          
        
        parameters['fixedVolume'] = volumenFijo.GetID()
        parameters['movingVolume'] = volumenSalida.GetID()
        parameters['transformType'] = 'Affine'
        parameters['outputTransform'] = transformadaSalidaLinear.GetID()
        parameters['outputVolume']=volumenSalida.GetID()
      
        cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
        slicer.util.saveNode(volumenSalida,'volumenSalida'+str(i+1)+'.nrrd')
        
        frameImage = volumenSalida.GetImageData()
        frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
        mvImageArray.T[i] = frameImageArray
        
      elif (Tipo_registro=='Rigid') or (Tipo_registro=='Bspline') or (Tipo_registro=='Affine'):
        
        
        parameters['fixedVolume'] = volumenFijo.GetID()
        parameters['movingVolume'] = volumenMovil.GetID()
        parameters['transformType'] = Tipo_registro
##        parameters['linearTransform'] = transformadaSalidaLinear.GetID()
##        parameters['bsplineTransform'] = transformadaSalidaBSpline.GetID()
        if Tipo_registro=='Bspline':
          parameters['outputTransform'] = transformadaSalidaBSpline.GetID()
        else:
          parameters['outputTransform'] = transformadaSalidaLinear.GetID()
        parameters['outputVolume']=volumenSalida.GetID()

        cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
        
        slicer.util.saveNode(volumenSalida,'volumenSalida'+str(i+1)+'.nrrd')
        print('entre')
        frameImage = volumenSalida.GetImageData()
        frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
        mvImageArray.T[i] = frameImageArray
        
        

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
        
      Matriz=transformadaSalidaLinear.GetMatrixTransformToParent()
      Desp_LR2=Matriz.GetElement(0,3)
      Desp_PA2=Matriz.GetElement(1,3)
      Desp_IS2=Matriz.GetElement(2,3)
      print(Desp_LR2)
      Desp_LR=Desp_LR2+Desp_LR1
      Desp_PA=Desp_PA2+Desp_PA1
      Desp_IS=Desp_IS2+Desp_IS1
      
      if ((abs(Desp_LR)>1) or (abs(Desp_PA)>1) or (abs(Desp_IS)>1)) :
        print(j)
        vol_des='VOLUMEN'+str(i+1)+' Desplazamiento --> LR: '+str(Desp_LR)+' PA: '+str(Desp_PA)+' IS: '+str(Desp_IS);
        vol_desp.append(vol_des)
        
    


    
    print('Registro completo')
    print(vol_desp)
    #al terminar el ciclo for con todos los volumenes registrados se genera una
    #ventana emergente con un mensaje("Registro completo!") y mostrando los
    #volumenes que se desplazaron mas de 4mm
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Registro completo'+str(vol_desp))
    
    return True

##
##cliModule = slicer.modules.brainsfit
##n=cliModule.cliModuleLogic().CreateNode()
##for groupIndex in xrange(0,n.GetNumberOfParameterGroups()):
##  for parameterIndex in xrange(0,n.GetNumberOfParametersInGroup(groupIndex)):
##    print '  Parameter ({0}/{1}): {2} ({3})'.format(groupIndex, parameterIndex, n.GetParameterName(groupIndex, parameterIndex), n.GetParameterLabel(groupIndex, parameterIndex))
##
##
