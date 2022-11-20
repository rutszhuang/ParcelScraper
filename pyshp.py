import shapefile

r = shapefile.Reader("/Users/erin/Documents/github/Project_volumntransfer/sectname/sectname97-面.shp", encoding="Big5")
fields=r.fields
# print(fields)
records = r.records()
# print(records)
outFile = "/Users/erin/Documents/github/Project_volumntransfer/sectname/sectname97-面-addcount.shp"
w = shapefile.Writer(outFile, encoding="utf-8")

w.fields = list(r.fields)

# Add our new field using the pyshp API
w.field("count", "N", 10,0)
print(w.fields)



i=1 
# TODO: replace i with count
for shaperec in r.iterShapeRecords():    
    w.record(shaperec.record[0], shaperec.record[1], shaperec.record[2], i )    
    w.shape(shaperec.shape)
    i+=1

 
