# To run: ./documents/github/Project_volumntransfer/use_qgis.sh "-LTR"

import os
from pyqgis_toolbox import *
from definitions import *
from ScraperProcessClass import *
from Statistics import *


os.environ["PROJ_LIB"]="/Applications/QGIS-LTR.app/Contents/Resources/proj"
from qgis.core import *
from qgis.gui import QgisInterface,QgsMapCanvas
from PyQt5.QtGui import *
from PyQt5.QtCore import QFileInfo
from PyQt5.QtSql import *
import qgis.utils
from qgis.core import QgsProject,QgsVectorLayerJoinInfo,QgsVectorLayer,QgsApplication,QgsCoordinateReferenceSystem, QgsVectorFileWriter


# start = time.time()
# print(start)
urlslug = "https://www.udd.gov.taipei/volumn-transfer/avdwckf?page="
scraper = ScraperProcessClass(urlslug, 25)
scraper.scrape()
scraper.process()
stat = SectionStatistics()
stat.statistics()



strProjectName = "my_project.qgs"

# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app", True)

# Create a reference to the QgsApplication.  Setting the second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

# start a project
selectedcrs = "EPSG:4326"
project = QgsProject.instance()
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromUserInput(selectedcrs)
project.setCrs(target_crs)

#load layers
print("-- load vector layer --")
vec_path = os.path.join(ROOT_DIR, "sectname/sectname97-面.shp")
baseMap = QgsVectorLayer(vec_path, "section")
if not baseMap.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(baseMap)

baseMap.setProviderEncoding('big5')
baseMap.dataProvider().setEncoding('big5')

for field in baseMap.fields():
    print(field.name(), field.typeName())
baseMap_style = QgsFillSymbol.createSimple({"color_border":"#281E1A", "width_border":"0.2", "style":"no"})
baseMap.renderer().setSymbol(baseMap_style)

# load csv layer
print("-- load csv layer --")
csvPath = os.path.join(ROOT_DIR, "statistics.csv")
csvLayer = AddVec(csvPath, "csvLayer")
for field in csvLayer.fields():
    print(field.name(), field.typeName())

# export count map
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = ROOT_DIR
options.fileEncoding = "utf-8"
QgsVectorFileWriter.writeAsVectorFormatV3(baseMap, "countmap", project.transformContext(), QgsVectorFileWriter.SaveVectorOptions())
countmap_path = os.path.join(ROOT_DIR, "countmap.gpkg")
countMap = AddVec(countmap_path, "countmap")

# table join
print("-- SHPxCSV --")
shpField='小段代碼'
csvField='section_code'
joinObject = QgsVectorLayerJoinInfo()
joinObject.setJoinFieldName(csvField)
joinObject.setTargetFieldName(shpField)
joinObject.setJoinLayerId(csvLayer.id())
joinObject.setUsingMemoryCache(True)
joinObject.setJoinLayer(csvLayer)
countMap.addJoin(joinObject)
for field in countMap.fields():
    print(field.name(), field.typeName())

#apply graduated symbology to each class
applyGraduatedSymbology(countMap, "csvLayer_count")


# load district layer
districtMapPath = os.path.join(ROOT_DIR, "district/G97_A_CADIST_P.shp")
districtMap = QgsVectorLayer(districtMapPath, "district")
if not districtMap.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(districtMap)
districtMap_style = QgsFillSymbol.createSimple({"color_border":"#2A0503", "width_border":"0.7", "style":"no"})
districtMap.renderer().setSymbol((districtMap_style))

addAttributeLabels(districtMap, "TNAME")

# save project
proj_path = os.path.join(ROOT_DIR, strProjectName)
project.write(proj_path)


# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
