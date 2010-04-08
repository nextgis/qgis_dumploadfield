# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources
from dumpfield_dlgselfield import dlgSelField

class dumpfield:

  def __init__(self, iface):
    """Initialize the class"""
    self.iface = iface
  
  def initGui(self):
    self.action = QAction(QIcon(":/plugins/dumpfield/icon.png"), "Dump field", self.iface.mainWindow())
    self.action.setStatusTip("Dumps a field to a textfile")
    QObject.connect(self.action, SIGNAL("triggered()"), self.dumpfield)
    self.iface.addPluginToMenu("&Dump and load field", self.action)
    self.action = QAction(QIcon(":/plugins/dumpfield/icon.png"), "Load to a field", self.iface.mainWindow())
    self.action.setStatusTip("Loads text to a field from the textfile")
    QObject.connect(self.action, SIGNAL("triggered()"), self.loadtofield)
    self.iface.addPluginToMenu("&Dump and load field", self.action)
  def unload(self):
    self.iface.removePluginMenu("&Dump and load field",self.action)

  def dumpfield(self):
    layersmap=QgsMapLayerRegistry.instance().mapLayers()
    layerslist=[]
    curLayer = self.iface.mapCanvas().currentLayer()
    if (curLayer == None):
      infoString = QString("No layers selected")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    if (curLayer.type() <> curLayer.VectorLayer):
      infoString = QString("Not a vector layer")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    featids=curLayer.selectedFeaturesIds()
    if (len(featids) == 0):
      infoString = QString("No features selected, using all " + str(curLayer.featureCount()) + " features")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      featids = range(curLayer.featureCount())
    fProvider = curLayer.dataProvider()
    myFields = fProvider.fields()
    allFieldsNames= [f.name() for f in myFields.values()]
    myFieldsNames=[]
    for f in myFields.values():
       if f.typeName() == "String":
          myFieldsNames.append(f.name())
    if len(myFieldsNames) == 0:
       QMessageBox.information(self.iface.mainWindow(),"Warning","No string field names. Exiting")
       return
    elif len(myFieldsNames) == 1:
       attrfield = myFieldsNames[0]
    else:
      res = dlgSelField(myFieldsNames)
      if res.exec_():
        attrfield=res.selectedAttr()
      else:
        return
    attrindex = allFieldsNames.index(attrfield)
    adumpfile = QFileDialog.getSaveFileName(None, "save file dialog", attrfield +'.txt', "Text (*.txt)")
    fileHandle = open (adumpfile, 'w')
    for fid in featids: 
       features={}
       result={}
       features[fid]=QgsFeature()
       curLayer.featureAtId(fid,features[fid])
       attrmap=features[fid].attributeMap()
       attr=attrmap.values()[attrindex]
       fileHandle.write(attr.toString()+"\n")
    fileHandle.close()

  def loadtofield(self):
    layersmap=QgsMapLayerRegistry.instance().mapLayers()
    layerslist=[]
    curLayer = self.iface.mapCanvas().currentLayer()
    if (curLayer == None):
      infoString = QString("No layers selected")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    if (curLayer.type() <> curLayer.VectorLayer):
      infoString = QString("Not a vector layer")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    featids = range(curLayer.featureCount())
    fProvider = curLayer.dataProvider()
    myFields = fProvider.fields()
    allFieldsNames= [f.name() for f in myFields.values()]
    myFieldsNames=[]
    for f in myFields.values():
       if f.typeName() == "String":
          myFieldsNames.append(f.name())
    if len(myFieldsNames) == 0:
       QMessageBox.information(self.iface.mainWindow(),"Warning","No string field names. Exiting")
       return
    elif len(myFieldsNames) == 1:
       attrfieldname = myFieldsNames[0]
    else:
      res = dlgSelField(myFieldsNames)
      if res.exec_():
        attrfieldname=res.selectedAttr()
      else:
        return
    attrindex = allFieldsNames.index(attrfieldname)
    attrfield = myFields[attrindex]
    aloadfile = QFileDialog.getOpenFileName(None, "Open file dialog","","Text (*.txt)")
    fileHandle = open(aloadfile, 'r')
    #QMessageBox.information(self.iface.mainWindow(),"Warning",str(curLayer.isEditable()))
    for fid in [0,2]: 
       features={}
       result={}
       features[fid]=QgsFeature()
       curLayer.featureAtId(fid,features[fid])
       astr = unicode(fileHandle.next(),'windows-1251')
       #astr2 = astr.strip().encode('utf-8')
       features[fid].changeAttribute(attrindex,QVariant(astr.strip()))
       tmp = {}
       tmp[fid] = features[fid].attributeMap()
       fProvider.changeAttributeValues(tmp)

       #bbul = curLayer.commitChanges()
       #QMessageBox.information(self.iface.mainWindow(),"Warning",str(fid))	   
       #QMessageBox.information(self.iface.mainWindow(),"Warning",str(bbul))	   
    fileHandle.close()