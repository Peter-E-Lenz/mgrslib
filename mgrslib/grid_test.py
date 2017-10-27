#settest

from mgrslib import *
import random

g=Grid(73,-43).mgrs1000.buffer(10000)
gg=mgrsSet(random.sample(g,15))

print len(g)

print g.northernmost()
print g.southernmost()
print g.westernmost()
print g.easternmost()

print g.centeroid()
print g.exterior()
print g.interior()

z=Grid(73,-43)
k=g.nearestTo(z)
print z,z.latitude,z.longitude
print k, k.latitude,k.longitude

z=Grid(20,20)
k=g.nearestTo(z)
print z,z.latitude,z.longitude
print k, k.latitude,k.longitude

print g.centeroid()
print gg.centeroid()
print g.centeroid().distance(gg.centeroid())
print g.nearestTo(gg.centeroid())
