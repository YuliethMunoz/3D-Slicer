from __main__ import vtk, qt, ctk, slicer

#
#HelloLaplace
#


class moduloMASCARA1:
  def __init__(self, parent):
    parent.title = "Mascara nueva"
    parent.categories = ["Evaluar metabolismo"]
    parent.dependencies = []
    parent.contributors = ["Laura Carolina Rozo Hoyos",
                           "Yulieth Katerine Munoz Zapata",
                           "Estudiantes de bioingenieria, Universidad de Antioquia"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    """
    parent.acknowledgementText = """""" # replace with organization, grant and thanks.
    self.parent = parent


class moduloMASCARA1Widget:
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
    # Collapsible button
    self.mascaraCollapsibleButton = ctk.ctkCollapsibleButton()
    self.mascaraCollapsibleButton.text = "Creacion de la Mascara Corteza derecha e izquierda"
    self.layout.addWidget(self.mascaraCollapsibleButton)

    # Creacion de el boton desplegable para la creacion  de la mascara
    self.mascaraFormLayout = qt.QFormLayout(self.mascaraCollapsibleButton)
    




      #selector de imgen a partir de la cual se crea la mascara
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.objectName = 'Seleccionar imagen'
    self.inputSelector.toolTip = 'Seleccione la imagen de entrada'
    self.inputSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.inputSelector.noneEnabled = True
    self.inputSelector.addEnabled = False  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
    self.inputSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    self.mascaraFormLayout.addRow("Imagen de entrada:", self.inputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputSelector, 'setMRMLScene(vtkMRMLScene*)')

     #selector de imgen que que contendra la mascara 
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.objectName = 'imagenSelector'
    self.outputSelector.toolTip = 'Seleccione la imagen que desea centrar'
    self.outputSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.outputSelector.noneEnabled = True
    self.outputSelector.addEnabled = True  # Se habilita la posibildad al usuario de crear un nuevo nodo con este widget
    self.outputSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    self.mascaraFormLayout.addRow("Corteza cerebral derecha:", self.outputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.outputSelector, 'setMRMLScene(vtkMRMLScene*)')  

    self.petSelector = slicer.qMRMLNodeComboBox()
    self.petSelector.objectName = 'imagenSelector'
    self.petSelector.toolTip = 'Seleccione la imagen que desea centrar'
    self.petSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.petSelector.noneEnabled = True
    self.petSelector.addEnabled = True  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
    self.petSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.petSelector.setMRMLScene(slicer.mrmlScene)
    self.mascaraFormLayout.addRow("Imagen PET:", self.petSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.petSelector, 'setMRMLScene(vtkMRMLScene*)')  

    self.mascaraDerechaSelector = slicer.qMRMLNodeComboBox()
    self.mascaraDerechaSelector.objectName = 'imagenSelector'
    self.mascaraDerechaSelector.toolTip = 'Seleccione la imagen que desea centrar'
    self.mascaraDerechaSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.mascaraDerechaSelector.noneEnabled = True
    self.mascaraDerechaSelector.addEnabled = True  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
    self.mascaraDerechaSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.mascaraDerechaSelector.setMRMLScene(slicer.mrmlScene)
    self.mascaraFormLayout.addRow("Corteza derecha-mascara:", self.mascaraDerechaSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.mascaraDerechaSelector, 'setMRMLScene(vtkMRMLScene*)')

    self.mascaraIzquierdaSelector = slicer.qMRMLNodeComboBox()
    self.mascaraIzquierdaSelector.objectName = 'imagenSelector'
    self.mascaraIzquierdaSelector.toolTip = 'Seleccione la imagen que desea centrar'
    self.mascaraIzquierdaSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.mascaraIzquierdaSelector.noneEnabled = True
    self.mascaraIzquierdaSelector.addEnabled = True  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
    self.mascaraIzquierdaSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
    self.mascaraIzquierdaSelector.setMRMLScene(slicer.mrmlScene)
    self.mascaraFormLayout.addRow("Corteza izquierda-mascara:", self.mascaraIzquierdaSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.mascaraIzquierdaSelector, 'setMRMLScene(vtkMRMLScene*)')


    
    # Crear button
    mascaraDerechaButton = qt.QPushButton("Crear mascara corteza derecha")
    self.mascaraFormLayout.addWidget(mascaraDerechaButton)
    mascaraDerechaButton.connect('clicked(bool)', self.CrearDerecha)
    # Add vertical spacer
    self.layout.addStretch(1)

    
    # Set local var as instance attribute
    self.mascaraDerechaButton = mascaraDerechaButton

        # Crear button
    mascaraIzquierdaButton = qt.QPushButton("Crear mascara corteza izquierda")
    self.mascaraFormLayout.addWidget(mascaraIzquierdaButton)
    mascaraIzquierdaButton.connect('clicked(bool)', self.CrearIzquierda)
    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.mascaraIzquierdaButton = mascaraIzquierdaButton

    ################BOTON PARA LA CORTEZA DERECHA####################

  def CrearDerecha(self):

     ###  imagenes a trabajar
      inputVolume = self.inputSelector.currentNode()
      outputVolume = self.outputSelector.currentNode()
      petVolume = self.petSelector.currentNode()
      mascaraDerechaVolume = self.mascaraDerechaSelector.currentNode()

    
      salida = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(salida)
      salida.SetName('salida')

      
      parameters={}      
      parameters['InputVolume']= inputVolume
      parameters['OutputVolume']= salida
      parameters['ThresholdType']= 'Above'
      parameters['Lower']= 0
      parameters['Upper']= 0
      parameters['Outsite']=0
      parameters['ThresholdValue']= 42
      cliNode=slicer.cli.run(slicer.modules.thresholdscalarvolume,None,parameters, wait_for_completion=True)
      parameters={}
      parameters['InputVolume']= salida
      parameters['OutputVolume']= outputVolume
      parameters['ThresholdType']= 'Below'
      parameters['Lower']= 0
      parameters['Upper']= 0
      parameters['Outsite']=0
      parameters['ThresholdValue']= 42
      cliNode=slicer.cli.run(slicer.modules.thresholdscalarvolume,None,parameters, wait_for_completion=True)

      parameters={}
      parameters['InputVolume']= petVolume
      parameters['MaskVolume']= outputVolume
      parameters['OutputVolume']= mascaraDerechaVolume
      parameters['Label']= 42
      parameters['Replace']= 0
      cliNode=slicer.cli.run(slicer.modules.maskscalarvolume,None,parameters, wait_for_completion=True)
      
      imagen=slicer.util.getNode('Volume_1')
      imagenData=imagen.GetImageData()
      intensidadTotal=0
      for i in range (127):
	for j in range (127,0,-1):		
		intensidadTotal=intensidadTotal+(imagenData.GetScalarComponentAsDouble(int(i),int(j), int(45), 0))

      print(intensidadTotal)

          ################BOTON PARA LA CORTEZA IZQUIERDA####################

  def CrearIzquierda(self):

     ###  imagenes a trabajar
      inputVolume = self.inputSelector.currentNode()
      outputVolume = self.outputSelector.currentNode()
      petVolume = self.petSelector.currentNode()
      mascaraIzquierdaVolume = self.mascaraIzquierdaSelector.currentNode()

    
      salida = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(salida)
      salida.SetName('salida')

      
      parameters={}      
      parameters['InputVolume']= inputVolume
      parameters['OutputVolume']= salida
      parameters['ThresholdType']= 'Above'
      parameters['Lower']= 0
      parameters['Upper']= 0
      parameters['Outsite']=0
      parameters['ThresholdValue']= 3
      cliNode=slicer.cli.run(slicer.modules.thresholdscalarvolume,None,parameters, wait_for_completion=True)
      parameters={}
      parameters['InputVolume']= salida
      parameters['OutputVolume']= outputVolume
      parameters['ThresholdType']= 'Below'
      parameters['Lower']= 0
      parameters['Upper']= 0
      parameters['Outsite']=0
      parameters['ThresholdValue']= 3
      cliNode=slicer.cli.run(slicer.modules.thresholdscalarvolume,None,parameters, wait_for_completion=True)

      parameters={}
      parameters['InputVolume']= petVolume
      parameters['MaskVolume']= outputVolume
      parameters['OutputVolume']= mascaraIzquierdaVolume
      parameters['Label']= 3
      parameters['Replace']= 0
      cliNode=slicer.cli.run(slicer.modules.maskscalarvolume,None,parameters, wait_for_completion=True)
      
      imagenIzquierda=slicer.util.getNode('Volume_2')
      imagenDataIzquierda=imagenIzquierda.GetImageData()
      intensidadTotalIzquierda=0
      for i in range (127):
	for j in range (127,0,-1):		
		intensidadTotalIzquierda=intensidadTotalIzquierda+(imagenDataIzquierda.GetScalarComponentAsDouble(int(i),int(j), int(45), 0))

      print(intensidadTotalIzquierda)

  




      
    
  

