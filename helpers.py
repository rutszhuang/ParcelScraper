# To run: ./use_qgis.sh "-LTR"

import os
os.environ["PROJ_LIB"]="/Applications/QGIS-LTR.app/Contents/Resources/proj"
import glob
import os
import sys
from qgis.core import *
from qgis.gui import QgisInterface,QgsMapCanvas
from PyQt5.QtCore import QFileInfo, QSize, Qt, QRectF
from PyQt5.QtSql import *
from PyQt5.QtGui import * 


def addAttributeLabels(layer, attribute):
    #https://gis.stackexchange.com/questions/384601/enabling-show-all-labels-for-this-layer-including-colliding-labels-in-pyqgis
    layer_settings = QgsPalLayerSettings()
    text_format = QgsTextFormat()
    buffer_settings = QgsTextBufferSettings()
    shadow_settings = QgsTextShadowSettings()

    text_format.setFont(QFont("Arial", 2))
    text_format.setSize(2)
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


# TODO: Pass array or dictionary in with different ranges
#       Use those to create graduations
def applyGraduatedSymbology(layer, target_field):
    myRangeList = []                                
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#ffcccc"))
    symbol.setColor(QColor("yellow"))
    myRange = QgsRendererRange(1, 99, symbol, '1 - 99')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#ff9999"))
    symbol.setColor(QColor("orange"))
    myRange = QgsRendererRange(100, 199, symbol, '100 - 199')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#ff6666"))
    symbol.setColor(QColor("red"))
    myRange = QgsRendererRange(200, 299, symbol, '200 - 299')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("#ff3333"))
    symbol.setColor(QColor("blue"))
    myRange = QgsRendererRange(300, 399, symbol, '300 - 399')
    myRangeList.append(myRange)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor("black"))
    myRange = QgsRendererRange(400, 499, symbol, '400 - 499')
    myRangeList.append(myRange)

    myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
    myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)               

    layer.setRenderer(myRenderer)
    layer.triggerRepaint()           

def printMap(project, layers, png_path):
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName("MyLayout")
    project.layoutManager().addLayout(layout)

    map = QgsLayoutItemMap(layout)
    map.setRect(20, 20, 20, 20)

    # set the map extent
    ms = QgsMapSettings()
    ms.setLayers(layers)  # set layers to be mapped
    rect = QgsRectangle(ms.fullExtent())
    rect.scale(1.0)
    ms.setExtent(rect)
    map.setExtent(rect)

    map.setBackgroundColor(QColor(255, 255, 255, 0))

    layout.addLayoutItem(map)

    map.attemptMove(QgsLayoutPoint(50, 20, QgsUnitTypes.LayoutMillimeters))
    map.attemptResize(QgsLayoutSize(180, 180, QgsUnitTypes.LayoutMillimeters))

    title = QgsLayoutItemLabel(layout)
    title.setText("Taipei City - Swaps by Section")
    title.setFont(QFont('Arial', 24))
    title.adjustSizeToText()
    layout.addLayoutItem(title)
    title.attemptMove(QgsLayoutPoint(80, 5, QgsUnitTypes.LayoutMillimeters))

    
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle("LEGEND")
    layerTree = QgsLayerTree()
    # add layers that you want to see in legend
    layerTree.addLayer(layers[0])
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)

    map.zoomToExtent(layers[0].extent())

    # layout.addLayoutItem(map)
    exporter = QgsLayoutExporter(layout)
    # settings = exporter.ImageExportSettings()
    exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
    # exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

