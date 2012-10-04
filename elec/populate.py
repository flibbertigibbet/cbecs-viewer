"""

>>> import sqlite3
>>> conn = sqlite3.connect('bander')
>>> c = conn.cursor()
>>> res = c.execute("select * from elec_building"
... )
>>> res.fetchall()
[]
>>> c.execute("insert into elec_building values (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1) ")
<sqlite3.Cursor object at 0x10657b650>
>>> res = c.execute("select * from elec_building")
>>> l = res.fetchall()
>>> l
[(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)]

insert into elec_building (pubid,activity,region,area,area_cat,yrcon,heat,cooling,ventilat,waterheat,lighting,cooking,refrig,office,computer,misc) values (3,3,3,3,4,4,4,4,3,3,3,3,4,4,5,4)

"""

template = "insert into elec_building (pubid,activity,region,area,area_cat,yrcon,heat,cooling,ventilat,waterheat,lighting,cooking,refrig,office,computer,misc) values (%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"

datafnam = "/Users/tobis/CBECS/FILE18.csv"
dataf = file(datafnam)

data = dataf.readlines()

indices = data[0].strip().split(",")
indices = [item.strip() for item in indices]

indexnames = "PUBID8 PBA8 REGION8 SQFT8 SQFTC8 YRCONC8 ELHTBTU8 ELCLBTU8 ELVNBTU8 ELWTBTU8 ELLTBTU8 ELCKBTU8 ELRFBTU8 ELOFBTU8 ELPCBTU8 ELMSBTU8".split()

indexlist = [indices.index(indexname) for indexname in indexnames]

import sqlite3
conn = sqlite3.connect('../bander')
c = conn.cursor()

for line in data[1:]:
    if not line.isspace():
        values = line.split(",")
    tuplify = "("
    for index in indexlist:
        tuplify += " values[%d]," % index
    tuplify += ")"
    try:
        interptuple = tuple(map(int,eval(tuplify)))
    except ValueError:
        continue
    cmd = template % interptuple
    print cmd
    c.execute(cmd)
    


