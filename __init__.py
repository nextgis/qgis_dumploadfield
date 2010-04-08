# -*- coding: utf-8 -*-
mVersion = "0.0.5"
def name():
  return "DumpLoadField"
def description():
  return "Dumps or loads text from/to a selected field from/to a textfile"
def qgisMinimumVersion(): 
  return "1.0" 
def version():
  return mVersion
def authorName():
  return "Maxim Dubinin, sim@gis-lab.info"
def classFactory(iface):
  from dumpfield import dumpfield
  return dumpfield(iface)