import vtk, qt, ctk, slicer

class INTENSIDAD:
  def __init__(self, parent):
    parent.title = "Curvas Intensidad"
    parent.categories = ["PIS_BKL"]
    parent.dependencies = []
    parent.contributors = ["Katy","Bandy","Laura"] 
    parent.helpText = """ """
    parent.acknowledgementText = """ """  
    self.parent = parent

class INTENSIDADWidget:
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

    
    #INTENSIDAD Vs VOLUMEN
    #BOTON
    self.VolumenCollapsibleButton = ctk.ctkCollapsibleButton()
    self.VolumenCollapsibleButton.text = "Intensidad Vs Volumen"
    self.layout.addWidget(self.VolumenCollapsibleButton)
    #LAYOUT
    self.VolumenFormLayout = qt.QFormLayout(self.VolumenCollapsibleButton)


    # BOTON GRAFICAR VOLUMEN
    VolumenButton = qt.QPushButton("Graficar")
    VolumenButton.toolTip = ""
    self.VolumenFormLayout.addWidget(VolumenButton)
    VolumenButton.connect('clicked(bool)', self.grafVolumen)

    self.VolumenButton = VolumenButton

    #INTENSIDAD Vs TIEMPO
    #BOTON
    self.TiempoCollapsibleButton = ctk.ctkCollapsibleButton()
    self.TiempoCollapsibleButton.text = "Intensidad Vs Tiempo"
    self.layout.addWidget(self.TiempoCollapsibleButton)
    # LAYOUT
    self.TiempoFormLayout = qt.QFormLayout(self.TiempoCollapsibleButton)

    self.plotRDFrame = ctk.ctkCollapsibleButton();
    self.plotRDFrame.text = "Grafica";
    self.plotRDFrame.collapsed = 0;
    plotRDFrameLayout = qt.QGridLayout(self.plotRDFrame);
    self.layout.addWidget(self.plotRDFrame);


    #BOTON GRAFICAR TIEMPO
    TiempoButton = qt.QPushButton("Graficar")
    TiempoButton.toolTip = ""
    self.TiempoFormLayout.addWidget(TiempoButton)
    TiempoButton.connect('clicked(bool)', self.grafTiempo)

    self.TiempoButton = TiempoButton
    
    self.chartRDView = ctk.ctkVTKChartView(w);
    plotRDFrameLayout.addWidget(self.chartRDView,3,0,1,3);

    self.chartRD = self.chartRDView.chart();

    self.xArrayRD = vtk.vtkFloatArray();
    self.yArrayRD = vtk.vtkFloatArray();
    self.yArrayRI = vtk.vtkFloatArray();
    self.yArrayA = vtk.vtkFloatArray();

    self.xArrayRD.SetName('');
    self.yArrayRD.SetName('signal intesity RD');
    self.yArrayRI.SetName('signal intesity RI');
    self.yArrayA.SetName('signal intesity A');
        
    self.tableRD = vtk.vtkTable()

    self.tableRD.AddColumn(self.xArrayRD)
    self.tableRD.AddColumn(self.yArrayRD)
    self.tableRD.AddColumn(self.yArrayRI)
    self.tableRD.AddColumn(self.yArrayA)

  def grafVolumen(self): 
    escena=slicer.mrmlScene
    volumen4D= escena.GetNodeByID('vtkMRMLMultiVolumeNode1')
    Vector1=[]
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    fidList_1 = slicer.util.getNode('vtkMRMLMultiVolumeNode1')
    Imagenvtk4D = fidList_1.GetImageData()
    numOfVol_1 = Imagenvtk4D.GetNumberOfScalarComponents()
    for i in range(numFids):
      ras = [0,0,0]
      fidList.GetNthFiducialPosition(i,ras)
      ras.append(1)
      Vector1.append(ras)
    ras_rinon_der=Vector1[0]
    ras_rinon_izq=Vector1[1]
    ras_aorta=Vector1[2]
    ras2ijk_rinon_der=vtk.vtkMatrix4x4()
    ras2ijk_rinon_izq=vtk.vtkMatrix4x4()
    ras2ijk_aorta=vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk_rinon_der)
    volumen4D.GetRASToIJKMatrix(ras2ijk_rinon_izq)
    volumen4D.GetRASToIJKMatrix(ras2ijk_aorta)
    ijk_rinon_der=ras2ijk_rinon_der.MultiplyPoint([ras_rinon_der[0],ras_rinon_der[1],ras_rinon_der[2],1])
    ijk_rinon_izq=ras2ijk_rinon_izq.MultiplyPoint([ras_rinon_izq[0],ras_rinon_izq[1],ras_rinon_izq[2],1])
    ijk_aorta=ras2ijk_aorta.MultiplyPoint([ras_aorta[0],ras_aorta[1],ras_aorta[2],1])
    Vector_int_rinon_der=[]
    Vector_int_rinon_izq=[]
    Vector_int_aorta=[]
    for i in range(numOfVol_1):
      intensidad_rinon_der=Imagenvtk4D.GetScalarComponentAsDouble(int(ijk_rinon_der[0]),int(ijk_rinon_der[1]),int(ijk_rinon_der[2]),i)
      intensidad_rinon_izq=Imagenvtk4D.GetScalarComponentAsDouble(int(ijk_rinon_izq[0]),int(ijk_rinon_izq[1]),int(ijk_rinon_izq[2]),i)
      intensidad_aorta=Imagenvtk4D.GetScalarComponentAsDouble(int(ijk_aorta[0]),int(ijk_aorta[1]),int(ijk_aorta[2]),i)
      Vector_int_rinon_der.append(intensidad_rinon_der)
      Vector_int_rinon_izq.append(intensidad_rinon_izq)
      Vector_int_aorta.append(intensidad_aorta)
    vol=range(numOfVol_1)

    self.tableRD.SetNumberOfRows(numOfVol_1)
    for i in range(0, numOfVol_1):
        self.tableRD.SetValue(i, 0, vol[i])
        self.tableRD.SetValue(i, 1, Vector_int_rinon_der[i])
        self.tableRD.SetValue(i, 2, Vector_int_rinon_izq[i])
        self.tableRD.SetValue(i, 3, Vector_int_aorta[i])

    self.lineRD = self.chartRD.AddPlot(vtk.vtkChart.LINE)
    self.lineRD.SetInputData(self.tableRD, 0, 1)
    self.lineRD.SetColor(0, 0, 0, 255)
    self.lineRD.SetWidth(1.0)

    self.lineRD.GetXAxis().SetTitle("Indice de volumen")
    self.lineRD.GetYAxis().SetTitle("Intensidad")
    self.lineRD.Update()
    
    self.lineRI = self.chartRD.AddPlot(vtk.vtkChart.LINE)
    self.lineRI.SetInputData(self.tableRD, 0, 2)
    self.lineRI.SetColor(128,90, 0, 255)
    self.lineRI.SetWidth(1.0)
    self.lineRI.Update()

    self.lineA = self.chartRD.AddPlot(vtk.vtkChart.LINE)
    self.lineA.SetInputData(self.tableRD, 0, 3)
    self.lineA.SetColor(12, 678, 87)
    self.lineA.SetWidth(1.0)
    self.lineA.Update()
    
  def grafTiempo(self):
    escena=slicer.mrmlScene
    volumen4D= escena.GetNodeByID('vtkMRMLMultiVolumeNode1')
    Vector1=[]
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    fidList_1 = slicer.util.getNode('vtkMRMLMultiVolumeNode1')
    Imagenvtk4D = fidList_1.GetImageData()
    numOfVol_1 = Imagenvtk4D.GetNumberOfScalarComponents()
    for i in range(numFids):
      ras = [0,0,0]
      fidList.GetNthFiducialPosition(i,ras) 
      Vector1.append(ras)
    ras_rinon_der=Vector1[0]
    ras_rinon_izq=Vector1[1]
    ras_aorta=Vector1[2]
    ras2ijk_rinon_der=vtk.vtkMatrix4x4()
    ras2ijk_rinon_izq=vtk.vtkMatrix4x4()
    ras2ijk_aorta=vtk.vtkMatrix4x4()
    volumen4D.GetRASToIJKMatrix(ras2ijk_rinon_der)
    volumen4D.GetRASToIJKMatrix(ras2ijk_rinon_izq)
    volumen4D.GetRASToIJKMatrix(ras2ijk_aorta)
    ijk_rinon_der=ras2ijk_rinon_der.MultiplyPoint([ras_rinon_der[0],ras_rinon_der[1],ras_rinon_der[2],1])
    ijk_rinon_izq=ras2ijk_rinon_izq.MultiplyPoint([ras_rinon_izq[0],ras_rinon_izq[1],ras_rinon_izq[2],1])
    ijk_aorta=ras2ijk_aorta.MultiplyPoint([ras_aorta[0],ras_aorta[1],ras_aorta[2],1])
    Vector_int_rinon_der=[]
    Vector_int_rinon_izq=[]
    Vector_int_aorta=[]
    for i in range(numOfVol_1):
      intensidad_rinon_der=Imagenvtk4D.GetScalarComponentAsDouble(int(ijk_rinon_der[0]),int(ijk_rinon_der[1]),int(ijk_rinon_der[2]),i)
      intensidad_rinon_izq=Imagenvtk4D.GetScalarComponentAsDouble(int(ijk_rinon_izq[0]),int(ijk_rinon_izq[1]),int(ijk_rinon_izq[2]),i)
      intensidad_aorta=Imagenvtk4D.GetScalarComponentAsDouble(int(ijk_aorta[0]),int(ijk_aorta[1]),int(ijk_aorta[2]),i)
      Vector_int_rinon_der.append(intensidad_rinon_der)
      Vector_int_rinon_izq.append(intensidad_rinon_izq)
      Vector_int_aorta.append(intensidad_aorta)
    vol=range(numOfVol_1)

    self.tableRD.SetNumberOfRows(numOfVol_1)
    for i in range(0, numOfVol_1):
        self.tableRD.SetValue(i, 0, vol[i])
        self.tableRD.SetValue(i, 1, Vector_int_rinon_der[i])
        self.tableRD.SetValue(i, 2, Vector_int_rinon_izq[i])
        self.tableRD.SetValue(i, 3, Vector_int_aorta[i])

    self.lineRD = self.chartRD.AddPlot(vtk.vtkChart.LINE)
    self.lineRD.SetInputData(self.tableRD, 0, 1)
    self.lineRD.SetColor(0, 0, 0, 255)
    self.lineRD.SetWidth(1.0)

    self.lineRD.GetXAxis().SetTitle("Tiempo")
    self.lineRD.GetYAxis().SetTitle("Intensidad")
    self.lineRD.Update()
    
    self.lineRI = self.chartRD.AddPlot(vtk.vtkChart.LINE)
    self.lineRI.SetInputData(self.tableRD, 0, 2)
    self.lineRI.SetColor(128,90, 0, 255)
    self.lineRI.SetWidth(1.0)
    self.lineRI.Update()

    self.lineA = self.chartRD.AddPlot(vtk.vtkChart.LINE)
    self.lineA.SetInputData(self.tableRD, 0, 3)
    self.lineA.SetColor(12, 678, 87)
    self.lineA.SetWidth(1.0)
    self.lineA.Update()


      

    
   

    
   

