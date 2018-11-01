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
import sitkUtils
import SimpleITK as itk

import numpy as np
#
# MultiVolumeImporter
#



class PerfussionAnalysis:
  def __init__(self, parent):
    parent.title = "PerfussionAnalysis"
    parent.categories = ["Uro-Resonance"]
    parent.dependencies = []
    parent.contributors = ["Yulieth Katerine Muï¿½oz Zapata Hola(Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
        """
    parent.acknowledgementText = """

"""
    self.parent=parent

class PerfussionAnalysisWidget:
  def __init__(self, parent = None):

    self.vector_int_der = None;
    self.vector_int_izq = None;
    self.vector_int_aort = None;
    self.numero_frames = None;
    self.vector_vol_der = None;
    self.vector_vol_izq = None;
    self.vector_vol_aort = None;
    self.frame_max = None
    
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

### Se crea la secciï¿½n para cargar el volumen 4D en una pestaï¿½a desplegable
    importDataCollapsibleButton = ctk.ctkCollapsibleButton()
    importDataCollapsibleButton.text = "Import Data"
    self.layout.addWidget(importDataCollapsibleButton)

    importDataFormLayout = qt.QFormLayout(importDataCollapsibleButton)


#### Crear desplegable para seleccionar direcciï¿½n del volumen
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
    #self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.outputSelector, 'setMRMLScene(vtkMRMLScene*)')



    # Botï¿½n de importar

    self.buttonImport = qt.QPushButton("Import")
    self.buttonImport.toolTip = "Run the algorithm."
    self.buttonImport.enabled = False
    importDataFormLayout.addWidget(self.buttonImport)

    self.buttonImport.connect('clicked(bool)', self.onImportFunction)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)


###########################REGISTRO##########################################

##    # Se crea una secciï¿½n de parï¿½metros en una pestaï¿½a desplegable
    registerCollapsibleButton = ctk.ctkCollapsibleButton()
    registerCollapsibleButton.text = "Register"
    self.layout.addWidget(registerCollapsibleButton)

    registerFormLayout = qt.QFormLayout(registerCollapsibleButton)


    #Se crea una ventana desplegable en la cual se ingresa el volumen 4D de
    #entrada que se quiere registrar, este volumen debe ser de tipo
    #"vtkMRMLMultiVolumeNode", ademï¿½s si se tienen varios multivolumenes cargados
    #se puede elegir entre ellos el que se desea registrar
    self.inputRegSelector = slicer.qMRMLNodeComboBox()
    self.inputRegSelector.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputRegSelector.addEnabled = True
    self.inputRegSelector.removeEnabled = False
    self.inputRegSelector.setMRMLScene( slicer.mrmlScene )
    registerFormLayout.addRow("Input node: ", self.inputRegSelector)



   ###Selector de volumen donde se guardara el volumen de la direccion
    self.outputRegSelector = slicer.qMRMLNodeComboBox()
    self.outputRegSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputRegSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputRegSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputRegSelector.setMRMLScene(slicer.mrmlScene)
    registerFormLayout.addRow("Output node:", self.outputRegSelector)

 # Botï¿½n de Registro
    #Este botï¿½n solo se activa si el multivolumen ha sido seleccionado en la
    #ventana desplegable de Volumen 4D. Al presionarlo, el algoritmo
    #realiza el registro de los diferentes volumenes en el volumen 4D
    self.registerButton = qt.QPushButton("Apply Register")
    self.registerButton.toolTip = "Run the algorithm."
    self.registerButton.enabled = False
    registerFormLayout.addWidget(self.registerButton)

    # Conexiones necesarias para el algoritmo
    #entrega al algoritmo el volumen 4D de entrada y conecta la funciï¿½n del botï¿½n
    #con la ejecuciï¿½n del registro
    self.registerButton.connect('clicked(bool)', self.onRegisterFunction)
    self.outputRegSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.inputRegSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)



###########################FILTRADO##########################################

    filterCollapsibleButton = ctk.ctkCollapsibleButton()
    filterCollapsibleButton.text = "Smoothing"
    self.layout.addWidget(filterCollapsibleButton)

    filterFormLayout = qt.QFormLayout(filterCollapsibleButton)

     ###Selector de volumen donde se guardara el volumen de la direccion
    self.inputFilterSelector = slicer.qMRMLNodeComboBox()
    self.inputFilterSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.inputFilterSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.inputFilterSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.inputFilterSelector.setMRMLScene(slicer.mrmlScene)
    filterFormLayout.addRow("Input node:", self.inputFilterSelector)
##    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputFilterSelector, 'setMRMLScene(vtkMRMLScene*)')

    self.outputFilterSelector = slicer.qMRMLNodeComboBox()
    self.outputFilterSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputFilterSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputFilterSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputFilterSelector.setMRMLScene(slicer.mrmlScene)
    filterFormLayout.addRow("output node:", self.outputFilterSelector)


    self.filterButton = qt.QPushButton("Apply filter")
    self.filterButton.toolTip = "Run the algorithm."
    self.filterButton.enabled = False
    filterFormLayout.addWidget(self.filterButton)

    # Conexiones necesarias para el algoritmo
    #entrega al algoritmo el volumen 4D de entrada y conecta la funciï¿½n del botï¿½n
    #con la ejecuciï¿½n del registro
    self.filterButton.connect('clicked(bool)', self.onFilterFunction)
    self.inputFilterSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.outputFilterSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    
    ###########################SEGMENTADO##########################################

    segmentCollapsibleButton = ctk.ctkCollapsibleButton()
    segmentCollapsibleButton.text = "Segmentation"
    self.layout.addWidget(segmentCollapsibleButton)

    segmentFormLayout = qt.QFormLayout(segmentCollapsibleButton)

    self.typeSegComboBox=ctk.ctkComboBox()#permite crear un desplegable con opcioneas a elegir, en este caso será el de tipo de registro
    self.typeSegComboBox.addItem('Rinon Derecho')#opción que de tipo de registro que puede elegir el usuario
    self.typeSegComboBox.addItem('Rinon izquierdo')#opción que de tipo de registro que puede elegir el usuario
    self.typeSegComboBox.addItem('Aorta')#opción que de tipo de registro que puede elegir el usuario
    self.typeSegComboBox.addItem('Todos')#opción que de tipo de registro que puede elegir el usuario
    segmentFormLayout.addRow('Area To segment:', self.typeSegComboBox)  #añade el desplegable al Layout de parameter

     ###Selector de volumen donde se guardara el volumen de la direccion
    self.inputSegSelector = slicer.qMRMLNodeComboBox()
    self.inputSegSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.inputSegSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.inputSegSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.inputSegSelector.setMRMLScene(slicer.mrmlScene)
    segmentFormLayout.addRow("Input node:", self.inputSegSelector)
##    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputFilterSelector, 'setMRMLScene(vtkMRMLScene*)')

    self.outputSegSelector = slicer.qMRMLNodeComboBox()
    self.outputSegSelector.nodeTypes = ['vtkMRMLMultiVolumeNode']
    self.outputSegSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputSegSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputSegSelector.setMRMLScene(slicer.mrmlScene)
    segmentFormLayout.addRow("output node:", self.outputSegSelector)
    
    self.fiducialSegSelector = slicer.qMRMLNodeComboBox()
    self.fiducialSegSelector.nodeTypes = ['vtkMRMLMarkupsFiducialNode']
    self.fiducialSegSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.fiducialSegSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.fiducialSegSelector.setMRMLScene(slicer.mrmlScene)
    segmentFormLayout.addRow("Seed:", self.fiducialSegSelector)


    self.segmentButton = qt.QPushButton("Apply Segmentation")
    self.segmentButton.toolTip = "Run the algorithm."
    self.segmentButton.enabled = False
    segmentFormLayout.addWidget(self.segmentButton)

    # Conexiones necesarias para el algoritmo
    #entrega al algoritmo el volumen 4D de entrada y conecta la funciï¿½n del botï¿½n
    #con la ejecuciï¿½n del registro
    self.segmentButton.connect('clicked(bool)', self.onSegmentFunction)
    self.inputSegSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.outputSegSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.fiducialSegSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)


    plotCollapsibleButton = ctk.ctkCollapsibleButton()
    plotCollapsibleButton.text = "Analysis of Data"
    self.layout.addWidget(plotCollapsibleButton)

    plotFormLayout = qt.QFormLayout(plotCollapsibleButton)

    self.typeComboBox=ctk.ctkComboBox()#permite crear un desplegable con opcioneas a elegir, en este caso será el de tipo de registro
    self.typeComboBox.addItem('Intensidad Rinon Derecho')#opción que de tipo de registro que puede elegir el usuario
    self.typeComboBox.addItem('Intensidad Rinon Izquierdo')#opción que de tipo de registro que puede elegir el usuario
    self.typeComboBox.addItem('Intensidad Aorta')#opción que de tipo de registro que puede elegir el usuario
    self.typeComboBox.addItem('Patlak Rinon derecho')
    self.typeComboBox.addItem('Patlak Rinon izquierdo')
    
    plotFormLayout.addRow('Area Type:', self.typeComboBox)  #añade el desplegable al Layout de parameter

    self.file_path0 = qt.QLineEdit()
    self.file_path0.text = 'Copy File Path from DICOM'
    plotFormLayout.addRow('First Path:', self.file_path0)

    self.file_pathx = qt.QLineEdit()
    self.file_pathx.text = 'Copy File Path from DICOM'
    plotFormLayout.addRow('Last one Path:', self.file_pathx)
    
    self.CTT = qt.QLineEdit()
    self.CTT.text = 'NA'
    self.CTT.enabled = False
    plotFormLayout.addRow('CTT (mins):', self.CTT)

    self.RTT = qt.QLineEdit()
    self.RTT.text = 'NA'
    self.RTT.enabled = False
    plotFormLayout.addRow('RTT (mins):', self.RTT)

    self.TTP = qt.QLineEdit()
    self.TTP.text = 'NA'
    self.TTP.enabled = False
    plotFormLayout.addRow('TTP (mins):', self.TTP)


    self.plotButton = qt.QPushButton("Results")
    self.plotButton.toolTip = "Run the algorithm."
    self.plotButton.enabled = True
    plotFormLayout.addWidget(self.plotButton)

    self.plotButton.connect('clicked(bool)', self.onPlotFunction)

        
    
    self.onSelect()

  def onSelect(self):
    self.buttonImport.enabled=self.outputSelector.currentNode()
    self.filterButton.enabled=self.inputFilterSelector.currentNode() and self.outputFilterSelector.currentNode()
    self.registerButton.enabled=self.outputRegSelector.currentNode() and  self.inputRegSelector.currentNode()
    self.segmentButton.enabled=self.outputSegSelector.currentNode() and  self.inputSegSelector.currentNode() and  self.fiducialSegSelector.currentNode()
  
  
  def onImportFunction(self):
    logic=IMPORTLogic()
    logic.importFunction(self.outputSelector.currentNode(),self.__fDialog.directory)

  def onRegisterFunction(self):
    logic=REGISTERLogic()
    logic.registerFunction(self.inputRegSelector.currentNode(),self.outputRegSelector.currentNode())
    
  def onFilterFunction(self):
    logic=FILTERLogic()
    logic.filterFunction(self.inputFilterSelector.currentNode(),self.outputFilterSelector.currentNode())
  
  def onSegmentFunction(self):
    if(self.typeSegComboBox.currentText=='Rinon Derecho'):
      logic=SEGMENTATIONLogic()
      self.vector_int_der,self.numero_frames,self.vector_vol_der,self.frame_max=logic.segmentDerFunction(self.inputSegSelector.currentNode(),self.outputSegSelector.currentNode(),self.fiducialSegSelector.currentNode() )
    elif(self.typeSegComboBox.currentText=='Rinon izquierdo'):
      logic=SEGMENTATIONLogic()
      self.vector_int_izq,self.numero_frames,self.vector_vol_izq,self.frame_max=logic.segmentIzqFunction(self.inputSegSelector.currentNode(),self.outputSegSelector.currentNode(),self.fiducialSegSelector.currentNode() )
    elif(self.typeSegComboBox.currentText=='Aorta'):
      logic=SEGMENTATIONLogic()
      self.vector_int_aort,self.numero_frames,self.vector_vol_aort,self.frame_max=logic.segmentAortFunction(self.inputSegSelector.currentNode(),self.outputSegSelector.currentNode(),self.fiducialSegSelector.currentNode() )

  def onPlotFunction(self):
    logic=ANALISISLogic()
    logic.plotDerFunction(self.numero_frames,self.vector_int_der,self.vector_vol_der,self.vector_int_izq,self.vector_vol_izq,self.vector_int_aort,self.vector_vol_aort,self.typeComboBox.currentText,self.CTT,self.RTT,self.TTP,self.frame_max,self.file_path0.text,self.file_pathx.text)
  
class ANALISISLogic:
  global vector_int_der
  global numero_frames
  global vector_vol_der
  def plotDerFunction(self,numero_frames,vector_int_der,vector_vol_der,vector_int_izq,vector_vol_izq,vector_int_aort,vector_vol_aort,area,CTT,RTT,TTP,frame_max,file_path0,file_pathx):
    import numpy as np
    
    import dicom
    metadato=dicom.read_file(file_path0)
    metadato1=dicom.read_file(file_pathx)
    primer_frame=int(metadato.AcquisitionTime[2:4])
    ultimo_frame=int(metadato1.AcquisitionTime[2:4])
    minutos=ultimo_frame-primer_frame
    
    lns = slicer.mrmlScene.GetNodesByClass('vtkMRMLLayoutNode')
    lns.InitTraversal()
    ln = lns.GetNextItemAsObject()
    ln.SetViewArrangement(24)

    # Get the Chart View Node
    cvns = slicer.mrmlScene.GetNodesByClass('vtkMRMLChartViewNode')
    cvns.InitTraversal()
    cvn = cvns.GetNextItemAsObject()

    # Create an Array Node and add some d0ata
    dn = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
    a = dn.GetArray()
    a.SetNumberOfTuples(numero_frames)
    x = range(0, 600)
    i=0
    prom_der=np.mean(vector_int_der)
    prom_izq=np.mean(vector_int_izq)
    prom_aort=np.mean(vector_int_aort)
    acu=0
    acu1=0
    print('ESTADÍSTICA')
    
##    TTP_list_der=np.where(vector_int_der==np.max(vector_int_der))
##    TTP_list_izq=np.where(vector_int_der==np.max(vector_int_der))
##    TTP_list_aort=np.where(vector_int_der==np.max(vector_int_der))
##    TTP_pos_der=TTP_list_der[1][0]
##    TTP_pos_izq=TTP_list_izq[1][0]
##    TTP_pos_aort=TTP_list_aort[1][0]
##    prom_TTP=(TTP_pos_der+TTP_pos_der+TTP_pos_aort)/3
##    x=(((minutos*100)/numero_frames)*prom_TTP)
##    TTP.text=x/100
##    
    x=(((minutos*100)/numero_frames)*frame_max)
    RTT.text=x/100
    x=((minutos*100)/numero_frames)*frame_max
    CTT.text=x/100
    for i in range(numero_frames):

      if(area=='Intensidad Rinon Derecho'):
      
        
        print('RINON DERECHO')
        print('Volumen frame'+str(i)+': '+str(vector_vol_der[i])+' mm3')
        a.SetComponent(i, 0,i )
        a.SetComponent(i, 1, vector_int_der[i])
        
      elif(area=='Intensidad Rinon Izquierdo'):
        
        print('RINON IZQUIERDO')
        print('Volumen frame'+str(i)+': '+str(vector_vol_izq[i])+' mm3')
        print('Intensidad frame'+str(i)+': '+str(vector_int_izq[i]))
        a.SetComponent(i, 0,i )
        a.SetComponent(i, 1, vector_int_izq[i])
      elif(area=='Intensidad Aorta'):
        print('AORTA')
        print('Volumen frame'+str(i)+': '+str(vector_vol_aort[i])+' mm3')
        a.SetComponent(i, 0,i )
        a.SetComponent(i, 1, vector_int_aort[i])
      elif(area=='Patlak Rinon izquierdo'):
        acu=acu+(vector_int_aort[i]-prom_aort)*(vector_int_izq[i]-prom_izq)
        acu1=acu+(vector_int_aort[i]-prom_aort)**2
        B1=acu/acu1
        B0=prom_izq-(B1*prom_aort)
      elif(area=='Patlak Rinon derecho'):
        acu=acu+(vector_int_aort[i]-prom_aort)*(vector_int_der[i]-prom_der)
        acu1=acu1+(vector_int_aort[i]-prom_aort)**2.0
        B1=acu/acu1
        B0=prom_der-(B1*prom_aort)
    
    cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

    # Add the Array Nodes to the Chart. The first argument is a string used for the legend and to refer to the Array when setting properties.
    cn.AddArray('Perfusion '+str(area), dn.GetID())

    # Set a few properties on the Chart. The first argument is a string identifying which Array to assign the property. 
    # 'default' is used to assign a property to the Chart itself (as opposed to an Array Node).
    cn.SetProperty('default', 'title', 'Perfusion curves')
    cn.SetProperty('default', 'xAxisLabel', 'Volume')
    cn.SetProperty('default', 'yAxisLabel', 'Intensity')

    # Tell the Chart View which Chart to display
    cvn.SetChartNodeID(cn.GetID()) 
    y=[]
    if(area=='Patlak Rinon izquierdo' or area=='Patlak Rinon derecho'):
      if(area=='Patlak Rinon izquierdo'):
        
        for i in range(numero_frames):
          y.append(B0+(B1*vector_int_aort[i]))
          a.SetComponent(i, 0,vector_int_aort[i] )
          a.SetComponent(i, 1, y[i])
          a.SetComponent(i, 2, vector_int_izq[i])
        cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

      # Add the Array Nodes to the Chart. The first argument is a string used for the legend and to refer to the Array when setting properties.
        cn.AddArray('Pendiente: '+str(B1), dn.GetID())

        # Set a few properties on the Chart. The first argument is a string identifying which Array to assign the property. 
        # 'default' is used to assign a property to the Chart itself (as opposed to an Array Node).
        cn.SetProperty('default', 'title', 'Perfusion curves')
        cn.SetProperty('default', 'xAxisLabel', 'Rinon Izquierdo/aorta')
        cn.SetProperty('default', 'yAxisLabel', 'Aorta')

        # Tell the Chart View which Chart to display
        cvn.SetChartNodeID(cn.GetID())
      if (area=='Patlak Rinon derecho'):
        for i in range(numero_frames):
          y.append(B0+(B1*vector_int_aort[i]))
          a.SetComponent(i, 0,vector_int_aort[i] )
          a.SetComponent(i, 1, y[i])
          a.SetComponent(i, 2, vector_int_izq[i])
        cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

      # Add the Array Nodes to the Chart. The first argument is a string used for the legend and to refer to the Array when setting properties.
        cn.AddArray('Pendiente: '+str(B1), dn.GetID())

        # Set a few properties on the Chart. The first argument is a string identifying which Array to assign the property. 
        # 'default' is used to assign a property to the Chart itself (as opposed to an Array Node).
        cn.SetProperty('default', 'title', 'Perfusion curves')
        cn.SetProperty('default', 'xAxisLabel', 'Rinon derecho/aorta')
        cn.SetProperty('default', 'yAxisLabel', 'Aorta')

        # Tell the Chart View which Chart to display
        cvn.SetChartNodeID(cn.GetID())


    # Create a Chart Node.
    
    return True
    
class SEGMENTATIONLogic:
  global vector_int_der
  global numero_frames
  global vector_vol_der
  
  def segmentDerFunction(self, volumen4D, outputVolume, fiducial):
##    slicer.util.getNode('vtkMRMLMultiVolumeNode1').SetName('h')
##    a=slicer.util.getNode('h')
    
	
    ##  Obtencion de datos de la imagen
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)
    imagenvtk4D = volumen4D.GetImageData()
    numero_puntos=int(volumen4D.GetImageData().GetNumberOfPoints())
    numero_frames= volumen4D.GetImageData().GetNumberOfScalarComponents()

    ## Inicialiando listas
    vector_int=[]
    vector_int_der=[]
    vect_int=[]
    vector_med=[]
    vector_dif=[]
    vector_dif2=[]
    frame=[]
    i=0
    frameLabelsAttr = ''
    ##  Extraccion de intensidad del fiducial para cada volumen
    fidList = fiducial

    #  Crdenadas del fiducial
    ras=[0,0,0]
    fidList.GetNthFiducialPosition(0,ras)
    ijk=ras2ijk.MultiplyPoint([ras[0],ras[1],ras[2],1])

    ##  Extraccion de volumenes por  separado
    for i in range(numero_frames):
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(volumen4D.GetImageData())
      extract1.SetComponents(i)
      extract1.Update()
      
    ##  Creacion de volumenes 
      volume=slicer.vtkMRMLScalarVolumeNode()
      volume.SetAndObserveImageData(extract1.GetOutput())
      volume.SetName('Vol10')
      volume.SetIJKToRASMatrix(ijk2ras)
      volume.SetRASToIJKMatrix(ras2ijk)
      slicer.mrmlScene.AddNode(volume)
      frameImage1 = volume.GetImageData()
      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage1.GetPointData().GetScalars())
      frame.append(frameImageArray)
      intensidad=np.mean(frameImageArray[:])
      mediana=np.median(frameImageArray)
      vector_int.append(intensidad)
      vector_med.append(mediana)
      slicer.mrmlScene.RemoveNode(volume)
      vect_int.append(volumen4D.GetImageData().GetScalarComponentAsDouble(int(ijk[0]),int(ijk[1]),int(ijk[2]),i))

    ## Creacion espacial
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    volumeLabels = vtk.vtkDoubleArray()
    volumeLabels.SetNumberOfTuples(6)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(6)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen4D.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumen4D.GetImageData().GetScalarType(),6)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen

    ##  Identificacion volumen de ingreso del contrste y suavizado
    vector_dif.append(np.diff(vector_med))  
    vector_max=np.where(vector_dif==np.max(vector_dif[0][(int(numero_frames*0.125)):(int(numero_frames*0.875))]))
    frame_max=vector_max[1][0] + 1

    frame[0]=np.sum(frame[0:frame_max-5], axis=0)/(frame_max-5+1)
    frame[1]=np.sum(frame[frame_max+2:numero_frames], axis=0)/(numero_frames-frame_max+2+1)

    frame[0]=frame[0].astype(int)
    frame[1]=frame[1].astype(int)
    smothingImageArray=abs(np.subtract(frame[1],frame[0]))

    ##  Transformada de intensidad [gamma] son min y max
    transformImageArray=smothingImageArray**1.2

    dimensions=volumen4D.GetImageData().GetDimensions()
    transformImageMatriz=np.reshape(transformImageArray, (dimensions[2],dimensions[1],dimensions[0]))

    ## Binarizacion numero 1
    bin1ImageArray=np.zeros(np.shape(transformImageArray)[0])
    binMask=transformImageMatriz[int(ijk[2])-1:int(ijk[2])+2,int(ijk[1])-1:int(ijk[1])+2,int(ijk[0])-1:int(ijk[0])+2]## cambie la variable por trasnformImageMatrix
    rang_bin=np.where(np.logical_and(transformImageArray>=np.min(binMask)*0.9,transformImageArray<=np.max(binMask)*1.1))
    bin1ImageArray[rang_bin[0]]=1##Resultado primera binarizacion

    ##  Operacion local
    bin1ImageMatriz=np.reshape(bin1ImageArray, (dimensions[2],dimensions[1],dimensions[0]))
    opLocalImageMatriz=np.zeros(np.shape(bin1ImageMatriz))##crear matriz de ceros
    for i in range(dimensions[1]/2):
      for j in range (dimensions[0]/2): 
            
            bin1ImageSubMatriz=bin1ImageMatriz[:,i*2:(i*2)+2,j*2:(j*2)+2]
            onesSubmatriz=np.where(bin1ImageSubMatriz==1)
            numOnes=np.size(onesSubmatriz[1])
            opLocalImageMatriz[:,i*2:(i*2)+2,j*2:(j*2)+2]=numOnes

    opLocalImageMatriz[:,:,0:dimensions[0]/2]=0
    opLocalImageMatriz2=np.zeros((dimensions[2],dimensions[0],dimensions[1]))##crear matriz de ceros
    opLocalImageArray2=np.reshape(opLocalImageMatriz,-1)##Resultado operacion local
    for i in range(dimensions[2]):
      for j in range (dimensions[1]):
            for k in range (dimensions[0]): 
            
              opLocalImageMatriz2[i,k,j]=opLocalImageMatriz[i,j,k]
            

    opLocalImageArray=np.reshape(opLocalImageMatriz2,-1)##Resultado operacion local

    ##  Filtro promedio
    kernelAverage=np.ones((13))*13
    imFiltArray=np.convolve(opLocalImageArray,kernelAverage,mode='same')
    imFiltArray2=np.convolve(opLocalImageArray2,kernelAverage,mode='same')

    ##  Binarizacion numero 2
    imFiltArrayMatriz=np.reshape(imFiltArray, (dimensions[2],dimensions[0],dimensions[1]))
    bin2ImageArray=np.zeros(np.shape(imFiltArray)[0])

    imFiltArrayMatriz2=np.zeros((dimensions[2],dimensions[1],dimensions[0]))##crear matriz de ceros

    for i in range(dimensions[2]):
      for j in range (dimensions[0]):
            for k in range (dimensions[1]): 
            
              imFiltArrayMatriz2[i,k,j]=imFiltArrayMatriz[i,j,k]

    imFiltArray=np.reshape(imFiltArrayMatriz2,-1)

    imFiltArray=(imFiltArray+imFiltArray2)/2
    ##imFiltArray=imFiltArray**1.7
    imFiltArray=imFiltArray.astype(int)

    histogram=np.histogram(imFiltArray,bins=np.max(imFiltArray))
    ##imFiltArray=(np.median(histogram[1])+imFiltArray2)/2


    ##mvImageArray.T[0] = smothingImageArray
    ##mvImageArray.T[0] = transformImageArray
    ##mvImageArray.T[0] = imFiltArray
    ##mvImageArray.T[0] = opLocalImageArray
    ##mvImageArray.T[0]=opLocalImageArray2
    mvImageArray.T[0] = imFiltArray
    ##mvImageArray.T[0]=bin1ImageArray
    ##mvImageArray.T[1] = bin2ImageArray
    mvNode=outputVolume
    mvNode.SetRASToIJKMatrix(ras2ijk)
    mvNode.SetIJKToRASMatrix(ijk2ras)
    mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
    mvNode.SetAndObserveImageData(mvImage)
    mvNode.SetNumberOfFrames(2)
    mvNode.SetLabelArray(volumeLabels)
    mvNode.SetName('PrimerasOp2')
    slicer.mrmlScene.AddNode(mvNode)

    volumen4D=slicer.util.getNode('PrimerasOp2')
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)

    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(volumen4D.GetImageData())
    extract1.SetComponents(0)
    extract1.Update()
    
    volume=slicer.vtkMRMLScalarVolumeNode()
    volume.SetAndObserveImageData(extract1.GetOutput())
    volume.SetName('OpLocalVol_gir')
    volume.SetIJKToRASMatrix(ijk2ras)
    volume.SetRASToIJKMatrix(ras2ijk)
    slicer.mrmlScene.AddNode(volume)
    
    Label=slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(Label)
    
    parameters = {}
    parameters['iterations'] = 5
    parameters['multiplier'] = 2.5
    parameters['neighborhood'] = 1
    parameters['labelvalue'] =1
    parameters['seed'] =fiducial.GetID()
    parameters['inputVolume'] =volume.GetID()
    parameters['outputVolume'] =Label.GetID()
    cliNode = slicer.cli.run( slicer.modules.simpleregiongrowingsegmentation,None,parameters,wait_for_completion=True)

    Label.SetName('Label_volume')
    bin2ImageMatriz=slicer.util.arrayFromVolume(Label)
    bin3ImageMatriz=bin1ImageMatriz*bin2ImageMatriz
    
    volumen= slicer.vtkMRMLScalarVolumeNode()
    volumen.SetAndObserveImageData(extract1.GetOutput())
    volumen.SetName('volumen')
    volumen.SetIJKToRASMatrix(ijk2ras)
    volumen.SetRASToIJKMatrix(ras2ijk)
    slicer.mrmlScene.AddNode(volumen)
    
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    volumeLabels = vtk.vtkDoubleArray()
    volumeLabels.SetNumberOfTuples(numero_frames)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_frames)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen4D.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumen4D.GetImageData().GetScalarType(),numero_frames)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen
    
    
    
    prim=ijk2ras.MultiplyPoint([1,1,1,1])
    seg=ijk2ras.MultiplyPoint([2,2,2,1])
    vol_voxel=(seg[0]-prim[0])*(seg[1]-prim[1])*(seg[2]-prim[2])
    vector_vol_der=[]
    for i in range(numero_frames):
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(imagenvtk4D)
      extract1.SetComponents(i) #Seleccionar un volumen lejano
      extract1.Update()
      volumen.SetAndObserveImageData(extract1.GetOutput())
      volumen.SetName('volumen_binarizado')
      slicer.mrmlScene.AddNode(volumen)
      ImageMatriz=slicer.util.arrayFromVolume(volumen)
      bin4ImageMatriz=bin3ImageMatriz*ImageMatriz
      bin4ImageArray=np.reshape(bin4ImageMatriz,-1)
      intensidad=np.mean(bin4ImageArray[:])
      vector_int_der.append(intensidad)
      vol_rinon=abs(intensidad*vol_voxel)
      vector_vol_der.append(vol_rinon)
      print('Volumen frame'+str(i)+': '+str(vol_rinon)+' mm3')
      mvImageArray.T[i] = bin4ImageArray
      
    RECONSTRUCTIONLogic().reconstruction2Function(outputVolume,mvImage,numero_frames,volumeLabels,frameLabelsAttr,'Multivolumen Segmentado',ras2ijk,ijk2ras)
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Segmentado completo')
    # Switch to a layout (24) that contains a Chart View to initiate the construction of the widget and Chart View Node

    return vector_int_der, numero_frames, vector_vol_der,frame_max


    
    
  def segmentIzqFunction(self, volumen4D, outputVolume, fiducial):

    ##  Obtencion de datos de la imagen
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)
    imagenvtk4D = volumen4D.GetImageData()
    numero_puntos=int(volumen4D.GetImageData().GetNumberOfPoints())
    numero_frames= volumen4D.GetImageData().GetNumberOfScalarComponents()

    ## Inicialiando listas
    vector_int_izq=[]
    vector_int=[]
    vect_int=[]
    vector_med=[]
    vector_dif=[]
    vector_dif2=[]
    frame=[]
    i=0
    frameLabelsAttr = ''
    ##  Extraccion de intensidad del fiducial para cada volumen
    fidList = fiducial

    #  Crdenadas del fiducial
    ras=[0,0,0]
    fidList.GetNthFiducialPosition(0,ras)
    ijk=ras2ijk.MultiplyPoint([ras[0],ras[1],ras[2],1])

    ##  Extraccion de volumenes por  separado
    for i in range(numero_frames):
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(volumen4D.GetImageData())
      extract1.SetComponents(i)
      extract1.Update()
      
    ##  Creacion de volumenes 
      volume=slicer.vtkMRMLScalarVolumeNode()
      volume.SetAndObserveImageData(extract1.GetOutput())
      volume.SetName('Vol10')
      volume.SetIJKToRASMatrix(ijk2ras)
      volume.SetRASToIJKMatrix(ras2ijk)
      slicer.mrmlScene.AddNode(volume)
      frameImage1 = volume.GetImageData()
      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage1.GetPointData().GetScalars())
      frame.append(frameImageArray)
      intensidad=np.mean(frameImageArray[:])
      mediana=np.median(frameImageArray)
      vector_int.append(intensidad)
      vector_med.append(mediana)
      slicer.mrmlScene.RemoveNode(volume)
      vect_int.append(volumen4D.GetImageData().GetScalarComponentAsDouble(int(ijk[0]),int(ijk[1]),int(ijk[2]),i))

    ## Creacion espacial
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    volumeLabels = vtk.vtkDoubleArray()
    volumeLabels.SetNumberOfTuples(6)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(6)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen4D.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumen4D.GetImageData().GetScalarType(),6)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen

    ##  Identificacion volumen de ingreso del contrste y suavizado
    vector_dif.append(np.diff(vector_med))  
    vector_max=np.where(vector_dif==np.max(vector_dif[0][(int(numero_frames*0.125)):(int(numero_frames*0.875))]))
    frame_max=vector_max[1][0] + 1

    frame[0]=np.sum(frame[0:frame_max-5], axis=0)/(frame_max-5+1)
    frame[1]=np.sum(frame[frame_max+2:numero_frames], axis=0)/(numero_frames-frame_max+2+1)

    frame[0]=frame[0].astype(int)
    frame[1]=frame[1].astype(int)
    smothingImageArray=abs(np.subtract(frame[1],frame[0]))

    ##  Transformada de intensidad [gamma] son min y max
    transformImageArray=smothingImageArray**1.2

    dimensions=volumen4D.GetImageData().GetDimensions()
    transformImageMatriz=np.reshape(transformImageArray, (dimensions[2],dimensions[1],dimensions[0]))

    ## Binarizacion numero 1
    bin1ImageArray=np.zeros(np.shape(transformImageArray)[0])
    binMask=transformImageMatriz[int(ijk[2])-1:int(ijk[2])+2,int(ijk[1])-1:int(ijk[1])+2,int(ijk[0])-1:int(ijk[0])+2]## cambie la variable por trasnformImageMatrix
    rang_bin=np.where(np.logical_and(transformImageArray>=np.min(binMask)*0.9,transformImageArray<=np.max(binMask)*1.1))
    bin1ImageArray[rang_bin[0]]=1##Resultado primera binarizacion

    ##  Operacion local
    bin1ImageMatriz=np.reshape(bin1ImageArray, (dimensions[2],dimensions[1],dimensions[0]))
    opLocalImageMatriz=np.zeros(np.shape(bin1ImageMatriz))##crear matriz de ceros
    for i in range(dimensions[1]/2):
      for j in range (dimensions[0]/2): 
            
            bin1ImageSubMatriz=bin1ImageMatriz[:,i*2:(i*2)+2,j*2:(j*2)+2]
            onesSubmatriz=np.where(bin1ImageSubMatriz==1)
            numOnes=np.size(onesSubmatriz[1])
            opLocalImageMatriz[:,i*2:(i*2)+2,j*2:(j*2)+2]=numOnes

    opLocalImageMatriz[:,:,dimensions[0]/2:dimensions[0]]=0
    opLocalImageMatriz2=np.zeros((dimensions[2],dimensions[0],dimensions[1]))##crear matriz de ceros
    opLocalImageArray2=np.reshape(opLocalImageMatriz,-1)##Resultado operacion local
    for i in range(dimensions[2]):
      for j in range (dimensions[1]):
            for k in range (dimensions[0]): 
            
              opLocalImageMatriz2[i,k,j]=opLocalImageMatriz[i,j,k]
            

    opLocalImageArray=np.reshape(opLocalImageMatriz2,-1)##Resultado operacion local

    ##  Filtro máximo
    kernelAverage=np.ones((13))*13
    imFiltArray=np.convolve(opLocalImageArray,kernelAverage,mode='same')
    imFiltArray2=np.convolve(opLocalImageArray2,kernelAverage,mode='same')

    ##  Binarizacion numero 2
    imFiltArrayMatriz=np.reshape(imFiltArray, (dimensions[2],dimensions[0],dimensions[1]))
    bin2ImageArray=np.zeros(np.shape(imFiltArray)[0])

    imFiltArrayMatriz2=np.zeros((dimensions[2],dimensions[1],dimensions[0]))##crear matriz de ceros

    for i in range(dimensions[2]):
      for j in range (dimensions[0]):
            for k in range (dimensions[1]): 
            
              imFiltArrayMatriz2[i,k,j]=imFiltArrayMatriz[i,j,k]

    imFiltArray=np.reshape(imFiltArrayMatriz2,-1)

    imFiltArray=(imFiltArray+imFiltArray2)/2
    ##imFiltArray=imFiltArray**1.7
    imFiltArray=imFiltArray.astype(int)

    histogram=np.histogram(imFiltArray,bins=np.max(imFiltArray))
    ##imFiltArray=(np.median(histogram[1])+imFiltArray2)/2


    ##mvImageArray.T[0] = smothingImageArray
    ##mvImageArray.T[0] = transformImageArray
    ##mvImageArray.T[0] = imFiltArray
    ##mvImageArray.T[0] = opLocalImageArray
    ##mvImageArray.T[0]=opLocalImageArray2
    mvImageArray.T[0] = imFiltArray
    ##mvImageArray.T[0]=bin1ImageArray
    ##mvImageArray.T[1] = bin2ImageArray
    mvNode=outputVolume
    mvNode.SetRASToIJKMatrix(ras2ijk)
    mvNode.SetIJKToRASMatrix(ijk2ras)
    mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
    mvNode.SetAndObserveImageData(mvImage)
    mvNode.SetNumberOfFrames(2)
    mvNode.SetLabelArray(volumeLabels)
    mvNode.SetName('PrimerasOp2')
    slicer.mrmlScene.AddNode(mvNode)

    volumen4D=slicer.util.getNode('PrimerasOp2')
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)

    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(volumen4D.GetImageData())
    extract1.SetComponents(0)
    extract1.Update()
    
    volume=slicer.vtkMRMLScalarVolumeNode()
    volume.SetAndObserveImageData(extract1.GetOutput())
    volume.SetName('OpLocalVol_gir')
    volume.SetIJKToRASMatrix(ijk2ras)
    volume.SetRASToIJKMatrix(ras2ijk)
    slicer.mrmlScene.AddNode(volume)
    
    Label=slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(Label)
    
    parameters = {}
    parameters['iterations'] = 5
    parameters['multiplier'] = 2.5
    parameters['neighborhood'] = 1
    parameters['labelvalue'] =1
    parameters['seed'] =fiducial.GetID()
    parameters['inputVolume'] =volume.GetID()
    parameters['outputVolume'] =Label.GetID()
    cliNode = slicer.cli.run( slicer.modules.simpleregiongrowingsegmentation,None,parameters,wait_for_completion=True)

    Label.SetName('Label_volume')
    bin2ImageMatriz=slicer.util.arrayFromVolume(Label)
    bin3ImageMatriz=bin1ImageMatriz*bin2ImageMatriz
    
    volumen= slicer.vtkMRMLScalarVolumeNode()
    volumen.SetAndObserveImageData(extract1.GetOutput())
    volumen.SetName('volumen')
    volumen.SetIJKToRASMatrix(ijk2ras)
    volumen.SetRASToIJKMatrix(ras2ijk)
    slicer.mrmlScene.AddNode(volumen)
    
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    volumeLabels = vtk.vtkDoubleArray()
    volumeLabels.SetNumberOfTuples(numero_frames)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_frames)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen4D.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumen4D.GetImageData().GetScalarType(),numero_frames)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen
    
    prim=ijk2ras.MultiplyPoint([1,1,1,1])
    seg=ijk2ras.MultiplyPoint([2,2,2,1])
    vol_voxel=(seg[0]-prim[0])*(seg[1]-prim[1])*(seg[2]-prim[2])
    vector_vol_izq=[]
    for i in range(numero_frames):
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(imagenvtk4D)
      extract1.SetComponents(i) #Seleccionar un volumen lejano
      extract1.Update()
      volumen.SetAndObserveImageData(extract1.GetOutput())
      volumen.SetName('volumen_binarizado')
      slicer.mrmlScene.AddNode(volumen)
      ImageMatriz=slicer.util.arrayFromVolume(volumen)
      bin4ImageMatriz=bin3ImageMatriz*ImageMatriz
      bin4ImageArray=np.reshape(bin4ImageMatriz,-1)
      intensidad=np.mean(bin4ImageArray[:])
      vector_int_izq.append(intensidad)
      vol_rinon=abs(intensidad*vol_voxel)
      vector_vol_izq.append(vol_rinon)
      print('Volumen frame'+str(i)+': '+str(vol_rinon)+' mm3')
      mvImageArray.T[i] = bin4ImageArray
    RECONSTRUCTIONLogic().reconstruction2Function(outputVolume,mvImage,numero_frames,volumeLabels,frameLabelsAttr,'Multivolumen Segmentado',ras2ijk,ijk2ras)
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Segmentado completo')
    return vector_int_izq,numero_frames,vector_vol_izq,frame_max

  def segmentAortFunction(self, volumen4D, outputVolume, fiducial):

	
    ##  Obtencion de datos de la imagen
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)
    imagenvtk4D = volumen4D.GetImageData()
    numero_puntos=int(volumen4D.GetImageData().GetNumberOfPoints())
    numero_frames= volumen4D.GetImageData().GetNumberOfScalarComponents()

    ## Inicialiando listas
    vector_int_aort=[]
    vector_int=[]
    vect_int=[]
    vector_med=[]
    vector_dif=[]
    vector_dif2=[]
    frame=[]
    i=0
    frameLabelsAttr = ''
    ##  Extraccion de intensidad del fiducial para cada volumen
    fidList = fiducial

    #  Crdenadas del fiducial
    ras=[0,0,0]
    fidList.GetNthFiducialPosition(0,ras)
    ijk=ras2ijk.MultiplyPoint([ras[0],ras[1],ras[2],1])

    ##  Extraccion de volumenes por  separado
    for i in range(numero_frames):
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(volumen4D.GetImageData())
      extract1.SetComponents(i)
      extract1.Update()
      
    ##  Creacion de volumenes 
      volume=slicer.vtkMRMLScalarVolumeNode()
      volume.SetAndObserveImageData(extract1.GetOutput())
      volume.SetName('Vol10')
      volume.SetIJKToRASMatrix(ijk2ras)
      volume.SetRASToIJKMatrix(ras2ijk)
      slicer.mrmlScene.AddNode(volume)
      frameImage1 = volume.GetImageData()
      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage1.GetPointData().GetScalars())
      frame.append(frameImageArray)
      intensidad=np.mean(frameImageArray[:])
      mediana=np.median(frameImageArray)
      vector_int.append(intensidad)
      vector_med.append(mediana)
      slicer.mrmlScene.RemoveNode(volume)
      vect_int.append(volumen4D.GetImageData().GetScalarComponentAsDouble(int(ijk[0]),int(ijk[1]),int(ijk[2]),i))

    ## Creacion espacial
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    volumeLabels = vtk.vtkDoubleArray()
    volumeLabels.SetNumberOfTuples(6)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(6)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen4D.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumen4D.GetImageData().GetScalarType(),6)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen

    ##  Identificacion volumen de ingreso del contrste y suavizado
    vector_dif.append(np.diff(vector_med))  
    vector_max=np.where(vector_dif==np.max(vector_dif[0][(int(numero_frames*0.125)):(int(numero_frames*0.875))]))
    frame_max=vector_max[1][0] + 1

    frame[0]=np.sum(frame[0:frame_max-5], axis=0)/(frame_max-5+1)
    frame[1]=np.sum(frame[frame_max+2:numero_frames], axis=0)/(numero_frames-frame_max+2+1)

    frame[0]=frame[0].astype(int)
    frame[1]=frame[1].astype(int)
    smothingImageArray=abs(np.subtract(frame[1],frame[0]))

    ##  Transformada de intensidad [gamma] son min y max
    transformImageArray=smothingImageArray**1.2

    dimensions=volumen4D.GetImageData().GetDimensions()
    transformImageMatriz=np.reshape(transformImageArray, (dimensions[2],dimensions[1],dimensions[0]))
    
    ## Binarizacion numero 1
    bin1ImageArray=np.zeros(np.shape(transformImageArray)[0])
    binMask=transformImageMatriz[int(ijk[2]):int(ijk[2])+1,int(ijk[1]):int(ijk[1])+1,int(ijk[0]):int(ijk[0])+1]## cambie la variable por trasnformImageMatrix
    rang_bin=np.where(np.logical_and(transformImageArray>=np.min(binMask)*0.8,transformImageArray<=np.max(binMask)*1.1))
    bin1ImageArray[rang_bin[0]]=1##Resultado primera binarizacion

    ##  Operacion local
    bin1ImageMatriz=np.reshape(bin1ImageArray, (dimensions[2],dimensions[1],dimensions[0]))
    opLocalImageMatriz=np.zeros(np.shape(bin1ImageMatriz))##crear matriz de ceros
    for i in range(dimensions[1]/2):
      for j in range (dimensions[0]/2): 
            
            bin1ImageSubMatriz=bin1ImageMatriz[:,i*2:(i*2)+2,j*2:(j*2)+2]
            onesSubmatriz=np.where(bin1ImageSubMatriz==1)
            numOnes=np.size(onesSubmatriz[1])
            opLocalImageMatriz[:,i*2:(i*2)+2,j*2:(j*2)+2]=numOnes

    grosor=opLocalImageMatriz[int(ijk[2]),int(ijk[1]),int(ijk[0])]

    opLocalImageMatriz[:,:,0:(int(ijk[0])-int(grosor*0.6))]=0
    opLocalImageMatriz[:,:,(int(ijk[0])+int(grosor*0.6)):dimensions[0]]=0
    opLocalImageArray2=np.reshape(opLocalImageMatriz,-1)##Resultado operacion local


    opLocalImageMatriz2=np.zeros((dimensions[2],dimensions[0],dimensions[1]))##crear matriz de ceros
    for i in range(dimensions[2]):
      for j in range (dimensions[1]):
            for k in range (dimensions[0]): 
            
              opLocalImageMatriz2[i,k,j]=opLocalImageMatriz[i,j,k]
            

    opLocalImageArray=np.reshape(opLocalImageMatriz2,-1)##Resultado operacion local



    ## Binarizacion numero 2
    bin2ImageArray=np.zeros(np.shape(opLocalImageArray2)[0])
    binMask=opLocalImageMatriz[int(ijk[2]):int(ijk[2])+1,int(ijk[1]):int(ijk[1])+1,int(ijk[0]):int(ijk[0])+1]## cambie la variable por trasnformImageMatrix
    rang_bin=np.where(np.logical_and(opLocalImageArray2>=np.min(binMask)*0.4,opLocalImageArray2<=np.max(binMask)*1.6))
    bin2ImageArray[rang_bin[0]]=1##Resultado primera binarizacion


    mvImageArray.T[0] = bin2ImageArray
    mvNode=outputVolume
    mvNode.SetRASToIJKMatrix(ras2ijk)
    mvNode.SetIJKToRASMatrix(ijk2ras)
    mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
    mvNode.SetAndObserveImageData(mvImage)
    mvNode.SetNumberOfFrames(2)
    mvNode.SetLabelArray(volumeLabels)
    mvNode.SetName('PrimerasOp2')
    slicer.mrmlScene.AddNode(mvNode)

    volumen4D=slicer.util.getNode('PrimerasOp2')
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)

    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(volumen4D.GetImageData())
    extract1.SetComponents(0)
    extract1.Update()
    
    volume=slicer.vtkMRMLScalarVolumeNode()
    volume.SetAndObserveImageData(extract1.GetOutput())
    volume.SetName('OpLocalVol_gir')
    volume.SetIJKToRASMatrix(ijk2ras)
    volume.SetRASToIJKMatrix(ras2ijk)
    slicer.mrmlScene.AddNode(volume)
    
    Label=slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(Label)
    
    parameters = {}
    parameters['iterations'] = 1
    parameters['multiplier'] = 1
    parameters['neighborhood'] = 1
    parameters['labelvalue'] =1
    parameters['seed'] =fiducial.GetID()
    parameters['inputVolume'] =volume.GetID()
    parameters['outputVolume'] =Label.GetID()
    cliNode = slicer.cli.run( slicer.modules.simpleregiongrowingsegmentation,None,parameters,wait_for_completion=True)

    Label.SetName('Label_volume')
    bin2ImageMatriz=slicer.util.arrayFromVolume(Label)
    bin3ImageMatriz=bin1ImageMatriz*bin2ImageMatriz
    
    volumen= slicer.vtkMRMLScalarVolumeNode()
    volumen.SetAndObserveImageData(extract1.GetOutput())
    volumen.SetName('volumen')
    volumen.SetIJKToRASMatrix(ijk2ras)
    volumen.SetRASToIJKMatrix(ras2ijk)
    slicer.mrmlScene.AddNode(volumen)
    
    mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    mvDisplayNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(mvDisplayNode)
    mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
    mvDisplayNode.SetDefaultColorMap()

    volumeLabels = vtk.vtkDoubleArray()
    volumeLabels.SetNumberOfTuples(numero_frames)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_frames)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen4D.GetImageData().GetExtent())##Se le asigna la dimension del miltuvolumen   
    mvImage.AllocateScalars(volumen4D.GetImageData().GetScalarType(),numero_frames)##Se le asigna el tipo y numero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen
    
    
    
    prim=ijk2ras.MultiplyPoint([1,1,1,1])
    seg=ijk2ras.MultiplyPoint([2,2,2,1])
    vol_voxel=(seg[0]-prim[0])*(seg[1]-prim[1])*(seg[2]-prim[2])
    vector_vol_aort=[]
    for i in range(numero_frames):
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(imagenvtk4D)
      extract1.SetComponents(i) #Seleccionar un volumen lejano
      extract1.Update()
      volumen.SetAndObserveImageData(extract1.GetOutput())
      volumen.SetName('volumen_binarizado')
      slicer.mrmlScene.AddNode(volumen)
      ImageMatriz=slicer.util.arrayFromVolume(volumen)
      bin4ImageMatriz=bin3ImageMatriz*ImageMatriz
      bin4ImageArray=np.reshape(bin4ImageMatriz,-1)
      intensidad=np.mean(bin4ImageArray[:])
      vector_int_aort.append(intensidad)
      vol_rinon=abs(intensidad*vol_voxel)
      vector_vol_aort.append(vol_rinon)
      print('Volumen frame'+str(i)+': '+str(vol_rinon)+' mm3')
      mvImageArray.T[i] = bin4ImageArray
      
    RECONSTRUCTIONLogic().reconstruction2Function(outputVolume,mvImage,numero_frames,volumeLabels,frameLabelsAttr,'Multivolumen Segmentado',ras2ijk,ijk2ras)
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Segmentado completo')
    
    return vector_int_aort,numero_frames,vector_vol_aort,frame_max


class IMPORTLogic:
  def importFunction(self, mvNode,inputDir):

    # check if the output container exists
    #mvNode = self.outputSelector.currentNode()
    if mvNode == None:
      self.__status.text = 'Status: Select output node!'
      return


    fileNames = []    # file names on disk
    frameList = []    # frames as MRMLScalarVolumeNode's
    frameFolder = ""
    volumeLabels = vtk.vtkDoubleArray()
    frameLabelsAttr = ''
    frameFileListAttr = ''
    dicomTagNameAttr = 'NA'
    dicomTagUnitsAttr = 'na'
    teAttr = 1 ## Echo time
    trAttr = 1 ##Repetition time
    faAttr = 1 ##Flip angle

    # each frame is saved as a separate volume
    # first filter valid file names and sort alphabetically
    frames = []
    frame0 = None
   # inputDir = self.__fDialog.directory
    for f in os.listdir(inputDir):

      if not f.startswith('.'):
        fileName = inputDir+'/'+f
        fileNames.append(fileName)
    self.humanSort(fileNames)
    n=0
    nFrames = 0;
    for fileName in fileNames:
      (s,f) = self.readFrame(fileName)

      if s:
        if not frame0:
          frame0 = f
          frame0Image = frame0.GetImageData()
          frame0Extent = frame0Image.GetExtent()
        else:
          frameImage = f.GetImageData()
          frameExtent = frameImage.GetExtent()
          if frameExtent[1]!=frame0Extent[1] or frameExtent[3]!=frame0Extent[3] or frameExtent[5]!=frame0Extent[5]:
            continue

        nFrames += 1;


    if nFrames == 1:
      print('Single frame dataset - not reading as multivolume!')
      return

    # convert seconds data to milliseconds, which is expected by pkModeling.cxx line 81
    if dicomTagUnitsAttr == 's':
      frameIdMultiplier = 1000.0
      dicomTagUnitsAttr = 'ms'
    else:
      frameIdMultiplier = 1.0


    for i in range(nFrames):
      frameId = frameIdMultiplier*(i)
      frameLabelsAttr += str(frameId)+','
    frameLabelsAttr = frameLabelsAttr[:-1]


    ##EMPIEZA A FORMARCE EL VOLUMEN###############
    (volumeLabels, mvImage, mvImageArray)=RECONSTRUCTIONLogic().reconstruction1Function(frame0.GetImageData(),nFrames)
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    frame0.GetRASToIJKMatrix(ras2ijk)
    frame0.GetIJKToRASMatrix(ijk2ras)

    frameId = 0;
    for fileName in fileNames:
      #f: informaciï¿½n de cada scalar volume de cada corte
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

    RECONSTRUCTIONLogic().reconstruction2Function(mvNode,mvImage,nFrames,volumeLabels,frameLabelsAttr,str(nFrames)+' frames MultiVolume',ras2ijk,ijk2ras)



    return True
  def humanSort(self,l):
      """ Sort the given list in the way that humans expect.
          Conributed by Yanling Liu
      """
      convert = lambda text: int(text) if text.isdigit() else text
      alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
      l.sort( key=alphanum_key )
  def readFrame(self,file):
    sNode = slicer.vtkMRMLVolumeArchetypeStorageNode()
    sNode.ResetFileNameList()
    sNode.SetFileName(file)
    sNode.SetSingleFile(1)
    frame = slicer.vtkMRMLScalarVolumeNode()
    success = sNode.ReadData(frame)
    return (success,frame)


  def cleanup(self):
    pass

class REGISTERLogic:
  def registerFunction(self,inputVolume,mvNode ):
    """
    Run the actual algorithm
    """
    #se obtiene la escena y se obtiene el volumen 4D a partir del Volumen 4D de
    #entrada de la ventana desplegable
    escena = slicer.mrmlScene
    imagenvtk4D = inputVolume.GetImageData()
    #Se obtiene el nï¿½mero de volï¿½menes que tiene el volumen 4D
    numero_imagenes = inputVolume.GetNumberOfFrames()
    #filtro vtk para descomponer un volumen 4D
    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(imagenvtk4D)
    #matriz de transformaciï¿½n
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
    #se crea un vector para guardar el nï¿½mero del volumen que tenga un
    #desplazamiento de mas de 4mm en cualquier direcciï¿½n
    v=[]

    #se hace un ciclo for para registrar todos los demï¿½s volï¿½menes del volumen 4D
    #con el primer volumen que se definiï¿½ como fijo
    (volumeLabels, mvImage, mvImageArray)=RECONSTRUCTIONLogic().reconstruction1Function(volumenFijo.GetImageData(),numero_imagenes)



    ##Se hace la conversiï¿½n y se obtiene la matriz de transformaciï¿½n del nodo

    volumenFijo.GetRASToIJKMatrix(ras2ijk)
    volumenFijo.GetIJKToRASMatrix(ijk2ras)
    frameLabelsAttr=''
    frames = []

    for i in range(numero_imagenes):
      # extraigo la imagen mï¿½vil en la posiciï¿½n i+1 ya que el primero es el fijo
      imagen_movil = extract1.SetComponents(i+1) #Seleccionar un volumen i+1
      extract1.Update()
      #Creo el volumen mï¿½vil, y realizo el mismo procedimiento que con el fijo
      volumenMovil = slicer.vtkMRMLScalarVolumeNode();
      volumenMovil.SetRASToIJKMatrix(ras2ijk)
      volumenMovil.SetIJKToRASMatrix(ijk2ras)
      volumenMovil.SetAndObserveImageData(extract1.GetOutput())
      volumenMovil.SetName('movil '+str(i+1))
      escena.AddNode(volumenMovil)

      #creamos la transformada para alinear los volï¿½menes
      transformadaSalida = slicer.vtkMRMLLinearTransformNode()
      transformadaSalida.SetName('Transformadaderegistro'+str(i+1))
      slicer.mrmlScene.AddNode(transformadaSalida)
      #parï¿½metros para la operaciï¿½n de registro
      parameters = {}
      #parameters['InitialTransform'] = transI.GetID()
      parameters['fixedVolume'] = volumenFijo.GetID()
      parameters['movingVolume'] = volumenMovil.GetID()
      parameters['transformType'] = 'Affine'
      parameters['outputTransform'] = transformadaSalida.GetID()
      parameters['outputVolume'] =volumenMovil.GetID()

##      parameters['outputVolume']=volumenSalida.GetID()
      #Realizo el registro
      cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters,wait_for_completion=True)
      slicer.mrmlScene.RemoveNode(volumenFijo)
      slicer.mrmlScene.RemoveNode(volumenMovil)
##      slicer.mrmlScene.RemoveNode(transformadaSalida)
      #obtengo la transformada lineal que se usï¿½ en el registro
      transformada=escena.GetFirstNodeByName('Transformadaderegistro'+str(i+1))
      #Obtengo la matriz de la transformada, esta matriz es de dimensiones 4x4
      #en la cual estan todos los desplazamientos y rotaciones que se hicieron
      #en la transformada, a partir de ella se obtienen los volumenes que se
      #desplazaron mas de 4mm en cualquier direccion

      frameImage = volumenMovil.GetImageData()
      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
      mvImageArray.T[i] = frameImageArray

      hm = vtk.vtkMatrix4x4();
      transformadaSalida.GetMatrixTransformToWorld(hm);
      volumenMovil.ApplyTransformMatrix(hm);
      volumenMovil.SetAndObserveTransformNodeID(None)

      frameId = i;
      volumeLabels.SetComponent(i, 0, frameId)
      frameLabelsAttr += str(frameId)+','

    RECONSTRUCTIONLogic().reconstruction2Function(mvNode,mvImage,numero_imagenes,volumeLabels,frameLabelsAttr,'MultiVolume Registrado',ras2ijk,ijk2ras)

    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Registro completo')
    return True
  
class FILTERLogic:

  def filterFunction(self,volumen4D,mvNode):
##    volumen4D = self.inputFilterSelector.currentNode()
    imagenvtk4D = volumen4D.GetImageData()
    numero_imagenes = volumen4D.GetNumberOfFrames()
    #filtro vtk para descomponer un volumen 4D
    #matriz de transformacion
    ras2ijk = vtk.vtkMatrix4x4()
    ijk2ras = vtk.vtkMatrix4x4()
    #le solicitamos al volumen original que nos devuelva sus matrices
    volumen4D.GetRASToIJKMatrix(ras2ijk)
    volumen4D.GetIJKToRASMatrix(ijk2ras)
    extract1 = vtk.vtkImageExtractComponents()
    extract1.SetInputData(imagenvtk4D)
    escena=slicer.mrmlScene
    extract1.SetComponents(10) #Seleccionar un volumen lejano
    extract1.Update()
    #Creo un volumen movil, y realizamos el mismo procedimiento que con el fijo


##    mvNode=self.outputFilterSelector.currentNode()
    frameLabelsAttr=''
    frames = []
    volumeLabels = vtk.vtkDoubleArray()

    volumeLabels.SetNumberOfTuples(numero_imagenes)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_imagenes)


    fd = vtk.vtkImageAnisotropicDiffusion3D();
    fd.SetInputData(extract1.GetOutput())
    fd.Update();

    (volumeLabels, mvImage, mvImageArray)=RECONSTRUCTIONLogic().reconstruction1Function(fd.GetOutput(),numero_imagenes)


    for i in range(numero_imagenes):
      extract1.SetComponents(i) #Seleccionar un volumen lejano
      extract1.Update()
      #Creo un volumen movil, y realizamos el mismo procedimiento que con el fijo
      import sitkUtils
      import SimpleITK as itk
      sitkReader = itk.ImageFileReader()
      sitkReader.SetDebug(False)

      volume=slicer.vtkMRMLScalarVolumeNode()
      volume.SetAndObserveImageData(extract1.GetOutput())
      volume.SetName('Vol10')
      volume.SetIJKToRASMatrix(ijk2ras)
      volume.SetRASToIJKMatrix(ras2ijk)
      slicer.mrmlScene.AddNode(volume)
      
      volume.GetName()
      imgNodeName=volume.GetName()
      import sitkUtils
      imgNodeName=volume.GetName()
      sitkReader.SetFileName(sitkUtils.GetSlicerITKReadWriteAddress(imgNodeName))
      img = sitkReader.Execute()
      img.GetPixelIDTypeAsString()

      SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter()
      smoothing= SmoothingFilterType
      smoothing.SetTimeStep(0.06250)
      smoothing.SetNumberOfIterations(5)
      smoothing.SetConductanceParameter(3)
      img=itk.DivideReal(img, 4.0)
      smoothing_img = smoothing.Execute(img)



      slice_vol = slicer.vtkMRMLScalarVolumeNode()
      slice_vol.SetScene(slicer.mrmlScene)
      slice_vol.SetName('Volume Filtrado')
      slicer.mrmlScene.AddNode(slice_vol)
      outputNodeName = slice_vol.GetName()
      nodeWriteAddress = sitkUtils.GetSlicerITKReadWriteAddress(outputNodeName)
      itk.WriteImage(smoothing_img, nodeWriteAddress)
      slice_vol.UnRegister(slicer.mrmlScene)

      
      

      frameImage = slice_vol.GetImageData()

      frameImageArray = vtk.util.numpy_support.vtk_to_numpy(frameImage.GetPointData().GetScalars())
      mvImageArray.T[i] = frameImageArray

    RECONSTRUCTIONLogic().reconstruction2Function(mvNode,mvImage,numero_imagenes,volumeLabels,frameLabelsAttr,'MultiVolume Filtrado',ras2ijk,ijk2ras)
    qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python','Filtrado completo')
    return True



class RECONSTRUCTIONLogic:
  global volumeLabels
  global mvImage
  global  mvNode
  global mvImageArray

  def reconstruction1Function(self, volumen,numero_imagenes):
    frameLabelsAttr=''
    frames = []
    volumeLabels = vtk.vtkDoubleArray()

    volumeLabels.SetNumberOfTuples(numero_imagenes)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(numero_imagenes)

    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(volumen.GetExtent())##Se le asigna la dimensiï¿½n del miltuvolumen
    mvImage.AllocateScalars(volumen.GetScalarType(), numero_imagenes)##Se le asigna el tipo y nï¿½mero de cortes al multivolumen
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())## Se crea la matriz de datos donde va a ir la imagen



    return volumeLabels, mvImage, mvImageArray

  def reconstruction2Function(self, mvNode,mvImage,numero_imagenes,volumeLabels,frameLabelsAttr,nombre,ras2ijk,ijk2ras):

    mvNode.SetRASToIJKMatrix(ras2ijk)
    mvNode.SetIJKToRASMatrix(ijk2ras)
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

    mvNode.SetName(nombre)
    Helper.SetBgFgVolumes(mvNode.GetID(),None)

