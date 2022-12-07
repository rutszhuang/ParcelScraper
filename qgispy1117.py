# TODO: Rename to VisualizeSectionCounts.py

# To run: ./use_qgis.sh "-LTR"

import os
os.environ["PROJ_LIB"]="/Applications/QGIS-LTR.app/Contents/Resources/proj"
from definitions import ROOT_DIR
from qgis.core import *
from qgis.gui import QgisInterface,QgsMapCanvas
from PyQt5.QtGui import *
from PyQt5.QtCore import QFileInfo
from PyQt5.QtSql import *

from helpers import *



# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

# Start a project
project = QgsProject.instance()

# Initialize project
selectedcrs="EPSG:4326"
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromUserInput(selectedcrs)
project.setCrs(target_crs)

vec_path= os.path.join(ROOT_DIR, 'sectname/sectname97-面.shp')
png_path = os.path.join(ROOT_DIR, "output.png")
 
##############################################################
# Load Layers
##############################################################

# Load base layer
baseveclayer = QgsVectorLayer(vec_path, "baselayer", "ogr")
if not baseveclayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(baseveclayer)
# Make baselayer transparent
baseveclayer.renderer().symbol().setColor(QColor(0,0,0,0))

# Load vector layer
veclayer = QgsVectorLayer(vec_path, "section", "ogr")
if not veclayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(veclayer)
veclayer.setProviderEncoding("big5")
veclayer.dataProvider().setEncoding("big5")

##############################################################
# Add attribute labels 
##############################################################
addAttributeLabels(veclayer, "小段代碼")

print("SHP")
for field in veclayer.fields():
    print(field.name(), field.typeName())

# Load CSV into project
csv_uri = os.path.join(ROOT_DIR, 'section_counts.csv')
csvLayer = QgsVectorLayer(csv_uri, "section_counts", "ogr")
QgsProject.instance().addMapLayer(csvLayer)

print("CSV")
for field in csvLayer.fields():
    print(field.name(), field.typeName())

##############################################################
# Join csv section counts to vector layer
##############################################################
shpField='小段代碼'
csvField='Section'
joinObject = QgsVectorLayerJoinInfo()
joinObject.setJoinFieldName(csvField)
joinObject.setTargetFieldName(shpField)
joinObject.setJoinLayerId(csvLayer.id())
joinObject.setUsingMemoryCache(True)
joinObject.setJoinLayer(csvLayer)
veclayer.addJoin(joinObject)

##############################################################
# Color areas of the map based on results of the join
# The higher the count in the section, the darker the section will be.
##############################################################
applyGraduatedSymbology(veclayer, 'section_counts_Count')

print("SHPxCSV")
for field in veclayer.fields():
    print(field.name(), field.typeName())

##############################################################
# Save Project
##############################################################
proj_path = os.path.join(ROOT_DIR, "my_project.qgs")
print(proj_path)
project.write(proj_path)

##############################################################
# Save layers to png file
##############################################################
layers = [veclayer]
printMap(project, layers, png_path)

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()


