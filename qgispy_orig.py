
# original 
import os
os.environ["PROJ_LIB"]="/Applications/QGIS-LTR.app/Contents/Resources/proj"



from qgis.core import *

# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

# Write your code here to load some layers, use processing
# algorithms, etc.


layer=iface.addVectorLayer("F:\public_streets.shp","street","ogr")

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
