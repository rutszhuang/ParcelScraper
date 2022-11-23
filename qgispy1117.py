# To run: ./use_qgis.sh "-LTR"

import os
os.environ["PROJ_LIB"]="/Applications/QGIS-LTR.app/Contents/Resources/proj"

from qgis.core import *

import glob
import os
import sys
from qgis.core import (QgsProject,QgsVectorLayer,QgsApplication,QgsCoordinateReferenceSystem)
from qgis.gui import QgisInterface,QgsMapCanvas
from PyQt5.QtCore import QFileInfo
from PyQt5.QtSql import *
from qgis.core import QgsDataSourceUri
import qgis.utils
strProjectName = "my_project.qgs"

# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

# start a project
project = QgsProject.instance()
selectedcrs="EPSG:4326"
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromUserInput(selectedcrs)
project.setCrs(target_crs)
project_path = strProjectName
vec_path= "/Users/erin/Documents/github/Project_volumntransfer/sectname/sectname97-面.shp"
###############################

# The format is:
# vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

def AddVec(path, name, provider = "ogr"):
    layer = QgsVectorLayer(path, name, provider)
    if not layer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(layer)
        return layer
section = AddVec(vec_path, "section")
section.setProviderEncoding('big5')
section.dataProvider().setEncoding('big5')
for field in section.fields():
    print(field.name(), field.typeName())


# print(layer.displayField())



# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
