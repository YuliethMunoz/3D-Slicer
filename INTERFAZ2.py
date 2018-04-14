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

class INTERFAZ2:
  def __init__(self, parent):
    parent.title = "INTERFAZ2" 
    parent.categories = ["Procesamiento"]
    parent.dependencies = []
    parent.contributors = ["Yulieth Katerine Muñoz Zapata (Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
        """
    parent.acknowledgementText = """
    
""" 
    self.parent=parent
class INTERFAZ2Widget:
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



##  def humanSort(self,l):
##    """ Sort the given list in the way that humans expect. 
##        Conributed by Yanling Liu
##    """ 
##    convert = lambda text: int(text) if text.isdigit() else text 
##    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
##    l.sort( key=alphanum_key )
##    

  def importFunction(self):

    # check if the output container exists
    mvNode = self.outputSelector.currentNode()
    #print(mvNode)
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
    print(inputDir)
##    for f in os.listdir(inputDir):
##      if not f.startswith('.'):
##        fileName = inputDir+'/'+f
##        fileNames.append(fileName)
##    self.humanSort(fileNames)
##
##    for fileName in fileNames:
##      print("Nombre archivo: " + str(fileName))
##      (s,f) = self.readFrame(fileName)
##      print("Valor s: " + str(s));
##
##      if s:
##        if not frame0:
##          frame0 = f
##          frame0Image = frame0.GetImageData()
##          frame0Extent = frame0Image.GetExtent()
##          print("Numero de volumenes: " + str(frame0Extent));
##        else:
##          frameImage = f.GetImageData()
##          frameExtent = frameImage.GetExtent()
##          if frameExtent[1]!=frame0Extent[1] or frameExtent[3]!=frame0Extent[3] or frameExtent[5]!=frame0Extent[5]:
##            continue
##        frames.append(f)
##
##    nFrames = len(frames)
##    print('Successfully read '+str(nFrames)+' frames')
##
##    if nFrames == 1:
##      print('Single frame dataset - not reading as multivolume!')
##      return
##
##    # convert seconds data to milliseconds, which is expected by pkModeling.cxx line 81
##    if dicomTagUnitsAttr == 's':
##      frameIdMultiplier = 1000.0
##      dicomTagUnitsAttr = 'ms'
##    else:
##      frameIdMultiplier = 1.0
##
##    volumeLabels.SetNumberOfTuples(nFrames)
##    volumeLabels.SetNumberOfComponents(1)
##    volumeLabels.Allocate(nFrames)
##    for i in range(nFrames):
##      frameId = frameIdMultiplier*(self.__veInitial.value+self.__veStep.value*i)
##      volumeLabels.SetComponent(i, 0, frameId)
##      frameLabelsAttr += str(frameId)+','
##    frameLabelsAttr = frameLabelsAttr[:-1]
##
##    # allocate multivolume
##    mvImage = vtk.vtkImageData()
##    mvImage.SetExtent(frame0Extent)
##    if vtk.VTK_MAJOR_VERSION <= 5:
##      mvImage.SetNumberOfScalarComponents(nFrames)
##      mvImage.SetScalarType(frame0.GetImageData().GetScalarType())
##      mvImage.AllocateScalars()
##    else:
##      mvImage.AllocateScalars(frame0.GetImageData().GetScalarType(), nFrames)
##
##    extent = frame0.GetImageData().GetExtent()
##    numPixels = float(extent[1]+1)*(extent[3]+1)*(extent[5]+1)*nFrames
##    scalarType = frame0.GetImageData().GetScalarType()
##    print('Will now try to allocate memory for '+str(numPixels)+' pixels of VTK scalar type'+str(scalarType))
##    print('Memory allocated successfully')
##    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())
##
##    mat = vtk.vtkMatrix4x4()
##    frame0.GetRASToIJKMatrix(mat)
##    mvNode.SetRASToIJKMatrix(mat)
##    frame0.GetIJKToRASMatrix(mat)
##    mvNode.SetIJKToRASMatrix(mat)
##
##    for frameId in range(nFrames):
##      # TODO: check consistent size and orientation!
##      frame = frames[frameId]
##      frameImage = frame.GetImageData()
##      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
##      mvImageArray.T[frameId] = frameImageArray
##
##    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
##    mvDisplayNode.SetScene(slicer.mrmlScene)
##    slicer.mrmlScene.AddNode(mvDisplayNode)
##    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
##    mvDisplayNode.SetDefaultColorMap()
##
##    mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
##    mvNode.SetAndObserveImageData(mvImage)
##    mvNode.SetNumberOfFrames(nFrames)
##
##    mvNode.SetLabelArray(volumeLabels)
##    mvNode.SetLabelName(self.__veLabel.text)
##
##    mvNode.SetAttribute('MultiVolume.FrameLabels',frameLabelsAttr)
##    mvNode.SetAttribute('MultiVolume.NumberOfFrames',str(nFrames))
##    mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagName',dicomTagNameAttr)
##    mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagUnits',dicomTagUnitsAttr)
##
##    if dicomTagNameAttr == 'TriggerTime' or dicomTagNameAttr == 'AcquisitionTime':
##      if teAttr != '':
##        mvNode.SetAttribute('MultiVolume.DICOM.EchoTime',teAttr)
##      if trAttr != '':
##        mvNode.SetAttribute('MultiVolume.DICOM.RepetitionTime',trAttr)
##      if faAttr != '':
##        mvNode.SetAttribute('MultiVolume.DICOM.FlipAngle',faAttr)
##
##    mvNode.SetName(str(nFrames)+' frames MultiVolume')
##    Helper.SetBgFgVolumes(mvNode.GetID(),None)
##
##  def readFrame(self,file):
##    sNode = slicer.vtkMRMLVolumeArchetypeStorageNode()
##    sNode.ResetFileNameList()
##    sNode.SetFileName(file)
##    sNode.SetSingleFile(1)
##    frame = slicer.vtkMRMLScalarVolumeNode()
##    success = sNode.ReadData(frame)
##    return (success,frame)
##
##  # leave no trace of the temporary nodes
##  def annihilateScalarNode(self, node):
##    dn = node.GetDisplayNode()
##    sn = node.GetStorageNode()
##    node.SetAndObserveDisplayNodeID(None)
##    node.SetAndObserveStorageNodeID(None)
##    slicer.mrmlScene.RemoveNode(dn)
##    slicer.mrmlScene.RemoveNode(sn)
##    slicer.mrmlScene.RemoveNode(node)
##
