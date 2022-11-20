# To run: ./use_qgis.sh "-LTR"


import os
os.environ["PROJ_LIB"]="/Applications/QGIS-LTR.app/Contents/Resources/proj"



from qgis.core import *


import glob
import os
import sys
from qgis.core import (QgsProject, QgsRasterLayer,QgsVectorLayer,QgsApplication,QgsCoordinateReferenceSystem)
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


# layer=iface.addVectorLayer("/Users/erin/Documents/github/Project_volumntransfer/sectname/sectname97-面-addcount.shp","sectname97","ogr")


# From https://gis.stackexchange.com/questions/347407/using-iface-in-standalone-pyqgis-script

# start a project
project = QgsProject.instance()

selectedcrs="EPSG:4326"
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromUserInput(selectedcrs)
project.setCrs(target_crs)

canvas=QgsMapCanvas()
iface=QgisInterface.QgsMapCanvas()
project_path = strProjectName
###############################

db = QSqlDatabase.addDatabase('QPSQL')
# check to see if it is valid
if db.isValid():
    print ("QPSQL db is valid")
    # set the parameters needed for the connection
    db.setHostName('localhost')
    db.setDatabaseName('request')
    db.setPort(int(5433))
    db.setUserName('postgres')
    db.setPassword('postgres')
    uri = QgsDataSourceUri()
    uri.setConnection("localhost", "5433", "request", "postgres", "postgres")
    #open (create) the connection
    if db.open():
        print ("Opened %s" % uri.uri())
        uri.setDataSource ("rodno_razvrstani_podaci", 'statistika_2017', 'wkb_geometry')
        vlayer=QgsVectorLayer (uri .uri(False), 'statistika_2017', "postgres")
        project.addMapLayer(vlayer)

    else:
            err = db.lastError()
            print (err.driverText())
db.close()

#This is where script breaks
qgis.utils.iface.setActiveLayer(vlayer)
#iface.zoomToActiveLayer()

###############################

# write the project file
project.write(project_path)



# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
