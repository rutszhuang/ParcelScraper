# for Qgis 3.10 LTR pass "3.10" as $1
# Qgis PR version is stored under QGIS.app on macOS
QGIS_VERSION=$1

# store PATH and PYTHONPATH 
OLD_PATH=$PATH
OLD_PYTHONPATH=$PYTHONPATH

# set env variables:
export PATH=/Applications/QGIS$QGIS_VERSION.app/Contents/MacOS/bin:$PATH
export PYTHONPATH=/Applications/QGIS$QGIS_VERSION.app/Contents/Resources/python
export QT_QPA_PLATFORM_PLUGIN_PATH=/Applications/QGIS$QGIS_VERSION.app/Contents/PlugIns/platforms/
export DYLD_INSERT_LIBRARIES=/Applications/QGIS$QGIS_VERSION.app/Contents/MacOS/lib/libsqlite3.dylib

# export DYLD_INSERT_LIBRARIES=/Applications/QGIS-LTR.app/Contents/MacOS/lib/libsqlite3.dylib

# check correct python bin is used
echo "Using python3 from $(which python3)"

# Run code
# python3 "./volumntransferscraper.py"
python3 "./qgispy1117.py"

# restore and clean up
export PATH=$OLD_PATH
export PYTHONPATH=$OLD_PYTHONPATH
unset QT_QPA_PLATFORM_PLUGIN_PATH
unset DYLD_INSERT_LIBRARIES