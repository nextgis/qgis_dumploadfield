# -*- coding: utf-8 -*-

#******************************************************************************
#
# DumpLoadField
# ---------------------------------------------------------
# Dump or load text from/to a selected field from/to a textfile
#
# Copyright (C) 2008-2014 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources_rc
from dumpfield_dlgselfield import dlgSelField

class dumpfield:

  def __init__(self, iface):
    """Initialize the class"""
    self.iface = iface

  def initGui(self):
    self.actionToFile = QAction(QIcon(":/plugins/dumpfield/icon.png"), "Dump field", self.iface.mainWindow())
    self.actionToFile.setStatusTip("Dump a field to a textfile")
    QObject.connect(self.actionToFile, SIGNAL("triggered()"), self.dumpfield)

    self.actionFromFile = QAction(QIcon(":/plugins/dumpfield/icon.png"), "Load to a field", self.iface.mainWindow())
    self.actionFromFile.setStatusTip("Load text to a field from the textfile")
    QObject.connect(self.actionFromFile, SIGNAL("triggered()"), self.loadtofield)

    if hasattr( self.iface, "addPluginToVectorMenu" ):
      self.iface.addPluginToVectorMenu("&Dump and load field", self.actionFromFile)
      self.iface.addPluginToVectorMenu("&Dump and load field", self.actionToFile)
    else:
      self.iface.addPluginToMenu("&Dump and load field", self.actionFromFile)
      self.iface.addPluginToMenu("&Dump and load field", self.actionToFile)

  def unload(self):
    if hasattr( self.iface, "addPluginToVectorMenu" ):
      self.iface.removePluginVectorMenu("&Dump and load field",self.actionToFile)
      self.iface.removePluginVectorMenu("&Dump and load field",self.actionFromFile)
    else:
      self.iface.removePluginMenu("&Dump and load field",self.actionToFile)
      self.iface.removePluginMenu("&Dump and load field",self.actionFromFile)

  def dumpfield(self):
    curLayer = self.iface.mapCanvas().currentLayer()
    if (curLayer == None):
      infoString = "No layers selected"
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    if (curLayer.type() != curLayer.VectorLayer):
      infoString = "Not a vector layer"
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    featids=curLayer.selectedFeaturesIds()
    if (len(featids) == 0):
      infoString = "No features selected, using all " + str(curLayer.featureCount()) + " features"
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      featids = range(curLayer.featureCount())
    fProvider = curLayer.dataProvider()
    myFields = fProvider.fields()
    allFieldsNames= [f.name() for f in myFields]
    myFieldsNames=[]
    for f in myFields:
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
    fileHandle = open(adumpfile, 'w')
    
    for f in curLayer.getFeatures():
       attr=f[attrfield]
       fileHandle.write(attr.encode('utf-8') +'\n')
    fileHandle.close()

  def loadtofield(self):
    layersmap=QgsMapLayerRegistry.instance().mapLayers()
    layerslist=[]
    curLayer = self.iface.mapCanvas().currentLayer()
    if (curLayer == None):
      infoString = "No layers selected"
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    if (curLayer.type() != curLayer.VectorLayer):
      infoString = "Not a vector layer"
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    fProvider = curLayer.dataProvider()
    myFields = fProvider.fields()
    allFieldsNames= [f.name() for f in myFields]
    myFieldsNames=[]
    for f in myFields:
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

    curLayer.startEditing()
    for f in curLayer.getFeatures():
       astr = unicode(fileHandle.next(),'utf-8')
       f[attrfieldname] = astr.strip()
       curLayer.updateFeature(f)

       #bbul = curLayer.commitChanges()
       #QMessageBox.information(self.iface.mainWindow(),"Warning",str(fid))
       #QMessageBox.information(self.iface.mainWindow(),"Warning",str(bbul))
    curLayer.commitChanges()
    fileHandle.close()
