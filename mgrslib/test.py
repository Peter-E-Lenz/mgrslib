from mgrslib import Heading,Grid
from pprint import pprint
import math

#Heading class

#_compass=[Heading(i['name'],i['abbr'],i['azimuth'],i['order']) for i in _compass]


hd1 = Heading('Test Heading 1','TDH1',0,1)
hd2 = Heading('Test Heading 2','TDH2',50,2)
hd3 = Heading('Test Heading 1','TDH3',100,1)

#assert hd1<hd3
#assert hd1>hd2


#Grid class

g = Grid('4QGH94933312')

assert g.gzd == '4Q'
assert g.gridSquare == 'GH'
assert g.easting == 9493
assert g.northing == 3312

assert g.lat == 20.17289585706837
assert g.lon == -156.1783234582578

assert g.size == 10
assert g.precision == 4

assert g.mgrs1 == Grid('4QGH9493033120')
assert g.mgrs10 == Grid('4QGH94933312')
assert g.mgrs100 == Grid('4QGH949331')
assert g.mgrs1k == Grid('4QGH9433')
assert g.mgrs10k == Grid('4QGH93')
assert g.mgrs100k == Grid('4QGH')
assert g.mgrs100k != Grid('4QGK')

assert g.north == Grid('4QGH94933313')
assert g.east == Grid('4QGH 9492 3312')
assert g.south == Grid('4QGH94933311')
assert g.west == Grid('4QGH 9494 3312')

assert g == Grid(20.17289585706837,-156.1783234582578).mgrs10

assert g.contains(g.mgrs1)
assert g.mgrs10k.contains(g)
assert g.mgrs1.isContainedBy(g)
assert g.isContainedBy(g.mgrs10k)

def direction_test(a,b):
    out={}
    #print a,(a.lat,a.lon),b,(b.lat,b.lon)

    out['bearing']=a.bearing(b)
    out['heading']=a.heading(b)
    out['heading_abbr']=a.heading(b)
    out['north']={'sphere':a.isNorthOf(b),'cartesian':a.isNorthOf(b,cartesian=True)}
    out['east']={'sphere':a.isEastOf(b),'cartesian':a.isEastOf(b,cartesian=True)}
    out['south']={'sphere':a.isSouthOf(b),'cartesian':a.isSouthOf(b,cartesian=True)}
    out['west']={'sphere':a.isWestOf(b),'cartesian':a.isWestOf(b,cartesian=True)}

    return out

#these tests represent four sides of a square on the Earth's surface

d=direction_test(Grid(10,10),Grid(10,-10))   #west
assert d['north']['sphere']==False
assert d['north']['cartesian']==False
assert d['east']['sphere']==False
assert d['east']['cartesian']==False
assert d['south']['sphere']==False
assert d['south']['cartesian']==False
assert d['west']['sphere']==True
assert d['west']['cartesian']==True


d=direction_test(Grid(10,-10),Grid(-10,-10)) #south
assert d['north']['sphere']==False
assert d['north']['cartesian']==False
assert d['east']['sphere']==False
assert d['east']['cartesian']==False
assert d['south']['sphere']==True
assert d['south']['cartesian']==True
assert d['west']['sphere']==False
assert d['west']['cartesian']==False


d=direction_test(Grid(-10,-10),Grid(-10,10)) #east
assert d['north']['sphere']==False
assert d['north']['cartesian']==False
assert d['east']['sphere']==True
assert d['east']['cartesian']==True
assert d['south']['sphere']==False
assert d['south']['cartesian']==False
assert d['west']['sphere']==False
assert d['west']['cartesian']==False

d=direction_test(Grid(-10,10),Grid(10,10))   #north
assert d['north']['sphere']==True
assert d['north']['cartesian']==True
assert d['east']['sphere']==False
assert d['east']['cartesian']==False
assert d['south']['sphere']==False
assert d['south']['cartesian']==False
assert d['west']['sphere']==False
assert d['west']['cartesian']==False

#similar to the above test group - but breaking out of the cardinal directions
d=direction_test(Grid(10,109),Grid(-71,-109))
assert d['north']['sphere']==False
assert d['north']['cartesian']==False
assert d['east']['sphere']==True
assert d['east']['cartesian']==False
assert d['south']['sphere']==True
assert d['south']['cartesian']==True
assert d['west']['sphere']==False
assert d['west']['cartesian']==True

# these two locations are on either side of the international date line, when using WGS84 179W is considered East of 179E, when using cartesian space the opposite is true
d=direction_test(Grid(0,179),Grid(0,-179))
assert d['west']['sphere']==False
assert d['west']['cartesian']==True
assert d['east']['sphere']==True
assert d['east']['cartesian']==False

k=Grid('4QGH94933312')

assert sorted(k.neighbors)==sorted([k.north,k.east,k.south,k.west])

assert k.adjoins(Grid('4QGH94933313'))
assert k.adjoins(Grid('4QGH94943312'))
assert k.adjoins(Grid('4QGH94933311'))
assert k.adjoins(Grid('4QGH94923312'))


def approxEqual(val1,val2,tol=0.05):
    val1=float(val1)
    val2=float(val2)
    r =1-(min([val1,val2])/max([val1,val2]))
    return r<float(tol)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


assert approxEqual(Grid(10,10).distance(Grid(-70,-71)),haversine(10,10,-71,-71))
assert approxEqual(Grid(10,10).distance(Grid(-70,-71),km=True),haversine(10,10,-71,-71)/1000)


l=[Grid(20,20),Grid('4QGH94933312'),Grid(-70,-70).mgrs10k]
print l
print sorted(l)


assert Grid(20,20)<Grid(-70,-70)
#asser

print "Grid passed"

#MgrsList & MgrsSet classes

