#
#  mgrslib
#  Geodetic operations in MGRS space for Data Scientists
#  version 0.0.1 
#  alpha status
#
#  http://www.pelenz.com/mgrslib
#  http://www.github.com/peter-e-lenz/mgrslib
#
#  Copyright 2017-2021 (c) Peter E Lenz [pelenz@pelenz.com]
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
from nvector import FrameE, deg #replace with pyproj
from pyproj import CRS
from collections import namedtuple
from math import fabs
from numbers import Number as number
from compassheadinglib import Compass

mgrs = MGRS()

#mgrslib assumes all geodata is WGS84
wgs84 = FrameE(name='WGS84')
#wgs84 = CRS.from_epsg(4326)

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

#TBD: a function for returning the grid that is the average of a list of grids 
#def average(grids):
#    #averages the locations of a list of grids
#    pass


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

