
    ####################################
    #                                  #
    #   MGRSSET/MGRSLIST PARENT CLASS  #
    #                                  #
    ####################################

class _gridStruct(object):

    def __containsOnlyGrids(self):
        test = [True if isinstance(i,Grid) else False for i in self]
        if False in test:
            return False
        else:
            return True

    def __removeNonGrids(self):
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
        _instanceTypeCheck(value,Grid)
        if isinstance(self,mgrsSet):
            self.add(item)
        elif isinstance(self,mgrsList):
            self.append(item)

    #def rTree(self):
        #Future idea: r tree exporter


    ###############################################################
    #                                                             #
    #   CREATE MGRSSET/MGRSLIST CLASSES VIA MULTIPLE INHERITANCE  #
    #                                                             #
    ###############################################################


class mgrsList(list, _gridStruct):
    pass

class mgrsSet(set, _gridStruct):
    pass
