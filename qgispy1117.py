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

# Write your code here to load some layers, use processing
# algorithms, etc.


# From https://gis.stackexchange.com/questions/347407/using-iface-in-standalone-pyqgis-script

# start a project
project = QgsProject.instance()

selectedcrs="EPSG:4326"
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromUserInput(selectedcrs)
project.setCrs(target_crs)
project_path = strProjectName
vec_path= "/Users/erin/Documents/github/Project_volumntransfer/sectname/sectname97-面-addcount.shp"
###############################

# The format is:
# vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

veclayer = QgsVectorLayer(vec_path, "section", "tpc")
if not veclayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(veclayer)

for field in veclayer.fields():
    print(field.name(), field.typeName())

print(veclayer.displayField())


#This is where script breaks
# qgis.utils.iface.setActiveLayer(veclayer)
#iface.zoomToActiveLayer()

###############################

# write the project file
project.write(project_path)



# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
