from numpy.random import *
from pylab import *

import etframes


ys = [normal() for _ in range(100)]
xs = [normal() for _ in range(100)]

scatter(xs,ys)

etframes.add_dot_dash_plot(gca(), ys=ys, xs=xs)


show()

