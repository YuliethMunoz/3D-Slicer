import vtk, qt, ctk, slicer, dicom


class PIS:
  def __init__(self, parent):
    parent.title = "pIS" 
    parent.categories = ["Procesamiento"]
    parent.dependencies = []
    parent.contributors = [" (Universidad de Antioquia)"] # replace with "Firstname Lastname (Organization)"
    parent.helpText = """
        """
    parent.acknowledgementText = """
    
""" 
    self.parent=parent


class PISWidget:
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

######Importar el volumen en formato DICOM#####################################
    importDataCollapsibleButton = ctk.ctkCollapsibleButton()
    importDataCollapsibleButton.text = "DICOM"
    self.layout.addWidget(importDataCollapsibleButton)

    importDataFormLayout = qt.QFormLayout(importDataCollapsibleButton)


    self.__fDialog = ctk.ctkDirectoryButton()
    self.__fDialog.caption = 'Input directory'
    importDataFormLayout.addRow('Input directory:', self.__fDialog)

    # Boton de importar

    self.buttonImport = qt.QPushButton("Boton")
    self.buttonImport.toolTip = "Run the algorithm."
    ##self.buttonImport.enabled = True
    importDataFormLayout.addRow("                                       ", self.buttonImport)

    self.buttonImport.connect('clicked(bool)', self.importFunction)


    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = True
    self.inputSelector.noneEnabled = True
    self.inputSelector.showHidden = True
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    importDataFormLayout.addRow("Volumen 4D: ", self.inputSelector)
    self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.inputSelector, 'setMRMLScene(vtkMRMLScene*)')
    

    #### Crear desplegable para seleccionar direccion del volumen
    self.__fDialogOutput = ctk.ctkDirectoryButton()
    self.__fDialogOutput.caption = 'DICOM directory'
    importDataFormLayout.addRow('DiCOM directory:', self.__fDialogOutput)




  def importFunction(self):
    inputVolume= self.inputSelector.currentNode()
    inputDir = self.__fDialog.directory
    outputDir=self.__fDialogOutput
    fileNames = []
    metadatos= []
    for f in os.listdir(inputDir):
      if not f.startswith('.'):
        fileName = str(inputDir+'/'+f)
        metadato=dicom.read_file(fileName)
        fileNames.append(fileName)
        metadatos.append(metadato)
        Parameters ['patientName']= KAty
        Parameters ['patientID']=metadato.PatientID
##        Parameters ['patientComments']=
        Parameters ['studyID']=metadato.StudyID
        Parameters ['studyDate']=metadato.StudyDate
        Parameters ['studyComments']=metadato.StudyComments
        Parameters ['studyDescription']=metadato.StudyDescription
        Parameters ['modality']=metadato.Modality
        Parameters ['manufacturer']=metadato.Manufacturer
##        Parameters ['model']=
        Parameters ['seriesNumber']=metadato.SeriesNumber
        Parameters ['seriesDescription']=metadato.SeriesDescription
##        Parameters ['rescaleIntercept']=metadato.Rescaleintercept
##  Parameter (3/1): rescaleSlope (Rescale slope)
        Parameters ['inputVolume']=inputVolume
        Parameters ['dicomDirectory']=outputDir
        Parameters ['dicomPrefix']='IMG'
        Parameters ['dicomNumberFormat']='%04d'
        cliNode = slicer.cli.run( slicer.modules.createdicomseries,None,parameters,wait_for_completion=True)


        
##  Parameter (5/3): reverseImages (Reverse Slices)
##  Parameter (5/4): useCompression (Use Compression)
##  Parameter (5/5): Type (Output Type:)
        




##
##
##
##
##
##parameters['patientName'] = 
##parameters['patientID'] = 
##parameters['patientComments'] = 
##parameters['studyID'] = 
##
##
##cliNode = slicer.cli.run( slicer.modules.createdicomseries,None,parameters,wait_for_completion=True)
##
##cliModule = slicer.modules.createdicomseries
##n=cliModule.cliModuleLogic().CreateNode()
##for groupIndex in xrange(0,n.GetNumberOfParameterGroups()):
##  for parameterIndex in xrange(0,n.GetNumberOfParametersInGroup(groupIndex)):
##    print '  Parameter ({0}/{1}): {2} ({3})'.format(groupIndex, parameterIndex, n.GetParameterName(groupIndex, parameterIndex), n.GetParameterLabel(groupIndex, parameterIndex))

