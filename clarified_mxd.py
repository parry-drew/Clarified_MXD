#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# mxd_clarify.py
# This script will create and populate a file gdb with all the unique data sources
# used in an mxd.
#
# C:\Python27\ArcGIS10.4\python.exe clarified_mxd.py
#
# ---------------------------------------------------------------------------
import os, datetime, timeit, shutil, zipfile, arcpy

root = os.path.abspath(os.path.curdir)

def main():
    #raw_mxd = raw_input('    1. What is the full directory of the mxd you want to clarify? --> ')
    raw_gdb = raw_input('    2. What do you want to to call the gdb? --> ')
    start = timeit.default_timer()
    print("\n    PROCESSING")
    arcpy.CreateFileGDB_management(root, raw_gdb)
    mxd = arcpy.mapping.MapDocument(raw_mxd)
    raw_sources = []
    # Creates a list of data sources
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("DATASOURCE"):
            raw_sources.append(lyr.dataSource)
    # Remove duplicate list values
    sources = list(set(raw_sources))
    # Populates the gdb.
    arcpy.FeatureClassToGeodatabase_conversion(sources , root + "\\" + raw_gdb + ".gdb")
    # Zip gdb
    outFile = raw_gdb + '.zip'
    gdbName = os.path.basename(raw_gdb)
    with zipfile.ZipFile(outFile,mode='w',compression=zipfile.ZIP_DEFLATED,allowZip64=True) as myzip:
        for f in os.listdir(raw_gdb + ".gdb"):
            myzip.write(os.path.join(raw_gdb + ".gdb",f),gdbName+'\\'+os.path.basename(f))

    stop = timeit.default_timer()
    print("\n    COMPLETED! Total Run Time: " +  str(stop - start) + " seconds")

if __name__ == '__main__':
    main()
