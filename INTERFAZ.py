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

class INTERFAZ:
  def __init__(self, parent):
    parent.title = "INTERFAZ" 
    parent.categories = ["Procesamiento"]
    parent.dependencies = []
    parent.contributors = ["Yulieth Katerine Muñoz Zapata Hola (Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
        """
    parent.acknowledgementText = """
    
""" 
    self.parent=parent
class INTERFAZWidget:
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


###########################REGISTRO##########################################
    
##    # Se crea una sección de parámetros en una pestaña desplegable
    registerCollapsibleButton = ctk.ctkCollapsibleButton()
    registerCollapsibleButton.text = "Register"
    self.layout.addWidget(registerCollapsibleButton)

    registerFormLayout = qt.QFormLayout(registerCollapsibleButton)


    #Se crea una ventana desplegable en la cual se ingresa el volumen 4D de
    #entrada que se quiere registrar, este volumen debe ser de tipo
    #"vtkMRMLMultiVolumeNode", además si se tienen varios multivolumenes cargados
    #se puede elegir entre ellos el que se desea registrar
    self.inputRegSelector = slicer.qMRMLNodeComboBox()
    self.inputRegSelector.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputRegSelector.selectNodeUponCreation = True
    self.inputRegSelector.addEnabled = True
    self.inputRegSelector.removeEnabled = False
    self.inputRegSelector.noneEnabled = True
    self.inputRegSelector.showHidden = False
    self.inputRegSelector.showChildNodeTypes = False
    self.inputRegSelector.setMRMLScene( slicer.mrmlScene )
    self.inputRegSelector.setToolTip( "Pick the input to the algorithm." )
    registerFormLayout.addRow("Volumen 4D: ", self.inputRegSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputRegSelector, 'setMRMLScene(vtkMRMLScene*)')


   ###Selector de volumen donde se guardara el volumen de la direccion
    self.outputRegSelector = slicer.qMRMLNodeComboBox()
    self.outputRegSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputRegSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputRegSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputRegSelector.setMRMLScene(slicer.mrmlScene)
    registerFormLayout.addRow("Output node:", self.outputRegSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.outputRegSelector, 'setMRMLScene(vtkMRMLScene*)')  

 # Botón de Registro
    #Este botón solo se activa si el multivolumen ha sido seleccionado en la
    #ventana desplegable de Volumen 4D. Al presionarlo, el algoritmo
    #realiza el registro de los diferentes volumenes en el volumen 4D
    self.applyButton = qt.QPushButton("Registrar")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    registerFormLayout.addRow(self.applyButton)

    # Conexiones necesarias para el algoritmo
    #entrega al algoritmo el volumen 4D de entrada y conecta la función del botón
    #con la ejecución del registro
    self.applyButton.connect('clicked(bool)', self.registrarButton)
##    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)




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
    nFrames = 0;
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
        #frames.append(f)
        nFrames += 1;

  

    #nFrames = len(frames)
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
##      volumeLabels.SetComponent(i, 0, frameId) ##no hay necesidad
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
    frameId = 0;
    for fileName in fileNames:
      #f: información de cada scalar volume de cada corte
      (s,f) = self.readFrame(fileName)
      
      if s:
        print(fileName);
        #frames.append(f)
    #for frameId in range(nFrames):
      # TODO: check consistent size and orientation!
        frame = f;#rames[frameId]
        frameImage = frame.GetImageData()
        frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
        mvImageArray.T[frameId] = frameImageArray
        frameId += 1;

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

  def cleanup(self):
    pass

  
  def registrarButton(self):
    mvNode = self.outputRegSelector.currentNode()
    inputVolume= self.inputRegSelector.currentNode()
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


      hm = vtk.vtkMatrix4x4();
      transformadaSalida.GetMatrixTransformToWorld(hm);
      volumenMovil.ApplyTransformMatrix(hm);
      volumenMovil.SetAndObserveTransformNodeID(None)
      
      frameId = i;
      volumeLabels.SetComponent(i, 0, frameId)
      frameLabelsAttr += str(frameId)+','


##      Matriz=transformada.GetMatrixTransformToParent()
##      LR=Matriz.GetElement(0,3)#dirección izquierda o derecha en la fila 1, columna 4
##      PA=Matriz.GetElement(1,3)#dirección anterior o posterior en la fila 2, columna 4
##      IS=Matriz.GetElement(2,3)#dirección inferior o superior en la fila 3, columna 4
##      #Se mira si el volumen "i" en alguna dirección tuvo un desplazamiento
##      #mayor a 4mm, en caso de ser cierto se guarda en el vector "v"
##      if abs(LR)>4:
##        v.append(i+2)
##      elif abs(PA)>4:
##        v.append(i+2)
##      elif abs(IS)>4:
##        v.append(i+2)
##    print("MovilExtent: "+str(volumenMovil.GetImageData().GetExtent()))
####    print("valor de f: "+ str(volumenMovil))
##    frameLabelsAttr = frameLabelsAttr[:-1]

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
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Registro completo')
    return True

