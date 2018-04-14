# -*- coding: cp1252 -*-
##import vtk, qt, ctk, slicer

#
from __future__ import print_function
import sys, re, os, dicom

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

class DataImportExport:
  def __init__(self, parent):
    parent.title = "DICOM" 
    parent.categories = ["Data Import/Export"]
    parent.dependencies = []
    parent.contributors = ["Andrey Arango, Katerine Muñoz, Robinson Quintero (UdeA)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
        """
    parent.acknowledgementText = """
Mateo Ramirez, John Fredy Ochoa (Asesores)
""" 
    self.parent=parent
    Diccionario={}
    self.Diccionario=Diccionario
class DataImportExportWidget:
  
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

### Se crea la sección para importar
    importDataCollapsibleButton = ctk.ctkCollapsibleButton()
    importDataCollapsibleButton.text = "Import DICOM"
    self.layout.addWidget(importDataCollapsibleButton)
    importDataFormLayout = qt.QFormLayout(importDataCollapsibleButton)
#### Crear desplegable para seleccionar dirección del volumen
    self.__fDialog = ctk.ctkDirectoryButton()
    self.__fDialog.caption = 'Input directory'
    importDataFormLayout.addRow('Input directory:', self.__fDialog)
#### Crear desplegable para seleccionar dirección del volumen
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.inputSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.inputSelector.removeEnabled = True  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    importDataFormLayout.addRow("Input node:", self.inputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputSelector, 'setMRMLScene(vtkMRMLScene*)')

    self.__nameFrame = qt.QLineEdit()
    self.__nameFrame.text = 'NA'
    importDataFormLayout.addRow('Volume Name', self.__nameFrame)

        # Botón de importar
    self.buttonImport = qt.QPushButton("Import")
    self.buttonImport.toolTip = "Run the algorithm."
    importDataFormLayout.addRow("", self.buttonImport)
    self.buttonImport.connect('clicked(bool)', self.importFunction)
### Se crea la sección para exportar
    exportDataCollapsibleButton = ctk.ctkCollapsibleButton()
    exportDataCollapsibleButton.text = "Export DICOM"
    self.layout.addWidget(exportDataCollapsibleButton)
    exportDataFormLayout = qt.QFormLayout(exportDataCollapsibleButton)    
     ###Selector de volumen donde se guardara el volumen de la direccion
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputSelector.addEnabled = False  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    exportDataFormLayout.addRow("Volumen to export:", self.outputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.outputSelector, 'setMRMLScene(vtkMRMLScene*)')                             
  #### Crear desplegable para seleccionar direccion del volumen
    self.__fDialogOutput = ctk.ctkDirectoryButton()
    self.__fDialogOutput.caption = 'DICOM directory'
    exportDataFormLayout.addRow('DiCOM directory:', self.__fDialogOutput)
            # Botón de exportar
    self.buttonExport = qt.QPushButton("Export")
    self.buttonExport.toolTip = "Run the algorithm."
    exportDataFormLayout.addRow("", self.buttonExport)
    self.buttonExport.connect('clicked(bool)', self.ExportFunction)



  def humanSort(self,l):
    """ Sort the given list in the way that humans expect. 
        Conributed by Yanling Liu
    """ 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    l.sort( key=alphanum_key )


  def importFunction(self):
    
    self.__dicomTag = 'NA'
    self.__veLabel = 'na'
    self.__veInitial = 0
    self.__veStep = 1
    self.__te = 1
    self.__tr = 1
    self.__fa = 1
    nameFrame = self.__nameFrame.text
    
    inputVolume= self.inputSelector.currentNode()
    # check if the output container exists
    mvNode = self.outputSelector.currentNode()
##    if mvNode == None:
##      self.__status.text = 'Status: Select output node!'
##      return



    fileNames = []    # file names on disk
    frameList = []    # frames as MRMLScalarVolumeNode's
    frameFolder = ""
    volumeLabels = vtk.vtkDoubleArray()
    frameLabelsAttr = ''
    frameFileListAttr = ''
    dicomTagNameAttr = self.__dicomTag
    dicomTagUnitsAttr = self.__veLabel
    teAttr = self.__te
    trAttr = self.__tr
    faAttr = self.__fa

    # each frame is saved as a separate volume
    # first filter valid file names and sort alphabetically
    frames = []
    frame0 = None
    inputDir = self.__fDialog.directory
    
    metadatos=[]
    print('hola'+str(len(os.listdir(inputDir))))
    for f in os.listdir(inputDir):
      
      if not f.startswith('.'):
        fileName = inputDir+'/'+f
        fileName1 = str(inputDir+'/'+f)
        metadato=dicom.read_file(fileName1)
        metadatos.append(metadato)
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
      frameId = frameIdMultiplier*(self.__veInitial+self.__veStep*i)
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
    mvNode.SetLabelName(self.__veLabel)

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

    mvNode.SetName(nameFrame)
    
    NameFrame=nameFrame
    self.Diccionario={NameFrame:metadato};
    print(self.Diccionario.get(NameFrame))
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

  def ExportFunction(self):
    escena = slicer.mrmlScene;
    outputVolume= self.outputSelector.currentNode()
    outputDir=self.__fDialogOutput.directory
    Nombre=outputVolume.GetName()
    metadato1=self.Diccionario.get(Nombre)

    volumen4D = outputVolume.GetImageData()
    numero_imagenes = outputVolume.GetNumberOfFrames()
    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(volumen4D)
    
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()

    outputVolume.GetRASToIJKMatrix(ras2ijk)
    outputVolume.GetIJKToRASMatrix(ijk2ras)
    print(outputDir)
    
    for i in range(numero_imagenes):

      extract1.SetComponents(i) #Seleccionar un volumen lejano
      extract1.Update()

      ScalarVolume = slicer.vtkMRMLScalarVolumeNode();
      ScalarVolume.SetRASToIJKMatrix(ras2ijk)
      ScalarVolume.SetIJKToRASMatrix(ijk2ras)
      ScalarVolume.SetAndObserveImageData(extract1.GetOutput())
      ScalarVolume.SetName(str(Nombre)+str(i+1))
      escena.AddNode(ScalarVolume)
      Parameters={}
      
      Parameters ['patientID']=metadato1.PatientID
##        Parameters ['patientComments']=
      Parameters ['patientName']  = 'Validacion_PIS'
      Parameters ['studyID']=metadato1.StudyID
      Parameters ['studyDate']=metadato1.StudyDate
      Parameters ['studyComments']=metadato1.StudyComments
      Parameters ['studyDescription']=metadato1.StudyDescription
      Parameters ['modality']=metadato1.Modality
      Parameters ['manufacturer']=metadato1.Manufacturer
##        Parameters ['model']=
      Parameters ['seriesNumber']=metadato1.SeriesNumber
      Parameters ['seriesDescription']=metadato1.SeriesDescription
##        Parameters ['rescaleIntercept']=metadato.Rescaleintercept
##  Parameter (3/1): rescaleSlope (Rescale slope)
      Parameters ['inputVolume']=ScalarVolume
      Parameters ['dicomDirectory']=outputDir
      Parameters ['dicomPrefix']='IMG'
      Parameters ['dicomNumberFormat']='%04d' + str(i+1)
      cliNode = slicer.cli.run( slicer.modules.createdicomseries,None,Parameters,wait_for_completion=True)
        
      
      n=0


    ##        Parameters ['patientName']= 'Katy'
    



  
    a=0
    a=2;
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Multivolume Exportado')
    
##    
##
##cliModule = slicer.modules.createdicomseries
##n=cliModule.cliModuleLogic().CreateNode()
##for groupIndex in xrange(0,n.GetNumberOfParameterGroups()):
##  for parameterIndex in xrange(0,n.GetNumberOfParametersInGroup(groupIndex)):
##    print '  Parameter ({0}/{1}): {2} ({3})'.format(groupIndex, parameterIndex, n.GetParameterName(groupIndex, parameterIndex), n.GetParameterLabel(groupIndex, parameterIndex))
##
