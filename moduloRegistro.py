# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer


class moduloRegistro:

    def __init__(self, parent):
        parent.title = "Registro"
        parent.categories = ["SEEG"]
        parent.dependencies = []
        parent.contributors = [u"Mateo Ramírez Uribe, John Fredy Ochoa, Jhon Jairo Velasquez"]
        parent.helpText = \
    u"""
    Este módulo permite registrar las imágenes usadas en planeación de SEEG y las imágenes
    usadas para la fusión en la evaluación de SEEG. También permite centrar imágenes y guardar
    la transformación para centrar la imagen y su transformada inversa.
     """

        parent.acknowledgementText = u"""
    Grupo GIBIC universidad de Antioquia, Instituto Neurológico de colombia."
    """  # replace with organization, grant and thanks.
        self.parent = parent


class moduloRegistroWidget:

    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())  # dispone los elementos de manera vertical
            self.parent.setMRMLScene(slicer.mrmlScene)  # Asocia la escena mrml al widget
        else:
            self.parent = parent
            self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()

    def setup(self):

        # Collapsible button
        self.centrarCollapsibleButton = ctk.ctkCollapsibleButton()
        self.centrarCollapsibleButton.text = u"Centrar imagen y guardar transformación"
        self.layout.addWidget(self.centrarCollapsibleButton)

        # Layout within the collapsible button
        self.centrarLayout = qt.QFormLayout(self.centrarCollapsibleButton)

        #selector de imgen a centrar
        self.imagenSelector = slicer.qMRMLNodeComboBox()
        self.imagenSelector.objectName = 'imagenSelector'
        self.imagenSelector.toolTip = 'Seleccione la imagen que desea centrar'
        self.imagenSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
        self.imagenSelector.noneEnabled = True
        self.imagenSelector.addEnabled = False  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
        self.imagenSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
##        self.imagenSelector.connect('currentNodeChanged(bool)', self.enableOrDisableCentrarButton)
        self.imagenSelector.setMRMLScene(slicer.mrmlScene)
        self.centrarLayout.addRow("Volumen a centrar:", self.imagenSelector)
        self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.imagenSelector, 'setMRMLScene(vtkMRMLScene*)')

        #Boton centrar
        self.centrarButton = qt.QPushButton("Centrar")
        self.centrarButton.toolTip = u"Centre la imagen y guarde la transoformación de sentrado y su transformada inversa"
        self.centrarLayout.addWidget(self.centrarButton)
        self.centrarButton.connect('clicked(bool)', self.onCentrar)
        self.centrarButton.enabled = True
        self.layout.addStretch(1)

        # Collapsible button
        self.registrarCollapsibleButton = ctk.ctkCollapsibleButton()
        self.registrarCollapsibleButton.text = u"Registrar imágenes"
        self.layout.addWidget(self.registrarCollapsibleButton)

        # Layout within the collapsible button
        self.registrarLayout = qt.QFormLayout(self.registrarCollapsibleButton)

        #selector de transformacion
        self.transformSelector = slicer.qMRMLNodeComboBox()
        self.transformSelector.objectName = 'transformSelector'
        self.transformSelector.toolTip = u'El método requiere que sólo centre la resonancia con este modulo'
        self.transformSelector.nodeTypes = ['vtkMRMLLinearTransformNode']
        self.transformSelector.noneEnabled = True
        self.transformSelector.addEnabled = True  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
        self.transformSelector.removeEnabled = True  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
##        self.transformSelector.connect('currentNodeChanged(bool)', self.enableOrDisableRegistrarButton)
        self.transformSelector.setMRMLScene(slicer.mrmlScene)
        self.registrarLayout.addRow("Transformacion de entrada:", self.transformSelector)
        self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.transformSelector, 'setMRMLScene(vtkMRMLScene*)')

        #selector de imgen fija
        self.imagenFijaSelector = slicer.qMRMLNodeComboBox()
        self.imagenFijaSelector.objectName = 'imagenFijaSelector'
        self.imagenFijaSelector.toolTip = 'Seleccione la imagen fija'
        self.imagenFijaSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
        self.imagenFijaSelector.noneEnabled = True
        self.imagenFijaSelector.addEnabled = False  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
        self.imagenFijaSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
##        self.imagenFijaSelector.connect('currentNodeChanged(bool)', self.enableOrDisableRegistrarButton)
        self.imagenFijaSelector.setMRMLScene(slicer.mrmlScene)
        self.registrarLayout.addRow("Imagen Fija:", self.imagenFijaSelector)
        self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.imagenFijaSelector, 'setMRMLScene(vtkMRMLScene*)')

        #selector de imgen movil
        self.imagenMovilSelector = slicer.qMRMLNodeComboBox()
        self.imagenMovilSelector.objectName = 'imagenMovilSelector'
        self.imagenMovilSelector.toolTip = u'Seleccione la imagen móvil'
        self.imagenMovilSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
        self.imagenMovilSelector.noneEnabled = True
        self.imagenMovilSelector.addEnabled = False  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
        self.imagenMovilSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
##        self.imagenMovilSelector.connect('currentNodeChanged(bool)', self.enableOrDisableRegistrarButton)
        self.imagenMovilSelector.setMRMLScene(slicer.mrmlScene)
        self.registrarLayout.addRow(u"Imagen Móvil:", self.imagenMovilSelector)
        self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.imagenMovilSelector, 'setMRMLScene(vtkMRMLScene*)')


        #selector de imgen Salida
        self.imagenSalidaSelector = slicer.qMRMLNodeComboBox()
        self.imagenSalidaSelector.objectName = 'imagenMovilSelector'
        self.imagenSalidaSelector.toolTip = u'Seleccione la imagen Salida'
        self.imagenSalidaSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
        self.imagenSalidaSelector.noneEnabled = True
        self.imagenSalidaSelector.addEnabled = True  # Se quita la posibilidad al usuario de crear un nuevo nodo con este widget
        self.imagenSalidaSelector.removeEnabled = False  # Se le quita al usuario la posibilidad de eliminar el nodo seleccionado en ese momento
##        self.imagenMovilSelector.connect('currentNodeChanged(bool)', self.enableOrDisableRegistrarButton)
        self.imagenSalidaSelector.setMRMLScene(slicer.mrmlScene)
        self.registrarLayout.addRow(u"Imagen Salida:", self.imagenSalidaSelector)
        self.parent.connect('mrmlSceneChanged(vtkMRMLScene*)', self.imagenSalidaSelector, 'setMRMLScene(vtkMRMLScene*)')

        #Boton ajustar
        self.ajustarButton = qt.QPushButton(u"Pre-ajustar imágenes")
        self.ajustarButton.toolTip = u"ajustar imágenes para facilitar el registro"
        self.registrarLayout.addWidget(self.ajustarButton)
        self.ajustarButton.connect('clicked(bool)', self.onAjustar)
        self.ajustarButton.enabled = True
        self.layout.addStretch(1)

        #Boton registrar
        self.registrarButton = qt.QPushButton(u"Registrar imágenes")
        self.registrarButton.toolTip = u"Centre una imagen y guarde la transformación de centrado y su inversa"
        self.registrarLayout.addWidget(self.registrarButton)
        self.registrarButton.connect('clicked(bool)', self.onRegistrar)
        self.registrarButton.enabled = True
        self.layout.addStretch(1)

        # Collapsible button
        #self.ajustarCollapsibleButton = ctk.ctkCollapsibleButton()
        #self.ajustarCollapsibleButton.text = u"Preajustar imágenes"
        #self.layout.addWidget(self.ajustarCollapsibleButton)

        self.ajustarDialog = qt.QDialog()
        #self.ajustarDialog.rejected.connect(self.onCancelarPreajuste)
        #self.ajustarDialog.accepted.connect(self.onAplicarPreajuste)

        # Layout within the collapsible button
        self.ajustarLayout = qt.QFormLayout(self.ajustarDialog)

        #sliders para de desplazamiento la posicion de la imagen movil
        self.transformTraslationSliders = slicer.qMRMLTransformSliders()
        self.transformTraslationSliders.toolTip = u"Desplace para trasladar la imagen móvil"
        self.transformTraslationSliders.Title = u'Traslación'
        self.transformTraslationSliders.TypeOfTransform = self.transformTraslationSliders.TRANSLATION
        self.ajustarLayout.addRow(self.transformTraslationSliders)

        #sliders para de desplazamiento la posicion de la imagen movil
        self.transformRotationSliders = slicer.qMRMLTransformSliders()
        self.transformRotationSliders.toolTip = u"Desplace para rotar la imagen móvil"
        self.transformRotationSliders.TypeOfTransform = self.transformRotationSliders.ROTATION
        self.transformRotationSliders.Title = u'Rotación'
        self.transformRotationSliders.LRLabel = 'Sagital'
        self.transformRotationSliders.PALabel = 'Coronal'
        self.transformRotationSliders.ISLabel = 'Axial'
        self.transformRotationSliders.minMaxVisible = False
        self.ajustarLayout.addRow(self.transformRotationSliders)

        self.cancelarButton = qt.QPushButton(u"Cancelar")
        self.cancelarButton.toolTip = u"Devuelve la imagen movil al estado inicial del preajuste"
        self.ajustarLayout.addWidget(self.cancelarButton)
        self.cancelarButton.connect('clicked(bool)', self.onCancelarPreajuste)
        self.cancelarButton.enabled = True

        self.capplyButton = qt.QPushButton(u"Aplicar")
        self.capplyButton.toolTip = u"Aplica el preajuste"
        self.ajustarLayout.addWidget(self.capplyButton)
        self.capplyButton.connect('clicked(bool)', self.onAplicarPreajuste)
        self.capplyButton.enabled = True

##    def enableOrDisableCentrarButton(self):
##        if self.imagenSelector.currentNode() is not None:
##            self.centrarButton.enabled = True

##    def enableOrDisableRegistrarButton(self):
##        if self.imagenFijaSelector.currentNode() is not None and self.imagenMovilSelector.currentNode() is not None and self.transformSelector.currentNode() is not None:
##            self.registrarButton.enabled = True
##            self.ajustarButton.enabled = True

    def SetBgFgVolumes(self, bg, fg):
        compositeNodes = slicer.util.getNodes('*CompositeNode*')
        appLogic = slicer.app.applicationLogic()
        selectionNode = appLogic.GetSelectionNode()
        selectionNode.SetReferenceActiveVolumeID(fg)
        selectionNode.SetReferenceSecondaryVolumeID(bg)
        appLogic.PropagateVolumeSelection()
        for co in compositeNodes.values():
            co.LinkedControlOn()
            co.SetForegroundOpacity(0.5)

    def onCentrar(self):
        volumenCentrar = self.imagenSelector.currentNode()
        lm = slicer.app.layoutManager()
        origenVolumen = volumenCentrar.GetOrigin()
        volumeLogic = slicer.vtkSlicerVolumesLogic()
        origenCentro = [0, 0, 0]
        volumeLogic.GetVolumeCenteredOrigin(volumenCentrar, origenCentro)
        traslacion = [0, 0, 0]
        volumenCentrar.SetOrigin(origenCentro)
        lm.resetSliceViews()
        for i in range(3):
            traslacion[i] = origenCentro[i] - origenVolumen[i]
        T = slicer.vtkMRMLTransformNode()
        I = slicer.vtkMRMLTransformNode()
        transmatrix = vtk.vtkMatrix4x4()
        transform = vtk.vtkTransform()
        T.SetAndObserveTransformToParent(transform)
        T.SetName('centrarTransformacionSeeg')
        I.SetName('CentrarTInversaSeeg')
        transmatrix.DeepCopy((1, 0, 0, traslacion[0], 0, 1, 0, traslacion[1], 0, 0, 1, traslacion[2], 0, 0, 0, 1))
        transform.SetMatrix(transmatrix)
        inv = transform.GetInverse()
        I.SetAndObserveTransformToParent(inv)
        slicer.mrmlScene.AddNode(T)
        slicer.mrmlScene.AddNode(I)

    def onAjustar(self):
        self.transformTraslationSliders.setMRMLTransformNode(self.transformSelector.currentNode())
        self.transformRotationSliders.setMRMLTransformNode(self.transformSelector.currentNode())
        imagenMovil = self.imagenMovilSelector.currentNode()
        imagenFija = self.imagenFijaSelector.currentNode()
        self.SetBgFgVolumes(imagenFija.GetID(), imagenMovil.GetID())
        transformada = self.transformSelector.currentNode()
        imagenMovil.SetAndObserveTransformNodeID(transformada.GetID())
        self.ajustarDialog.show()

    def onRegistrar(self):
        transformada = self.transformSelector.currentNode()
        imagenFija = self.imagenFijaSelector.currentNode()
        imagenMovil = self.imagenMovilSelector.currentNode()
        parameters = {}
        parameters['fixedVolume'] = imagenFija.GetID()
        parameters['movingVolume'] = imagenMovil.GetID()
        parameters['linearTransform'] = transformada.GetID()
        parameters['initialTransform'] = transformada.GetID()
        parameters['useRigid'] = True
        parameters['useAffine'] = True
        print(parameters)
        cliNode = slicer.cli.run(slicer.modules.brainsfit, None, parameters, wait_for_completion=True)
        print((cliNode))

    def onCancelarPreajuste(self):
        transformada = self.transformSelector.currentNode()
        matrizTransformada = transformada.GetMatrixTransformFromParent()
        matrizTransformada.Identity()
        transformada.SetMatrixTransformFromParent(matrizTransformada)

    def onAplicarPreajuste(self):
        self.ajustarDialog.close()
