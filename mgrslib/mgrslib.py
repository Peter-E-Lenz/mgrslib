#
#  mgrslib
#  Geodetic operations in MGRS space for Data Scientists
#  version 0.0.1 
#  alpha status
#
#  http://www.pelenz.com/mgrslib
#  http://www.github.com/peter-e-lenz/mgrslib
#
#  Copyright 2017 (c) Peter E Lenz [pelenz@pelenz.com]
#  All rights reserved. 
#
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  software and associated documentation files (the "Software"), to deal in the Software 
#  without restriction, including without limitation the rights to use, copy, modify, merge,
#  publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
#  to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

from mgrs import MGRS 
from nvector import FrameE, deg
from collections import namedtuple
from math import fabs
from numbers import Number as number

mgrs = MGRS()

#mgrslib assumes all geodata is WGS84
wgs84 = FrameE(name='WGS84')

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def _instanceTypeCheck(inst,typeof):
    if not isinstance(typeof,list):
        typeof=[typeof]

    matchesAny = False

    for i in typeof:
        if isinstance(inst,i):
            matchesAny = True
            break

    if not matchesAny:
        acceptable = ', '.join([str(i) for i in typeof])
        
        isMultMsg=''
        if len(typeof)>1:
            isMultMsg='one of '
        
        raise TypeError('Variable type must be '+isMultMsg+acceptable+'. Input was type '+str(type(inst)))

class Heading(object):
    def __init__(self, name, abbr, azimuth, order):
        self.name=name
        self.abbr=abbr
        self.azimuth=float(azimuth)
        self.order=order

    def __repr__(self):
        return self.name
    
    def __float__(self):
        return self.azimuth

    def __str__(self):
        return self.name

    def __abs__(self):
        return abs(self.azimuth)

    def __eq__(self,azimuthB):
        if isinstance(azimuthB,Heading):
            return self.__dict__ == azimuthB.__dict__
        else:
            return self.azimuth == azimuthB

    def __ne__(self,azimuthB):
        if isinstance(azimuthB,Heading):
            return self.__dict__ != azimuthB.__dict__
        else:
            return self.azimuth != azimuthB

    def __gt__(self,azimuthB):
        return float(azimuthB)>self.azimuth
    
    def __lt__(self,azimuthB):
        return float(azimuthB)<self.azimuth

    def __ge__(self,azimuthB):
        return float(azimuthB)>=self.azimuth

    def __le__(self,azimuthB):
        return float(azimuthB)<=self.azimuth

    #def next(self) 

class _Headings(dict):
    def __init__(self,c):
        self.iterlist__=[]
        for i in c:
            h=Heading(i['name'],i['abbr'],i['azimuth'],i['order'])
            if i['name'] not in c:
                self[i['name'].lower().replace(' ','-')]=h
            self.iterlist__.append(h)

    def __getattr__(self, name):
        return self[name.lower()]

    def __setattr__(self, name, value):
        if '__' not in name:
            _instanceTypeCheck(value,Heading)
            self[name.lower()]=value
        else:
            self[name]=value

    def __delattr__(self, name):
        del self[name]

    def __iter__(self):
        return iter(self.iterlist__)

    def __repr__(self):
        return '< Headings '+repr(self.keys())+' >'

    def findHeading(self,bearing,order=3):
        s=361
        out=None

        for i in self.iterlist__:
            if i.order<=order:
                d=max(bearing,i.azimuth)-min(bearing,i.azimuth)
                if d < s:
                    s = d
                    out = i
                else:
                    return out
        return out

_compass = [
    {
        'name':'North',
        'abbr':'N',
        'azimuth':0,
        'order':1
    },
    {
        'name':'North by East',
        'abbr':'NbE',
        'azimuth':11.25,
        'order':4
    },
    {
        'name':'North-Northeast',
        'abbr':'NNE',
        'azimuth':22.5,
        'order':3
    },
    {
        'name':'Northeast by North',
        'abbr':'NEbN',
        'azimuth':33.75,
        'order':4
    },
    {
        'name':'Northeast',
        'abbr':'NE',
        'azimuth':45,
        'order':2
    },
    {
        'name':'Northeast by East',
        'abbr':'NEbE',
        'azimuth':56.25,
        'order':4
    },
    {
        'name':'East-Northeast',
        'abbr':'ENE',
        'azimuth':67.5,
        'order':3
    },
    {
        'name':'East by North',
        'abbr':'EbN',
        'azimuth':78.75,
        'order':4
    },
    {
        'name':'East',
        'abbr':'E',
        'azimuth':90,
        'order':1
    },
    {
        'name':'East by South',
        'abbr':'EbS',
        'azimuth':101.25,
        'order':4
    },
    {
        'name':'East-Southeast',
        'abbr':'ESE',
        'azimuth':112.5,
        'order':3
    },
    {
        'name':'Southeast by East',
        'abbr':'SEbE',
        'azimuth':123.75,
        'order':4
    },
    {
        'name':'Southeast',
        'abbr':'SE',
        'azimuth':135,
        'order':2
    },
    {
        'name':'Southeast by South',
        'abbr':'SEbS',
        'azimuth':146.25,
        'order':4
    },
    {
        'name':'South-Southeast',
        'abbr':'SSE',
        'azimuth':157.5,
        'order':3
    },
    {
        'name':'South by East',
        'abbr':'SbE',
        'azimuth':168.75,
        'order':4
    },
    {
        'name':'South',
        'abbr':'S',
        'azimuth':180,
        'order':1
    },
    {
        'name':'South by West',
        'abbr':'SbW',
        'azimuth':191.25,
        'order':4
    },
    {
        'name':'South-Southwest',
        'abbr':'SSW',
        'azimuth':202.5,
        'order':3
    },
    {
        'name':'Southwest by South',
        'abbr':'SWbS',
        'azimuth':213.75,
        'order':4
    },
    {
        'name':'Southwest',
        'abbr':'SW',
        'azimuth':225,
        'order':2
    },
    {
        'name':'Southwest by West',
        'abbr':'SWbW',
        'azimuth':236.25,
        'order':4
    },
    {
        'name':'West-Southwest',
        'abbr':'WSW',
        'azimuth':247.5,
        'order':3
    },
    {
        'name':'West by South',
        'abbr':'WbS',
        'azimuth':258.75,
        'order':4
    },
    {
        'name':'West',
        'abbr':'W',
        'azimuth':270,
        'order':1
    },
    {
        'name':'West by North',
        'abbr':'WbN',
        'azimuth':281.25,
        'order':4
    },
    {
        'name':'West-Northwest',
        'abbr':'WNW',
        'azimuth':292.5,
        'order':3
    },
    {
        'name':'Northwest by West',
        'abbr':'NWbW',
        'azimuth':303.75,
        'order':4
    },
    {
        'name':'Northwest',
        'abbr':'NW',
        'azimuth':315,
        'order':2
    },
    {
        'name':'Northwest by North',
        'abbr':'NWbN',
        'azimuth':326.25,
        'order':4
    },
    {
        'name':'North-Northwest',
        'abbr':'NNW',
        'azimuth':337.5,
        'order':3
    },
    {
        'name':'North by West',
        'abbr':'NbW',
        'azimuth':348.75,
        'order':4
    },
    {
        'name':'North',
        'abbr':'N',
        'azimuth':360,
        'order':1
    }
]

Compass = _Headings(_compass)

class _GeometryStore(object):
    #This is dumb, we don't need this level of complexity here
    def __init__(self):
        self.Point = namedtuple('Point','latitude longitude')
        self.Segment = namedtuple('Segment','origin destination')
        self.Line = namedtuple('Line','origin destination')
        self.Rect = namedtuple('Rectangle','southeast southwest northeast northwest')
        self.Polygon = namedtuple('Polygon', 'segments')
        self.MultiPolygon = namedtuple('Multipolygon', 'polygons')

    #def quadToPolygon(self,quad):
    #    pass



_Geometry = _GeometryStore()

#TBD: a function for returning the grid that is the average of a list of grids 
#def average(grids):
#    #averages the locations of a list of grids
#    pass

#TBD: a function for determining if all members of a list are contiguous
#def isContiguous(grids):

#tbd: a function for determining if any member of a list of grids are non-contiguous
#def isNonContiguous(grids)

#TBD: a function for determining if all members of a list are non-contiguous
#def isIsolate(grids):

#TBD: a function for returning the Northern-most member of a list/set
#TBD: a function for returning the Southern-most member of a list/set
#TBD: a function for returning the Eastern-most member of a list/set
#TBD: a function for returning the Western-most member of a list/set
#TBD: a function for returning the Center-most member of a list/set
#TBD: a function for returning the Boundary-members of a list/set (i.e. any grid with less then 4 neighbors also in the set)

    ######################
    #                    #
    #   THE GRID OBJECT  #
    #                    #
    ######################

class Grid(object):

    ######################
    #                    #
    #   PARSING GRID ID  #
    #                    #
    ######################
    @property
    def __lastAlphaCharacter(self):
        c=-1
        for i in reversed(self.grid_id):
            c+=1
            if i.isalpha():
                return len(self.grid_id)-c
    @property
    def gzd(self):
        return self.grid_id[0:self.__lastAlphaCharacter-2]

    @property
    def gridSquare(self):
        return self.grid_id[self.__lastAlphaCharacter-2:self.__lastAlphaCharacter]

    @property
    def __numerical_location(self):
            try:
                return int(self.grid_id[self.__lastAlphaCharacter:])
            except:
                return 0
    @property
    def easting(self):
        return int(self.grid_id[self.__lastAlphaCharacter:self.__lastAlphaCharacter+self.precision])

    @property
    def northing(self):
        return int(self.grid_id[self.__lastAlphaCharacter+self.precision:])



    ############################
    #                          #
    #   GRID CHARACTERISTICS   #
    #                          #
    ############################

    @property
    def size(self):
        return int('1'+('0'*(abs(5-self.precision))))

    @property
    def precision(self):
        return len(str(self.__numerical_location))/2

    #####################
    #                   #
    #   RESIZING GRIDS  #
    #                   #
    #####################


    def resize(self,newPrecsision):

        if self.precision==newPrecsision:
            return self
        elif self.precision>newPrecsision:
            #larger size, truncate mgrs easting and northing
            source = 'upsize'
            grid_id=self.gzd+self.gridSquare+str(self.easting)[:newPrecsision]+str(self.northing)[:newPrecsision]
            return Grid(grid_id,precision=newPrecsision,source=source)
        else:
            source = 'downsize'
            #smaller size - return new Grid object based on currect Grid object's lat/lon value at the newPrecsision size
            return Grid(self.lat,self.lon,precision=newPrecsision,source=source)

    @property
    def mgrs1(self):
        #5
        return self.resize(5)

    @property
    def mgrs10(self):
        #4
        return self.resize(4)

    @property
    def mgrs100(self):
        #3
        return self.resize(3)

    @property
    def mgrs1000(self):
        #2
        return self.resize(2)

    @property
    def mgrs1k(self):
        #2
        return self.mgrs1000

    @property
    def mgrs10000(self):
        #1
        return self.resize(1)

    @property
    def mgrs10k(self):
        #1
        return self.mgrs10000

    @property
    def mgrs100000(self):
        #0
        return Grid(self.gzd+self.gridSquare)

    @property
    def mgrs100k(self):
        #0
        return self.mgrs100000

    def increase(self,increase_by=1):
        for i in range(decrease_by):
            r = self.resize(self.grid_id,precision=min([self.precision-1,1]),source='upsize')
        return r

    def decrease(self,decrease_by=1):
        for i in range(decrease_by):
            r=self.resize(self.grid_id,precision=max([self.precision+1,5]),source='downsize')
        return r

    ######################
    #                    #
    #   GRID TRAVERSAL   #
    #                    #
    ######################


    @property
    def __point(self):
        return wgs84.GeoPoint(latitude=self.lat, longitude=self.lon, z=0, degrees=True)

    def translate(self,dist,azimuth):
        dest, azimuth_dest = self.__point.geo_point(distance=dist, azimuth=azimuth, degrees=True)
        return Grid(dest.latitude_deg,dest.longitude_deg,precision=self.precision,source='translation')

    @property
    def north(self):
        return self.translate(self.size,Compass.north)

    @property
    def east(self):
        return self.translate(self.size,Compass.east)

    @property
    def south(self):
        return self.translate(self.size,Compass.south)

    @property
    def west(self):
        return self.translate(self.size,Compass.west)

    ################
    #              #
    #   DISTANCE   #
    #              #
    ################

    def __distToGridCount(self,dist):
        return max(int(dist/self.size),1)

    def distance(self,gridB,km=False):
        _instanceTypeCheck(gridB,Grid)

        dist, _azia, _azib = self.__point.distance_and_azimuth(gridB.__point)

        if km:
            return dist/1000.0
        else:
            return dist

    #def manhattan_distance(self,GridB):
    #    pass


    ###############
    #             #
    #   BUFFERS   #
    #             #
    ###############

    def rectBuffer(self,dist,distY=None):
        #TBD: return values in a GridList
        dist=int(dist)

        if not distY:
            distY=dist
        else:
            distY=int(distY)        

        row=self.translate(int(dist/2),Compass.west).translate(int(distY/2),Compass.south)
        cell=row
        out=mgrsList()
        for i in range(self.__distToGridCount(distY)):
            for j in range(self.__distToGridCount(dist)):
                out.append(cell)
                cell=cell.east
            row=row.north
            cell=row

        if len(out)==0:
            return [self]
        else:
            return out

    def buffer(self,dist):
        #TBD: return values in a GridList
        sq=self.rectBuffer(dist*2)
        out=mgrsList()
        for i in sq:
            if self.distance(i)<=dist:
                out.append(i)
        if len(out)==0:
            return [self]
        else:
            return out

    ################################
    #                              #
    #   DIRECTIONAL RELATIONSHIPS  #
    #                              #
    ################################


    def bearing(self,gridB):
            _instanceTypeCheck(gridB,Grid)

            _dist, azia, _azib = self.__point.distance_and_azimuth(gridB.__point)
            return deg(azia)

    def heading(self,gridB,order=4):
        _instanceTypeCheck(gridB,Grid)

        a=self.bearing(gridB)

        if a < 0:
            a = 360-fabs(a)

        return Compass.findHeading(a,order=order)

    def isNorthOf(self,gridB,cartesian=False,order=4):
        _instanceTypeCheck(gridB,Grid)

        if not cartesian:
            if 'N' in self.heading(gridB,order=order).abbr:
                return True
            else:
                return False
        else:
            if self.latitude<gridB.latitude:
                return True
            else:
                return False

    def isSouthOf(self,gridB,cartesian=False,order=4):
        _instanceTypeCheck(gridB,Grid)

        if not cartesian:
            if 'S' in self.heading(gridB,order=order).abbr:
                return True
            else:
                return False
        else:
            if self.latitude>gridB.latitude:
                return True
            else:
                return False

    def isEastOf(self,gridB,cartesian=False,order=4):
        _instanceTypeCheck(gridB,Grid)

        if not cartesian:
            if 'E' in self.heading(gridB,order=order).abbr:
                return True
            else:
                return False
        else:
            if self.longitude<gridB.longitude:
                return True
            else:
                return False

    def isWestOf(self,gridB,cartesian=False,order=4):
        _instanceTypeCheck(gridB,Grid)

        if not cartesian:
            if 'W' in self.heading(gridB,order=order).abbr:
                return True
            else:
                return False
        else:
            if self.longitude>gridB.longitude:
                return True
            else:
                return False


    #################################
    #                               #
    #   PARENT/CHILD RELATIONSHIPS  #
    #                               #
    #################################

    def contains(self,gridB):
        _instanceTypeCheck(gridB,Grid)

        if self.precision<gridB.precision:
                if gridB.resize(self.precision)==self:
                    return True
                else:
                    return False
        else:
            return False

    def isContainedBy(self,gridB):
        _instanceTypeCheck(gridB,Grid)

        if self.precision>gridB.precision:
            if self.resize(gridB.precision)==gridB:
                return True
            else:
                return False
        else:
            return False

    def __contains__(x):
        _instanceTypeCheck(gridB,Grid)
        return self.contains(x)

    #############################
    #                           #
    #   ADJOINAL RELATIONSHIPS  #
    #                           #
    #############################

    @property
    def neighbors(self):
        #TBD: make output into a GridList
        out = mgrsList()
        out.append(self.north)
        out.append(self.east)
        out.append(self.south)
        out.append(self.west)
        return out

    def adjoins(self,gridB):
        _instanceTypeCheck(gridB,Grid)

        if self.size==gridB.size:
            #compare this grid to a same sized grid
            neighbors=self.neighbors
            if gridB in neighbors:
                return True
            else:
                return False
        else:
            #disimalar sized grids
            if self.precision>gridB.precision:
                smaller=gridB
                larger=self
            else:
                larger=gridB
                smaller=self

            neighbors=[i.resize(larger.precision) for i in smaller.neighbors]
            #    smaller.north.resize(larger.precision), 
            #    smaller.east.resize(larger.precision), 
            #    smaller.south.resize(larger.precision), 
            #    smaller.west.resize(larger.precision)
            #]

            if larger in neighbors:
                return True
            else:
                return False



    ################
    #              #
    #   GEOMETRY   #
    #              #
    ################

    @property
    def point(self):
        return _Geometry.Point(self.latitude,self.longitude)

    @property
    def boundingBox(self):
        out ={}
        
        sw = self
        se = self.translate(self.size,90)
        ne = se.translate(self.size,0)
        nw = se.translate(self.size,270)

        se_p=_Geometry.Point(se.latitude,se.longitude)
        sw_p=_Geometry.Point(sw.latitude,sw.longitude)
        ne_p=_Geometry.Point(ne.latitude,ne.longitude)
        nw_p=_Geometry.Point(nw.latitude,nw.longitude)

        #bb=_Geometry.Polygon([_Geometry.Segment(se_p,_Geometry.Segment(sw_p,_Geometry.Segment(ne_p,_Geometry.Segment(nw_p, None))))])
        bb=_Geometry.Rect(se_p,sw_p,ne_p,nw_p)

        return bb


    def __str__(self):
        return self.grid_id

    def __repr__(self):
        return self.grid_id

    def __eq__(self, gridB):
        if self.grid_id.lstrip('0') == gridB.grid_id.lstrip('0'):
            return True
        else:
            return False

    def __ne__(self, gridB):
        return not self.__eq__(gridB)

    #This is not the right way to do this - rewrite these!
    def __gt__(self, gridB):
        return (self.isNorthOf(gridB) and self.isEastOf(gridB))

    def __lt__(self, gridB):
        return (self.isSouthOf(gridB) and self.isWestOf(gridB))


    def __ge__(self, gridB):
        if self==gribB:
            return True
        return self.__gt__(gribB)

    def __le__(self, gridB):
        if self==gribB:
            return True
        return self.__le__(gribB)

    def __contains__(self,gribB):
        return self.contains(gribB)
    
    def __init__(self,lat,lon=None,precision=5,source=None):

        if isinstance(lat,number) and isinstance(lon,number):
            # passed in lat/lon pair
            if source == None:
                self.source='lat/lon'
            else:
                self.source=source

            self.grid_id = mgrs.toMGRS(lat, lon, MGRSPrecision=precision)

            self.lat=lat
            self.latitude = self.lat
            self.lon=lon
            self.longitude = self.lon


        elif isinstance(lat,str) and lon == None:
            # passed in mgrs grid id
            if source == None:
                self.source='grid_id'
            else:
                self.source=source

            self.grid_id = lat.upper().replace(' ','')

            ll=mgrs.toLatLon(self.grid_id)
            self.lat=ll[0]
            self.latitude = self.lat
            self.lon=ll[1]
            self.longitude = self.lon

        else:
            if lon==None:
                pass
                #throw error, can not make a grid from lat
            else:
                pass
                #throw error, can not make a valid grid from these inputs


    ####################################
    #                                  #
    #   MGRSSET/MGRSLIST PARENT CLASS  #
    #                                  #
    ####################################

class _gridStruct(object):

    def containsOnlyGrids(self):
        test = [True if isinstance(i,Grid) else False for i in self]
        if False in test:
            return False
        else:
            return True

    def removeNonGrids(self):
        for i in self:
            if not isinstance(i,Grid):
                del self[i]
 
    def isContiguous(self,grid,diagonal=False):
        #return true if all neighbors of g have the same membership type as grid
        membershipType = grid in self
        tests = [(i in self) == membershipType for i in grid.neighbors]
        return not (False in tests) 

    def isIsoated(self,grid,diagonal=False):
        #return true if all neighbors of g have the opposite membership type as grid
        membershipType = grid in self
        tests = [(i in self) == membershipType for i in grid.neighbors]
        return False in tests

    def __distanceMap(self,to):
        out={}
        for i in self:
            d=i.distance(to)
            if d not in out:
                out[d]=[i]
            else:
                out[d].append(i)
        return out

    def nearestTo(self,gridB):
        #returns the Grid in self closest to gridB
        d=self.__distanceMap(gridB)
        return mgrsSet(d[min(d.keys())]).centerEasting()

    def centerEasting(self):
         #returns Grid containing the avg(latitude),max(longitude)
        lats = [i.latitude for i in self]
        lons = [i.longitude for i in self]
        c = Grid(mean(lats),max(lons))

        return c

    def centerX(self):
        return self.centerEasting()

    def centerNorthing(self):
         #returns Grid containing the avg(longitude),max(latitude) or else the nearest member of self to said point
        lats = [i.latitude for i in self]
        lons = [i.longitude for i in self]
        c = Grid(max(lats),mean(lons))

        return c

    def centerY(self):
        return self.centerNorthing()

    def centeroid(self):
        return Grid(self.centerNorthing().latitude,self.centerEasting().longitude)

    def northernmost(self):
        #returns the northernmost Grids in self. If multiple grids qualify it returns the one with max(easting)          
        max_lat = max(sorted(self, key=lambda x: x.latitude))
        print max_lat
        return self.__offspring([i for i in self if i.latitude==max_lat.latitude])

    def westernmost(self):
        #returns the westernmost Grids in self.           
        min_lon = min(sorted(self, key=lambda x: x.longitude))
        return self.__offspring([i for i in self if i.longitude==min_lon.longitude])

    def easternmost(self):
         #returns the easternmost Grids in self.      
        max_lon = max(sorted(self, key=lambda x: x.longitude))
        return self.__offspring([i for i in self if i.longitude==max_lon.longitude])

    def southernmost(self):
        #returns the southernmost Grids in self.
        min_lat = min(sorted(self, key=lambda x: x.latitude))
        return self.__offspring([i for i in self if i.latitude==min_lat.latitude])

    def exterior(self):
        out=[]
        for g in self:
            for n in g.neighbors:
                if n not in self:
                    out.append(g)
                    break
        return self.__offspring(out)

    def interior(self):
        return self.__offspring(mgrsSet(self).difference(mgrsSet(self.exterior())))

    def boundingBox(self):
        #returns grids at the corners of a bounding box encomposing all members of self
        nw = _Geometry.Point(self.northernmost().longitude,westernmost().latitude)
        ne = _Geometry.Point(self.northernmost().longitude,easternmost().latitude)
        sw = _Geometry.Point(self.southernmost().longitude,westernmost().latitude)
        se = _Geometry.Point(self.southernmost().longitude,easternmost().latitude)

        return _Geometry.Rect(se,sw,ne,nw)

    def __offspring(self,struct):
        if isinstance(self,mgrsSet):
            return mgrsSet(struct)
        elif isinstance(self,mgrsList):
            return mgrsList(struct)

    def __insert(self,item):
        if isinstance(self,mgrsSet):
            self.add(item)
        elif isinstance(self,mgrsList):
            self.append(item)


    ###############################################################
    #                                                             #
    #   CREATE MGRSSET/MGRSLIST CLASSES VIA MULTIPLE INHERITANCE  #
    #                                                             #
    ###############################################################


class mgrsList(list, _gridStruct):
    pass

class mgrsSet(set, _gridStruct):
    pass
