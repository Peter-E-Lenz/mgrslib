<span style="font-variant: small-caps">mgrslib</span> is a python library meant to simplify working with MGRS space.

## Introduction

[MGRS (Military Grid Reference System)](https://en.wikipedia.org/wiki/MGRS) is a system originally created by [NATO](https://en.wikipedia.org/wiki/NATO)  for [ gridifying ](http://earth-info.nga.mil/GandG/coordsys/grids/universal_grid_system.html) location data anywhere on earth by assigning every location to a tessellating set of grids, with each grid having a unique semantic string identifier.  Beyond its military applications MGRS is also very useful for data scientists working with spatial data for a number of jobs:
* dimensionality reduction
* featurization
* key-value stores
* gridification

The downside of working in MGRS is that there are few good tools for doing geodetic operations directly in MGRS space. I wrote <span style="font-variant: small-caps">mgrslib</span> to rectify this and - quite frankly - make my life as a geographer easier.

<span style="font-variant: small-caps">mgrslib</span> follows the [worse is better](https://en.wikipedia.org/wiki/Worse_is_better) design philosophy; it's better to have a slower less featureful implementation then no implementation at all. Optimizations will be executed when we have to.

## License

<span style="font-variant: small-caps">mgrslib</span> is licensed under the MIT License and offered as is without warranty of any kind, express or implied. 

## Installation

#### From PyPi

#### From Git

### Dependencies
<span style="font-variant: small-caps">mgrslib</span> uses the python [MGRS package](https://github.com/hobu/mgrs) for transforming between lat/lon and mgrs space which is in turn a thin wrapper around the [geotrans](http://earth-info.nga.mil/GandG/geotrans/) library from the [U.S. National Geo-Spatial Intelligence Agency](https://nga.mil ).
<span style="font-variant: small-caps">mgrslib</span> uses the [python port](https://pypi.python.org/pypi/nvector) of the [N-Vector package](http://www.navlab.net/nvector/) from the [Norwegian Defense Research Establishment](http://www.ffi.no/en/Sider/default.aspx) for spatial calculations.

When installing from PyPi these dependencies are handled automatically.

### Assumptions

<span style="font-variant: small-caps">mgrslib</span> performs all spatial calculations using the [WGS84 datum](https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84).
<span style="font-variant: small-caps">mgrslib</span> calculates all [bearings](https://en.wikipedia.org/wiki/Bearing_(navigation)) relative to [true north](https://en.wikipedia.org/wiki/True_north).

## Initializing Grid objects

##### Grid(Float/Int *latitude*,Float/Int *longitude*,[Int *precision* = 1...5])
##### Grid(String *grid_id*,[Int *precision* = 1...5])
##### Grid(Grid *grid_id*,[Int *precision* = 1...5])



| Type | Returns |
| ---- | ------- |
| Class | Grid Object |

Initializes a Grid object from a latitude and longitude, a string MGRS grid id, or another Grid object. If a *precision* is not set the Grid object will default to a *precision* of 5, the most precise value possible. Please refer to Grid.**precision**, later in this document, for more information about *precision* values.
TBD: allow initializing a Grid object from a [UTM](https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system)

### Grid object Equality
A Grid object is equal to another Grid object if the MGRS representation is exactly equal the MGRS representation of another Grid object. Leading '0' characters are ignored during the equality test.

``` python
>>> Grid('4QGH94933312') == Grid(20.17289585706837,-156.1783234582578).mgrs10
True
```


### Sorting Grid objects
Grids are sortable using the default Python methods:
``` python
sorted([Grid(20,20),Grid('4QGH94933312')])
```

When compared to another Grid object Grids sort spatially, Southwest to Northeast i.e. -180 W, -90 S is considered larger than 180 E, 90 N. 
Grids will throw an error when compared to another type.

## Parsing

##### Grid.**gzd**

| Type | Returns |
| ---- | ------- |
| Property | String |

Returns the Grid Zone Designator of this Grid, a 6 degree wide by 8 degree tall region between 90N and 90S, various other shapes above and below those lines of latitude

##### Grid.**grid_square**

| Type | Returns |
| ---- | ------- |
| Property | String |

Returns the grid square of this Grid

##### Grid.**easting**

| Type | Returns |
| ---- | ------- |
| Property | String |

Returns the easting of this Grid

##### Grid.**northing**

| Type | Returns |
| ---- | ------- |
| Property | String |

Returns the northing of this Grid

## Latitude / Longitude

##### Grid.**latitude**
##### Grid.**lat**

| Type | Returns |
| ---- | ------- |
| Property | Float |

Returns the latitude of the southeastern corner of this MGRS grid in [decimal degress](https://en.wikipedia.org/wiki/Decimal_degrees)

##### Grid.**longitude**
##### Grid.**lon**

| Type | Returns |
| ---- | ------- |
| Property | Float |

Returns the longitude of the southeastern corner of this MGRS grid in [decimal degress](https://en.wikipedia.org/wiki/Decimal_degrees)


## Grid Characteristics

##### Grid.**source**

| Type | Returns |
| ---- | ------- |
| Property | String |

Returns a text description of what kind of data this Grid object was derived from:

| Description | Source |
| ----------- | ------ |
| lat/lon     | Grid(Float *latitude*, Float *longitude*) |
| grid_id     | Grid(Grid *grid*) **or** Grid(String *grid_id*) |
| upsize      | Existing Grid object resized to a lower precision *i.e.* Grid(20,20).mgrs1000|
| downsize    | Existing Grid object resized to a higher precision *i.e.* Grid('4QGH9433').mgrs1|
| translation | Traversal from existing Grid object *i.e.* Grid(20,20).east|


##### Grid.**size**

| Type | Returns |
| ---- | ------- |
| Property | Int |

Size is a measure of the length of a side of a grid in meters

##### Grid.**precision**

| Type | Returns |
| ---- | ------- |
| Property | Int |

Precision is a measure of the maximum level of accuracy of a grid, larger values have higher accuracy:

| Precision | Size of grid side |
|---|---|
| 5   |   1m |
| 4   |   10m |
| 3   |   100m |
| 2   |   1000m (1km) |
| 1   |   10000m (10km) |
| 0   |   100000m (100km) |

## Resizing

##### Grid.resize(Int *precision*)

| Type | Returns |
| ---- | ------- |
| Function | Grid object |

When resizing to a larger grid size (i.e from precision 4 to precision 3) is done by truncating the MGRS grid id in accordance with best practices.
When resizing to a smaller grid size (i.e from precision 3 to precision 4) is done by specifying a new Grid object of the lat/lon of the current Grid at the specified smaller precision

Convenience methods are provided to simplify this process:
| Convenience Method | Equivalent using Grid.resize() |
|-----------------|----------------| 
| Grid.mgrs1      | Grid.resize(5) |
| Grid.mgrs10     | Grid.resize(4) |
| Grid.mgrs100    | Grid.resize(3) |
| Grid.mgrs1000   | Grid.resize(2) |
| Grid.mgrs1k     | Grid.resize(2) |
| Grid.mgrs10000  | Grid.resize(1) |
| Grid.mgrs10k    | Grid.resize(1) |
| Grid.mgrs100000 | Grid.resize(0) |
| Grid.mgrs100k   | Grid.resize(0) |

#### TBD:

##### Grid.increase

| Type | Returns |
| ---- | ------- |
| Property | Grid object |

Returns a grid one precision level greater - that is one level smaller
If your current grid is already as precise as possible (i.e. precision 5) then an error is thrown

##### Grid.decrease

| Type | Returns |
| ---- | ------- |
| Property | Grid object |

Returns a grid one precision level lesser - that is one level larger
If your current grid is already as large as possible (i.e. precision 0) then an error is thrown


## Grid Traversal
##### Grid.translate(Float *distance*, Float *azimuth*)

| Type | Returns |
| ---- | ------- |
| Function | Grid object |

Returns the Grid at a location offset from the point-of-origin of the current grid by *distance* meters at *azimuth* degrees heading

Convenience methods for returning Grid objects of the adjacent grids in each of these directions:

| Convenience Method | Equivalent Grid.translate statement |
|------------|------------------------------| 
| Grid.north |Grid.translate(Grid.size,0)   |
| Grid.east  |Grid.translate(Grid.size,90)  |
| Grid.south |Grid.translate(Grid.size,180) |
| Grid.west  |Grid.translate(Grid.size,270) |

## Distance
##### Grid.distance(grid *grid*)

| Type | Returns |
| ---- | ------- |
| Function | Float |
Returns the distance in meters between the lat/lon representation of the current Grid to a second Grid object

### TBD:
##### Grid.manhattan_distance(Grid *grid*)

| Type | Returns |
| ---- | ------- |
| Function | Int |

Returns the [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) measured in grids from the current Grid to a second Grid object

## Buffering
##### Grid.rect_buffer(Float *width*,[Float *height*])

| Type | Returns |
| ---- | ------- |
| Function | Unsorted list of Grid objects |

Returns a list of Grid objects representing all the Grid objects with their lat/lon representation in a polygon *width* meters wide by *height* meters high centered on the lat/lon representation of the current Grid. If *height* is omitted the value for *width* will also be used for *height*.

##### Grid.buffer(Float *radius*)

| Type | Returns |
| ---- | ------- |
| Function | Unsorted list of Grid objects |

Returns a list containing all the Grid objects with their lat/lon representation in circular area with a radius of *radius* meters centered on the lat/lon representation of the current grid.

## Bearing and Heading

##### Grid.bearing(Grid *grid*)

| Type | Returns |
| ---- | ------- |
| Function | Float |


Returns the [bearing](https://en.wikipedia.org/wiki/Bearing_(navigation)) from the current Grid to *grid* relative to [true north](https://en.wikipedia.org/wiki/True_north). 

##### Grid.heading(Grid *grid*,[*order* = 3, *abbr* = False])

| Type | Returns |
| ---- | ------- |
| Function | String |

Returns the name or abbreviation of the nearest named [heading](https://en.wikipedia.org/wiki/Course_(navigation)) from the current Grid to *grid* relative to [true north](https://en.wikipedia.org/wiki/True_north). The higher the *order* value the more specific the heading will be. First order headings are limited to **North**, **East**, **South**, and **West**. Second order directions would include directions like **Northeast** or **Southwest**. Third order would include **East-Northeast** or **West-Northwest**. Fourth order directions add values like **Northwest by West** or **West by South**. The *abbr* value determines if this function will return the full text name of the heading or an abbreviation.

<span style="font-variant: small-caps">mgrslib</span> does not support half or quarter headings (fifth and sixth order directions respectively).

A complete list of supported directions is included at the end of this document and includes compass degress relative to geodetic true north, direction order, heading name, and abbreviations.

## Directional Relationships
##### Grid.isNorthOf(Grid *grid*, Int *order* = 3, Boolean *cartesian* = False)
##### Grid.isEastOf(Grid *grid*, Int *order* = 3, Boolean *cartesian* = False)
##### Grid.isSouthOf(Grid *grid*, Int *order* = 3, Boolean *cartesian* = False)
##### Grid.isWestOf(Grid *grid*, Int *order* = 3, Boolean *cartesian* = False)

| Type | Returns |
| ---- | ------- |
| Function | Boolean |

These functions are provided as tests to determine the spatial relations of two Grid objects.
The default behavior (i.e. *cartesian* is set to False) is to check the heading between the two Grids relative to true north.

Because this test is performed is near-spherical space has the advantage of working with any two locations, anywhere on the globe. However because it is in spherical space it directions are considered cones that radiate from a point. The angle of the cone is determined by the *order* argument.

If *cartesian* is set to True a different test is performed. Instead of assuming a spherical WGS84 space, points are instead cast into a cartesian plane bounded by 90S to 90N and 180W to 180E. This test has the advantage of assuming directions are defined by perfectly straight lines and can be better when working with Grids separated over short distances. (TBD: what is a short distance), however this test has issues with working with Grids that pass outside the cartesian plane. I.E. 179E Longitude is considered East of 179W Longitude.

**TBD**:
Rewrite this description - it is very confusing.


## Parent/Child Relationships
##### Grid.contains(Grid *grid*)

| Type | Returns |
| ---- | ------- |
| Function | Boolean |

Returns True if the current Grid contains *grid*.

#### TBD:
##### Grid.isContainedBy(Grid *grid*)

| Type | Returns |
| ---- | ------- |
| Function | Boolean |

Returns True if *grid* contains the current Grid.


## Adjoinal Relationships
##### Grid.adjoins(Grid *grid*)

| Type | Returns |
| ---- | ------- |
| Function | Boolean |

Returns True if the current Grid and *grid* share any common border and are not nested.


## Polygon Boundaries
##### Grid.bounds

| Type | Returns |
| ---- | ------- |
| Property | Dictionary |

Returns a dictionary with the keys **southeast**, **southwest**, **northwest**, and **northeast**. Each of these entries in turn is a dictionary with two keys: **latitude** and **longitude**
It is intended that this property will be useful for generating polygons of MGRS grids.

## Future roadmap:
In addition to the features above marked **TBD** I plan on adding the following features to <span style="font-variant: small-caps">mgrslib</span> prior to version 1.

### mgrsList and mgrsSet
These will be extensions of the default **List** and **Set** objects with addition methods for performing operations on groups of **Grid** objects. In addition to all the built-ins for these two type I intend to also have functions for:
* averageing
* northern/southern/eastern/western - most grids
* most central grid
* most isolated grid
* boundary grids

### Random MGRS grid generator
This function will generate a random MGRS grid id string at a given precision. In addition to just being a random generator this will be very useful for testing.


## Compass Headings
| Heading            | Abbreviation | Degrees | Order |
|--------------------|-----------|---------|-------|
| North              | N         | 0       | 1     |
| North by East      | NbE       | 11.25   | 4     |
| North-Northeast    | NNE       | 22.5    | 3     |
| Northeast by North | NEbN      | 33.75   | 4     |
| Northeast          | NE        | 45      | 2     |
| Northeast by East  | NEbE      | 56.25   | 4     |
| East-Northeast     | ENE       | 67.5    | 3     |
| East by North      | EbN       | 78.75   | 4     |
| East               | E         | 90      | 1     |
| East by South      | EbS       | 101.25  | 4     |
| East-Southeast     | ESE       | 112.5   | 3     |
| Southeast by East  | SEbE      | 123.75  | 4     |
| Southeast          | SE        | 135     | 2     |
| Southeast by South | SEbS      | 146.25  | 4     |
| South-Southeast    | SSE       | 157.5   | 3     |
| South by East      | SbE       | 168.75  | 4     |
| South              | S         | 180     | 1     |
| South by West      | SbW       | 191.25  | 4     |
| South-Southwest    | SSW       | 202.5   | 3     |
| Southwest by South | SWbS      | 213.75  | 4     |
| Southwest          | SW        | 225     | 2     |
| Southwest by West  | SWbW      | 236.25  | 4     |
| West-Southwest     | WSW       | 247.5   | 3     |
| West by South      | WbS       | 258.75  | 4     |
| West               | W         | 270     | 1     |
| West by North      | WbN       | 281.25  | 4     |
| West-Northwest     | WNW       | 292.5   | 3     |
| Northwest by West  | NWbW      | 303.75  | 4     |
| Northwest          | NW        | 315     | 2     |
| Northwest by North | NWbN      | 326.25  | 4     |
| North-Northwest    | NNW       | 337.5   | 3     |
| North by West      | NbW       | 348.75  | 4     |
