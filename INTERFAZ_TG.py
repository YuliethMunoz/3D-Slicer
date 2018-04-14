# -*- coding: cp1252 -*-
##import vtk, qt, ctk, slicer

from __future__ import print_function
import sys, re, os

from __main__ import vtk, qt, ctk, slicer
try:
  NUMPY_AVAILABLE = True
  import vtk.util.numpy_support
except:
  NUMPY_AVAILABLE = False
from MultiVolumeImporterLib.Helper import Helper

#
# MultiVolumeImporter
#

class INTERFAZ_TG:
  def __init__(self, parent):
    parent.title = "INTERFAZ" 
    parent.categories = ["Procesamiento"]
    parent.dependencies = []
    parent.contributors = ["Yulieth Katerine Muñoz Zapata (Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
        """
    parent.acknowledgementText = """
    
""" 
    self.parent=parent
class INTERFAZ_TGWidget:
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

####################IMPORTAR VOLUMEN 4D#################################################3

### Se crea la sección para cargar el volumen 4D en una pestaña desplegable
    importDataCollapsibleButton = ctk.ctkCollapsibleButton()
    importDataCollapsibleButton.text = "Import Data"
    self.layout.addWidget(importDataCollapsibleButton)

    importDataFormLayout = qt.QFormLayout(importDataCollapsibleButton)


#### Crear desplegable para seleccionar dirección del volumen
    self.__fDialog = ctk.ctkDirectoryButton()
    self.__fDialog.caption = 'Input directory'
    importDataFormLayout.addRow('Input directory:', self.__fDialog)


 ###Selector de volumen donde se guardara el volumen de la direccion
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    importDataFormLayout.addRow("Output node:", self.outputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.outputSelector, 'setMRMLScene(vtkMRMLScene*)')  


### Parametros avanzados
    
    self.__dicomTag = qt.QLineEdit()
    self.__dicomTag.text = 'NA'
    importDataFormLayout.addRow('Frame identifying DICOM tag:', self.__dicomTag)

    self.__veLabel = qt.QLineEdit()
    self.__veLabel.text = 'na'
    importDataFormLayout.addRow('Frame identifying units:', self.__veLabel)

    self.__veInitial = qt.QDoubleSpinBox()
    self.__veInitial.value = 0
    importDataFormLayout.addRow('Initial value:', self.__veInitial)

    self.__veStep = qt.QDoubleSpinBox()
    self.__veStep.value = 1
    importDataFormLayout.addRow('Step:', self.__veStep)

  
    self.__te = qt.QDoubleSpinBox()
    self.__te.value = 1
    importDataFormLayout.addRow('EchoTime:', self.__te)

    
    self.__tr = qt.QDoubleSpinBox()
    self.__tr.value = 1
    importDataFormLayout.addRow('RepetitionTime:', self.__tr)

    self.__fa = qt.QDoubleSpinBox()
    self.__fa.value = 1
    importDataFormLayout.addRow('FlipAngle:', self.__fa)


    # Botón de importar

    self.buttonImport = qt.QPushButton("Import")
    self.buttonImport.toolTip = "Run the algorithm."
    ##self.buttonImport.enabled = True
    importDataFormLayout.addRow("                                       ", self.buttonImport)

    self.buttonImport.connect('clicked(bool)', self.importFunction)
    ##self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

################################### PARÁMETROS DE PROCESAMIENTO#################################################
##    # Se crea la sección para seleccionar parámetros el volumen 4D en una pestaña desplegable
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

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


##########################PROCESAMIENTO##########################################################################

##    # Se crea la sección para seleccionar procesamiento del volumen 4D en una pestaña desplegable
    processingCollapsibleButton = ctk.ctkCollapsibleButton()
    processingCollapsibleButton.text = "Processing"
    self.layout.addWidget(processingCollapsibleButton)

    processingFormLayout = qt.QFormLayout(processingCollapsibleButton)

        # Botón de Segmentación
    #Este botón solo se activa si el multivolumen ha sido seleccionado en la
    #ventana desplegable de Volumen 4D. Al presionarlo, el algoritmo
    #realiza el registro de los diferentes volumenes en el volumen 4D

    self.buttonSegmentation = qt.QPushButton("Segmentation")
    self.buttonSegmentation.toolTip = "Run the algorithm."
    self.buttonSegmentation.enabled = True
    processingFormLayout.addRow("                                       ", self.buttonSegmentation)


    # Botón de modelo 3D
    #Este botón solo se activa si el multivolumen ha sido seleccionado en la
    #ventana desplegable de Volumen 4D. Al presionarlo, el algoritmo
    #realiza el registro de los diferentes volumenes en el volumen 4D
    self.buttonModel = qt.QPushButton("Show 3D model")
    self.buttonModel.toolTip = "Run the algorithm."
    self.buttonModel.enabled = True
    processingFormLayout.addRow("                                       ",self.buttonModel)



########################################CURVAS#######################################################

    
##    # Se crea la sección para seleccionar curvas del volumen 4D en una pestaña desplegable
    curvesCollapsibleButton = ctk.ctkCollapsibleButton()
    curvesCollapsibleButton.text = "Curves"
    self.layout.addWidget(curvesCollapsibleButton)

    curvesFormLayout = qt.QFormLayout(curvesCollapsibleButton)

# Botón de generación de curvas
    #Este botón solo se activa si el multivolumen ha sido seleccionado en la
    #ventana desplegable de Volumen 4D. Al presionarlo, el algoritmo
    #realiza el registro de los diferentes volumenes en el volumen 4D
    self.buttonCurves = qt.QPushButton("Generate curves")
    self.buttonCurves.toolTip = "Run the algorithm."
    self.buttonCurves.enabled = True
    curvesFormLayout.addRow("                                       ",self.buttonCurves)




  def humanSort(self,l):
    """ Sort the given list in the way that humans expect. 
        Conributed by Yanling Liu
    """ 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    l.sort( key=alphanum_key )
    

  def importFunction(self):

    # check if the output container exists
    mvNode = self.outputSelector.currentNode()
    if mvNode == None:
      self.__status.text = 'Status: Select output node!'
      return


    fileNames = []    # file names on disk
    frameList = []    # frames as MRMLScalarVolumeNode's
    frameFolder = ""
    volumeLabels = vtk.vtkDoubleArray()
    frameLabelsAttr = ''
    frameFileListAttr = ''
    dicomTagNameAttr = self.__dicomTag.text
    dicomTagUnitsAttr = self.__veLabel.text
    teAttr = self.__te.text
    trAttr = self.__tr.text
    faAttr = self.__fa.text

    # each frame is saved as a separate volume
    # first filter valid file names and sort alphabetically
    frames = []
    frame0 = None
    inputDir = self.__fDialog.directory
    for f in os.listdir(inputDir):
      
      if not f.startswith('.'):
        fileName = inputDir+'/'+f
        fileNames.append(fileName)
    self.humanSort(fileNames)
    n=0
    for fileName in fileNames:
#f: información de cada scalar volume de cada corte
      (s,f) = self.readFrame(fileName)
      
      if s:
        if not frame0:
##          print("valor de f: "+ str(f));
          frame0 = f
##          print("frame0: "+str(frame0));
          frame0Image = frame0.GetImageData()
          frame0Extent = frame0Image.GetExtent()
##          print("frame0Extent: " + str(frame0Extent));
        else:
##          print("valor de f1: "+ str(f))      
          frameImage = f.GetImageData()
##          print("frameImage: "+str(frameImage))
          frameExtent = frameImage.GetExtent()
##          print("frameExtent: " + str(frameExtent));
          if frameExtent[1]!=frame0Extent[1] or frameExtent[3]!=frame0Extent[3] or frameExtent[5]!=frame0Extent[5]:
            continue
##          n=n+1
##          print("for: "+str(n))
        frames.append(f)
        

  

    nFrames = len(frames)
##    print("nFrames: "+str(nFrames))
    print('Successfully read '+str(nFrames)+' frames')

    if nFrames == 1:
      print('Single frame dataset - not reading as multivolume!')
      return

    # convert seconds data to milliseconds, which is expected by pkModeling.cxx line 81
    if dicomTagUnitsAttr == 's':
      frameIdMultiplier = 1000.0
      dicomTagUnitsAttr = 'ms'
    else:
      frameIdMultiplier = 1.0
##    print("volumeLabelsAntes: "+ str(volumeLabels))
    volumeLabels.SetNumberOfTuples(nFrames)
##    print("volumeLabelsIntermedio: "+ str(volumeLabels))
    volumeLabels.SetNumberOfComponents(1)
##    print("volumeLabelsDespues: "+ str(volumeLabels))
    volumeLabels.Allocate(nFrames)
##    print("volumeLabelsTotal: "+ str(volumeLabels))

### Después de los 3 pasos el único cambio es size, en vez de 0 pasa a ser nFrames
    for i in range(nFrames):
      frameId = frameIdMultiplier*(self.__veInitial.value+self.__veStep.value*i)
##      print("frameId: "+str(frameId))
      volumeLabels.SetComponent(i, 0, frameId) ##no hay necesidad
####      print("volumeLabelsTotal: "+ str(volumeLabels))##Aparentemente no hay cambio en volumeLabels
      frameLabelsAttr += str(frameId)+','
##      print("frameLabelsAttr: "+str(frameLabelsAttr))
    frameLabelsAttr = frameLabelsAttr[:-1] ##No hay cambio
##    print("frameLabelsAttrTOTAL: "+str(frameLabelsAttr))

    # allocate multivolume
    mvImage = vtk.vtkImageData()
##    print("mvImage: "+str(mvImage))
    mvImage.SetExtent(frame0Extent)
##    print("mvImageExtent: "+str(mvImage))
##    print("vtk.VTK_MAJOR_VERSION: "+str(vtk.VTK_MAJOR_VERSION))
    if vtk.VTK_MAJOR_VERSION <= 5: ##Versión 7
      mvImage.SetNumberOfScalarComponents(nFrames)
      print("mvImageSC: "+str(mvImage))
      mvImage.SetScalarType(frame0.GetImageData().GetScalarType())
      print("mvImageST: "+str(mvImage))
      mvImage.AllocateScalars()
      print("mvImageAllocate: "+str(mvImage))
    else:
      mvImage.AllocateScalars(frame0.GetImageData().GetScalarType(), nFrames)
##      print("mvImageElse: "+str(mvImage))
      
    extent = frame0.GetImageData().GetExtent()
    numPixels = float(extent[1]+1)*(extent[3]+1)*(extent[5]+1)*nFrames
    scalarType = frame0.GetImageData().GetScalarType()
    print('Will now try to allocate memory for '+str(numPixels)+' pixels of VTK scalar type'+str(scalarType))
    print('Memory allocated successfully')
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())
##    print("mvImageEArray: "+str(mvImageArray))
##    print("mvImage.GetPointData().GetScalars(): " + str(mvImage.GetPointData().GetScalars()));
##    print("ID mvImagearray " + str(id(mvImageArray)));
##    print("ID 2: " + str(mvImage.GetPointData().GetScalars()));
##    print("Que es frame0: " + str(frame0));


    ##EMPIEZA A FORMARCE EL VOLUMEN###############

    mat = vtk.vtkMatrix4x4()
    frame0.GetRASToIJKMatrix(mat)
    mvNode.SetRASToIJKMatrix(mat)
    frame0.GetIJKToRASMatrix(mat)
    mvNode.SetIJKToRASMatrix(mat)
    print("frameId: "+str(frameId))
    print("# imag: "+str(nFrames))
##    print("Long frame: "+str(len(frame)))
    for frameId in range(nFrames):
      # TODO: check consistent size and orientation!
      frame = frames[frameId]
      frameImage = frame.GetImageData()
      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
      mvImageArray.T[frameId] = frameImageArray

    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
    mvNode.SetAndObserveImageData(mvImage)
    mvNode.SetNumberOfFrames(nFrames)

    mvNode.SetLabelArray(volumeLabels)
    mvNode.SetLabelName(self.__veLabel.text)

    mvNode.SetAttribute('MultiVolume.FrameLabels',frameLabelsAttr)
    mvNode.SetAttribute('MultiVolume.NumberOfFrames',str(nFrames))
    mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagName',dicomTagNameAttr)
    mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagUnits',dicomTagUnitsAttr)

    if dicomTagNameAttr == 'TriggerTime' or dicomTagNameAttr == 'AcquisitionTime':
      if teAttr != '':
        mvNode.SetAttribute('MultiVolume.DICOM.EchoTime',teAttr)
      if trAttr != '':
        mvNode.SetAttribute('MultiVolume.DICOM.RepetitionTime',trAttr)
      if faAttr != '':
        mvNode.SetAttribute('MultiVolume.DICOM.FlipAngle',faAttr)

    mvNode.SetName(str(nFrames)+' frames MultiVolume')
    Helper.SetBgFgVolumes(mvNode.GetID(),None)

  def readFrame(self,file):
    sNode = slicer.vtkMRMLVolumeArchetypeStorageNode()
    sNode.ResetFileNameList()
    sNode.SetFileName(file)
    sNode.SetSingleFile(0)
    frame = slicer.vtkMRMLScalarVolumeNode()
    success = sNode.ReadData(frame)
    return (success,frame)

  # leave no trace of the temporary nodes
  def annihilateScalarNode(self, node):
    dn = node.GetDisplayNode()
    sn = node.GetStorageNode()
    node.SetAndObserveDisplayNodeID(None)
    node.SetAndObserveStorageNodeID(None)
    slicer.mrmlScene.RemoveNode(dn)
    slicer.mrmlScene.RemoveNode(sn)
    slicer.mrmlScene.RemoveNode(node)

    

##cliModule = slicer.modules.brainsfit
##n=cliModule.cliModuleLogic().CreateNode()
##for groupIndex in xrange(0,n.GetNumberOfParameterGroups()):
##  for parameterIndex in xrange(0,n.GetNumberOfParametersInGroup(groupIndex)):
##    print '  Parameter ({0}/{1}): {2} ({3})'.format(groupIndex, parameterIndex, n.GetParameterName(groupIndex, parameterIndex), n.GetParameterLabel(groupIndex, parameterIndex))
##
