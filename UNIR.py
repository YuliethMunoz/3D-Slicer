for fileName in fileNames:
#f es un scalar volume de cada corte
      (s,f) = self.readFrame(fileName)
      if s:
        if not frame0:
          frame0 = f
          frame0Image = frame0.GetImageData()
          frame0Extent = frame0Image.GetExtent()
          print("Numero de volumenes XXXXX: " + str(frame0Extent));
        else:
          frameImage = f.GetImageData()
          frameExtent = frameImage.GetExtent()
          if frameExtent[1]!=frame0Extent[1] or frameExtent[3]!=frame0Extent[3] or frameExtent[5]!=frame0Extent[5]:
            continue
        frames.append(f)

  

    nFrames = len(frames)
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

    volumeLabels.SetNumberOfTuples(nFrames)
    volumeLabels.SetNumberOfComponents(1)
    volumeLabels.Allocate(nFrames)
    for i in range(nFrames):
      frameId = frameIdMultiplier*(self.__veInitial.value+self.__veStep.value*i)
      volumeLabels.SetComponent(i, 0, frameId)
      frameLabelsAttr += str(frameId)+','
    frameLabelsAttr = frameLabelsAttr[:-1]

    # allocate multivolume
    mvImage = vtk.vtkImageData()
    mvImage.SetExtent(frame0Extent)
    if vtk.VTK_MAJOR_VERSION <= 5:
      mvImage.SetNumberOfScalarComponents(nFrames)
      mvImage.SetScalarType(frame0.GetImageData().GetScalarType())
      mvImage.AllocateScalars()
    else:
      mvImage.AllocateScalars(frame0.GetImageData().GetScalarType(), nFrames)

    extent = frame0.GetImageData().GetExtent()
    numPixels = float(extent[1]+1)*(extent[3]+1)*(extent[5]+1)*nFrames
    scalarType = frame0.GetImageData().GetScalarType()
    print('Will now try to allocate memory for '+str(numPixels)+' pixels of VTK scalar type'+str(scalarType))
    print('Memory allocated successfully')
    mvImageArray = vtk.util.numpy_support.vtk_to_numpy(mvImage.GetPointData().GetScalars())

    print("Que es escalar: " + str(mvImage.GetPointData().GetScalars()));
    print("ID mvImagearray " + str(id(mvImageArray)));
    print("ID 2: " + str(mvImage.GetPointData().GetScalars()));
    print("Que es frame0: " + str(frame0));
    

    mat = vtk.vtkMatrix4x4()
    frame0.GetRASToIJKMatrix(mat)
    mvNode.SetRASToIJKMatrix(mat)
    frame0.GetIJKToRASMatrix(mat)
    mvNode.SetIJKToRASMatrix(mat)

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
