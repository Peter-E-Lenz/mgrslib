#
#  mgrslib - Geodetic opertions in MGRS space for Python
#
#  Copyright (c) Peter E Lenz [pelenz@pelenz.com]
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

import mgrs as MGRS 
import nvector as nv
import numbers

mgrs = MGRS.MGRS()

#mgrslib assumes ALL geodata is WGS84
wgs84 = nv.FrameE(name='WGS84')

class Lazy(object):
    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value 

#TBD: Add 4th Order compass points (i.e. North by East at azimuth 11.25)
compass = [
    {
        'name':'North',
        'shortname':'N',
        'azimuth':0,
        'order':1
    },
    {
        'name':'North-Northeast',
        'shortname':'NNE',
        'azimuth':22.5,
        'order':3
    },
    {
        'name':'Northeast',
        'shortname':'NE',
        'azimuth':45,
        'order':2
    },
    {
        'name':'East-Northeast',
        'shortname':'ENE',
        'azimuth':67.5,
        'order':3
    },
    {
        'name':'East',
        'shortname':'E',
        'azimuth':90,
        'order':1
    },
    {
        'name':'East-Southeast',
        'shortname':'ESE',
        'azimuth':112.5,
        'order':3
    },
    {
        'name':'Southeast',
        'shortname':'SE',
        'azimuth':135,
        'order':2
    },
    {
        'name':'South-Southeast',
        'shortname':'SSE',
        'azimuth':157.5,
        'order':3
    },
    {
        'name':'South',
        'shortname':'S',
        'azimuth':180,
        'order':1
    },
    {
        'name':'South-Southwest',
        'shortname':'SSW',
        'azimuth':202.5,
        'order':3
    },
    {
        'name':'Southwest',
        'shortname':'SW',
        'azimuth':225,
        'order':2
    },
    {
        'name':'West-Southwest',
        'shortname':'WSW',
        'azimuth':247.5,
        'order':3
    },
    {
        'name':'West',
        'shortname':'W',
        'azimuth':270,
        'order':1
    },
    {
        'name':'West-Northwest',
        'shortname':'WNW',
        'azimuth':292.5,
        'order':3
    },
    {
        'name':'Northwest',
        'shortname':'NW',
        'azimuth':315,
        'order':2
    },
    {
        'name':'North-Northwest',
        'shortname':'NNW',
        'azimuth':337.5,
        'order':3
    },
    {
        'name':'North',
        'shortname':'N',
        'azimuth':360,
        'order':1
    }
]

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

#TBD: a function for sorting grids North-South
#def ns_sort(grids):

#TBD: a function for sorting grids East-West
#def es_sort(grids):

#TBD: a function for sorting grids East-West than North-South
#def sort(grids):

#TBD: a function for returning the Northern-most member of a list
#TBD: a function for returning the Southern-most member of a list
#TBD: a function for returning the Eastern-most member of a list
#TBD: a function for returning the Western-most member of a list



class Grid(object):

    ######################
    #                    #
    #   PARSING GRID ID  #
    #                    #
    ######################
    @Lazy
    def __lastAlphaCharacter(self):
        c=-1
        for i in reversed(self.grid_id):
            c+=1
            if i.isalpha():
                return len(self.grid_id)-c
    @Lazy
    def gzd(self):
        return self.grid_id[0:self.__lastAlphaCharacter-2]

    @Lazy
    def grid_square(self):
        return self.grid_id[self.__lastAlphaCharacter-2:self.__lastAlphaCharacter]

    @Lazy
    def numerical_location(self):
        return self.grid_id[self.__lastAlphaCharacter:]

    @Lazy
    def easting(self):
        return self.grid_id[self.__lastAlphaCharacter:self.__lastAlphaCharacter+self.precision]

    @Lazy
    def northing(self):
        return self.grid_id[self.__lastAlphaCharacter+self.precision:]

    ############################
    #                          #
    #   GRID CHARACTERISTICS   #
    #                          #
    ############################

    @Lazy
    def size(self):
        return int('1'+('0'*(abs(5-self.precision))))

    @Lazy
    def precision(self):
        return len(self.numerical_location)/2

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
            grid_id=self.gzd+self.grid_square+self.easting[:newPrecsision]+self.northing[:newPrecsision]
            return Grid(grid_id,precision=newPrecsision,source=source)
        else:
            source = 'downsize'
            #smaller size - return new Grid object based on currect Grid object's lat/lon value at the newPrecsision size
            return Grid(self.lat,self.lon,precision=newPrecsision,source=source)

    @Lazy
    def mgrs1(self):
        #5
        return self.resize(5)

    @Lazy
    def mgrs10(self):
        #4
        return self.resize(4)

    @Lazy
    def mgrs100(self):
        #3
        return self.resize(3)

    @Lazy
    def mgrs1000(self):
        #2
        return self.resize(2)

    @Lazy
    def mgrs1k(self):
        #2
        return self.mgrs1000

    @Lazy
    def mgrs10000(self):
        #1
        return self.resize(1)

    @Lazy
    def mgrs10k(self):
        #1
        return self.mgrs10000

    @Lazy
    def mgrs100000(self):
        #0
        return Grid(self.gzd+self.grid_square)

    @Lazy
    def mgrs100k(self):
        #0
        return self.mgrs100000


    ######################
    #                    #
    #   GRID TRAVERSAL   #
    #                    #
    ######################


    @Lazy
    def _point(self):
        return wgs84.GeoPoint(latitude=self.lat, longitude=self.lon, z=0, degrees=True)

    def translate(self,dist,azimuth):
        dest, azimuth_dest = self._point.geo_point(distance=dist, azimuth=azimuth, degrees=True)
        return Grid(dest.latitude_deg,dest.longitude_deg,precision=self.precision,source='translation')

    @Lazy
    def north(self):
        return self.translate(self.size,0)

    @Lazy
    def south(self):
        return self.translate(self.size,180)

    @Lazy
    def east(self):
        return self.translate(self.size,90)

    @Lazy
    def west(self):
        return self.translate(self.size,270)

    def _distToGridCount(self,dist):
        return max(int(dist/self.size),1)

    def distance(self,gridB,heading=False):
        dist, _azia, _azib = self._point.distance_and_azimuth(gridB._point)
        return dist

    def square_buffer(self,dist,distY=None):
        if not distY:
            distY=dist
        
        row=self.translate(dist/2,270).translate(distY/2,180)
        cell=row
        out=[]
        for i in range(self._distToGridCount(distY)):
            for j in range(self._distToGridCount(dist)):
                out.append(cell)
                cell=cell.east
            row=row.north
            cell=row

        if len(out)==0:
            return [self]
        else:
            return out

    def buffer(self,dist):
        sq=self.square_buffer(dist)
        out=[]
        for i in sq:
            if self.distance(i)<=dist/2:
                out.append(i)
        if len(out)==0:
            return [self]
        else:
            return out

    ###############################
    #                             #
    #   AZIMUTHAL RELATIONSHIPS   #
    #                             #
    ###############################


    def azimuth(self,gridB):
        _dist, azia, _azib = self._point.distance_and_azimuth(gridB._point)
        return azia

    def heading(self,gridB,order=3,shortNames=False):
        a=self.azimuth(gridB)
        s=0
        out=None
        for i in compass:
            if i['order']<=order:
                d=max(a,i['azimuth'])-min(a,i['azimuth'])
                if d>s:
                    if shortNames:
                        out=i['shortname']
                    else:
                        out=i['name']

        return out

    def isNorthOf(self,gridB,azimuthal=False):
        if azimuthal:
            if 'N' in self.heading(gridB,order=4,shortNames=True):
                return True
            else:
                return False
        else:
            if self.latitude>=gribB.latitude:
                return True
            else:
                return False

    def isSouthOf(self,gridB,azimuthal=True):
        if azimuthal:
            if 'S' in self.heading(gridB,order=3,shortNames=True):
                return True
            else:
                return False
        else:
            if self.latitude<=gribB.latitude:
                return True
            else:
                return False

    def isEastOf(self,gridB,azimuthal=True):
        if azimuthal:
            if 'E' in self.heading(gridB,order=3,shortNames=True):
                return True
            else:
                return False
        else:
            if self.longitude>=gribB.longitude:
                return True
            else:
                return False

    def isWestOf(self,gridB,azimuthal=True):
        if azimuthal:
            if 'W' in self.heading(gridB,order=3,shortNames=True):
                return True
            else:
                return False
        else:
            if self.longitude<=gribB.longitude:
                return True
            else:
                return False

    #############################
    #                           #
    #   ADJOINAL RELATIONSHIPS  #
    #                           #
    #############################

    #FUTURE ENHANCEMENT

    #def ajoins(self,gribB):
    #    pass

    #################################
    #                               #
    #   PARENT/CHILD RELATIONSHIPS  #
    #                               #
    #################################

    #FUTURE ENHANCEMENT

    #def contains(self,gribB,bilateral=False):
    #   pass


    #########################
    #                       #
    #   POLYGON BOUNDARIES  #
    #                       #
    #########################

    #FUTURE ENHANCEMENT


    def __str__(self):
        return self.grid_id

    def __repr__(self):
        return self.grid_id

    def __init__(self,lat,lon=None,precision=5,source=None):

        if isinstance(lat,numbers.Number) and isinstance(lon,numbers.Number):
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

            self.grid_id = lat

            ll=mgrs.toLatLon(self.grid_id)
            self.lat=ll[0]
            self.latitude = self.lat
            self.lon=ll[1]
            self.longitude = self.lon

        #TBD - add UTM as input
