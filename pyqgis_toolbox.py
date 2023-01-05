# To run: ./use_qgis.sh "-LTR"

# theProject.SaveProject()
# theProject.SaveProject("dir", "projectname")

# research getters and setters in python
# theProject.SetDir("xxx")
# theProject.SetName("yyy")
# theProject.SaveProject()

# On the first day at your new job....
# Where is the coding standards document?
# Where is the naming conventions document?


import os
from definitions import *
from qgis.core import *
from qgis.core import QgsProject,QgsVectorLayer,QgsVectorLayerJoinInfo, QgsApplication,QgsCoordinateReferenceSystem
from qgis.gui import QgisInterface,QgsMapCanvas
from PyQt5.QtCore import QFileInfo, QSize, Qt, QRectF
from PyQt5.QtSql import *
from PyQt5.QtGui import * 


def AddVec(path, name, provider = "ogr"):
    layer = QgsVectorLayer(path, name, provider)
    if not layer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(layer)
        return layer

def applyGraduatedSymbology(layer, target_field):
    myRangeList = []                                
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#FFECE5"))
    myRange = QgsRendererRange(1, 25, symbol, '1 - 25')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#FAB698"))
    myRange = QgsRendererRange(26, 50, symbol, '26 - 50')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#BA603A"))
    myRange = QgsRendererRange(51, 100, symbol, '51 - 100')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#947D74"))
    myRange = QgsRendererRange(101, 300, symbol, '101 - 300')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#5D473E"))
    myRange = QgsRendererRange(301, 500, symbol, '301 - 500')
    myRangeList.append(myRange)

    myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
    myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)               

    layer.setRenderer(myRenderer)
    layer.triggerRepaint()           


def addAttributeLabels(layer, attribute):
    #https://gis.stackexchange.com/questions/384601/enabling-show-all-labels-for-this-layer-including-colliding-labels-in-pyqgis
    layer_settings = QgsPalLayerSettings()
    text_format = QgsTextFormat()
    buffer_settings = QgsTextBufferSettings()
    shadow_settings = QgsTextShadowSettings()

    text_format.setFont(QFont("Arial", 12))
    text_format.setSize(12)
    text_format.setColor(QColor("black"))

    buffer_settings.setEnabled(True)
    buffer_settings.setSize(0.3)
    buffer_settings.setColor(QColor("#fafafa"))

    shadow_settings.setEnabled(False)
    shadow_settings.setOffsetAngle(135)
    shadow_settings.setOffsetDistance(1)
    # shadow_settings.setBlurRadius(1.5)

    text_format.setBuffer(buffer_settings)
    text_format.setShadow(shadow_settings)
    layer_settings.setFormat(text_format)

    layer_settings.fieldName =  attribute #"小段代碼"
    layer_settings.placement = 1
    # layer_settings.quadOffset = 7

    layer_settings.enabled = True
    layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    layer.setLabelsEnabled(True)
    layer.setLabeling(layer_settings)

    # refresh the layer on the map canvas
    layer.triggerRepaint()