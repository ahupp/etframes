"""
This module implements two graph types described in Edward Tufte's
"Visual Display of Quantitative Information".

Author: Adam Hupp <adam@hupp.org>
License: Distributed under the PSF license, http://www.python.org/psf/license/

"""
import matplotlib.pylab

from matplotlib.collections import LineCollection
from matplotlib.artist import Artist
from matplotlib.ticker import FixedLocator

__all__ = ["add_range_frame", "add_dot_dash_plot"]


def cleanframe_and_ticks(axes):

    # Turn off the default frame
    axes.set_frame_on(False)

    # Only show ticks on bottom and left frame
    axes.get_xaxis().tick_bottom()
    axes.get_yaxis().tick_left()


def interval_frac(interval, datapoint):
    """Given an interval and a point in the same range, return
    the fractional distance of that point along the interval
    Clipped to [0,1]
    """
    pos = (datapoint - interval.get_bounds()[0])/interval.span()
    # don't allow past border of axis
    return max(0.0, min(1.0, pos))


def data_bounds_on_axis(view_interval, data_bounds):
    "Map min/max from data space to viewport space."
    
    if data_bounds is None:
        return (0.0, 1.0)
    
    lower = interval_frac(view_interval, data_bounds[0])
    upper = interval_frac(view_interval, data_bounds[1])
    return lower, upper


class RangeFrameArtist(Artist):
    "Draws range frames on a graph"
    
    def __init__(self, color, linewidth, xbounds, ybounds):
        """
        color: str indicating color of line
        linewidth: width of line to draw
        xbounds, ybounds: tuple (min,max) of data on x and y axis
        """
        Artist.__init__(self)
        self.color = color
        self.linewidth = linewidth
        self.xbounds = xbounds
        self.ybounds = ybounds
        
    def draw(self, renderer, *args, **kwargs):
        if not self.get_visible(): return

        rf = self.make_range_frame()
        rf.draw(renderer)


    def make_range_frame(self):

        xminf, xmaxf = data_bounds_on_axis(self.axes.viewLim.intervalx(),
                                           self.xbounds)

        yminf, ymaxf = data_bounds_on_axis(self.axes.viewLim.intervaly(),
                                           self.ybounds)


        xline = [(xminf,0), (xmaxf,0)]
        yline = [(0,yminf), (0,ymaxf)]

        range_lines = LineCollection(segments=[xline, yline],
                                     linewidths=[self.linewidth],
                                     colors=[self.color])

        range_lines.set_transform(self.axes.transAxes)
        range_lines.set_zorder(10)

        return range_lines




def add_range_frame(axes=None, color="k", linewidth=1.0,
                         xbounds=None, ybounds=None):
    """
    Adds a range frame to a matplotlib graph.  The range frame is
    described in Tufte's "The Visual Display of Quantitative
    Information" p. 130.

    The range frame is an unobtrusive way of marking the minimum and
    maxiumum values on a scatterplot or other graph.
    
    axes: the matplotlib axes to apply a range frame to.  If None or
    unspecified, use the current axes

    color: string specification of the color. default is 'k', (black)

    linewidth: width of lines in range frame

    xbounds, ybounds: tuple (min,max) on x and y axes

    
    """

# Implementation detail: you might expect that the range of values is
# available via axes.dataLim.  Unfortunitely this range seems to
# extend .2 past the real min and max.

    if axes is None:
        axes = matplotlib.pylab.gca()

    axes.add_artist(RangeFrameArtist(color=color,
                                     linewidth=linewidth,
                                     xbounds=xbounds,
                                     ybounds=ybounds))

    cleanframe_and_ticks(axes)


def add_dot_dash_plot(axes=None, xs=None, ys=None):
    """
    Add a dot-dash-plot to a matplotlib graph, as described on p. 133
    of Tufte's "The Visual Display of Quantitative Information".

    axes: axes to apply the dash-dot-plot to.  If None or unspecified,
    use the current axes.

    xs: a list of values along the x-axis to plot
    yx: a list of values along the y-axis to plot

    """
    
    if axes is None:
        axes = matplotlib.pylab.gca()

    if xs is not None:
        axes.xaxis.set_minor_locator(FixedLocator(xs))

    if ys is not None:
        axes.yaxis.set_minor_locator(FixedLocator(ys))

    cleanframe_and_ticks(axes)

