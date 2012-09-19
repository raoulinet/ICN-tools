print "> Load usefull_tools.py"

import os
import sys

color_corr = {
	"b": "blue",
	"g": "green",
	"r": "red",
	"c": "cyan",
	"m": "magenta",
	"y": "yellow",
	"w": "white",
	"k": "black"
}



default_colors = [
	"b",
	"g",
	"r",
	"c",
	"m",
	"y",
	"k"
]



web_colors = [
	'maroon',
	'red',
	'purple',
	'fuchsia',
	'green',
	'lime',
	'olive',
	'yellow',
	'navy',
	'blue',
	'teal',
	'aqua'
]



brown_colors = [
	'cornsilk',
	'blanchedalmond',
	'bisque',
	'navajowhite',
	'wheat',
	'burlywood',
	'tan',
	'rosybrown',
	'sandybrown',
	'goldenrod',
	'darkgoldenrod',
	'peru',
	'chocolate',
	'saddlebrown',
	'sienna',
	'brown',
	'maroon'
]



fancy_colors = [
	"orchid",
	"firebrick",
	"orange",
	"peru",
	"olive",
	"saddlebrown",
	"mediumseagreen",
	"darkgreen",
	"slategrey",
	"skyblue",
	"royalblue"
]



curve_line = {
	"none":"None",
	"solid": "-",
	"dash": "--",
	"dot": "--",
	"dash dot": "--",
	"dash dot dot": "--"
}



curve_marker = {
	"none": "None",
	"plus": "+",
	"cross": "x",
	"asterisk": "h",
	"circle": ",",
	"square": "s",
	"diamond": "1",
	"triangle up": "2",
	"triangle down": "3",
	"star": "4"
}


################################################################################
#                                                                              #
# Usefull tools.                                                               #
# * colorize                                                                   #
# * get_data                                                                   #
# * rotate_data( |_by_mouse)                                                   #
# * translate_data( | _by_mouse)                                               #
# * get_index_list                                                             #
# * remove_line                                                                #
#                                                                              #
################################################################################

def cf():
	"""
	cf
	"""

	return gcf()



def cAs():
	"""
	ca
	"""

	return getp(cf(), 'axes')



def cA(num = -1):
	"""
	cA
	"""

	return getp(cf(), 'axes')[num]



def ci():
	"""
	ci
	"""

	return gci()



def cl(line_number = -1):
	"""
	cl
	"""

	return gca().lines[line_number]



def cls(lower = 0, higher = None):
	"""
	cls
	"""

	if higher == None:
		higher = len(gca().lines)

	n = 0

	for i in gca().lines:
		print("# " + str(n)
		+ "\tmarker: " + str(i.get_marker())
		+ "\tline: " + str(i.get_linestyle())
		+ "\tcolor: " + str(i.get_color())
		+ "\tlen: " + str(len(i.get_xdata())))
		n += 1

	return gca().lines[lower : higher]



def ct(text_number = -1):
	"""
	ct
	"""

	return gca().texts[text_number]



def ct(text_number = -1):
	"""
	ct
	"""

	return gca().texts



def cx():
	"""
	cx
	"""
	
	return ca().xaxis



def cy():
	"""
	cy
	"""
	
	return ca().yaxis



def cT():
	"""
	cT
	"""
	
	return ca().title



def cPs():
	"""
	"""

	return filter(lambda i: type(i) == Polygon, getp(ca(), 'children'))



def cP(num = -1):
	"""
	"""

	return filter(lambda i: type(i) == Polygon, getp(ca(), 'children'))[num]



def cEs():
	"""
	"""

	return filter(lambda i: type(i) == Ellipse, getp(ca(), 'children'))



def cE(num = -1):
	"""
	"""

	return filter(lambda i: type(i) == Ellipse, getp(ca(), 'children'))[num]



def colorize(palette = "fancy", offset = 0, period = None):
	"""
	to colorize lines depdening of layers
	"""

	if type(palette) == str:
		if palette == "fancy":
			colors = fancy_colors
		else:
			if palette == "web":
				colors = web_colors
			else:
				if palette == "brown":
					colors = brown_colors
				else:
					colors = default_colors
	elif type(palette) == list:
		colors = palette
	else:
		colors = default_colors

	if period == None:
		period = len(colors)

	n = len(gca().lines)

	for i in range(n):
		tmp_col = colors[i%period + offset%(len(colors) - 1)]
		gca().lines[i].set_color(tmp_col)
		gca().lines[i].set_markerfacecolor(tmp_col)
		gca().lines[i].set_markeredgecolor(tmp_col)

	draw()



def get_data(layer = -1):
	"""
	get_data
	"""

	return gca().lines[layer].get_data()



def rotate_data(theta = 0):
	"""
	rotate_data
	"""

	for i in gca().lines:
		_x1, _y1 = i.get_data()
		i.set_xdata(cos(theta) * _x1 + sin(theta) * _y1)
		i.set_ydata(-sin(theta) * _x1 + cos(theta) * _y1)

	draw()
	


def translate_data(displacement = 0):
	"""
	translate_data
	"""

	for i in gca().lines:
		_x1, _y1 = i.get_data()
		i.set_xdata(_x1 + displacement[0])
		i.set_ydata(_y1 + displacement[1])

	draw()



def rotate_data_by_mouse():
	"""
	rotate_data_by_mouse
	"""

	_p = ginput(2, show_clicks=False)

	if len(_p) < 2:
		return

	dtheta = - arctan2(_p[1][1], _p[1][0]) + arctan2(_p[0][1], _p[0][0])
	print("dtheta: " + str(dtheta))

	for i in gca().lines:
		_x1, _y1 = i.get_data()
		i.set_xdata(cos(dtheta) * _x1 + sin(dtheta) * _y1)
		i.set_ydata(-sin(dtheta) * _x1 + cos(dtheta) * _y1)

	draw()



def translate_data_by_mouse(layer = None):
	"""
	translate_data_by_mouse	
	"""

	_p = ginput(2, show_clicks=False)

	if len(_p) < 2:
		return

	xdisplacement = _p[1][0] - _p[0][0]
	ydisplacement = _p[1][1] - _p[0][1]
	print("dx: " + str(xdisplacement), "dy :" + str(ydisplacement))

	if layer != None:
		_x1, _y1 = gca().lines[layer].get_data()
		gca().lines[layer].set_xdata(_x1 + xdisplacement)
		gca().lines[layer].set_ydata(_y1 + ydisplacement)	
	else:
		for i in gca().lines:
			_x1, _y1 = i.get_data()
			i.set_xdata(_x1 + xdisplacement)
			i.set_ydata(_y1 + ydisplacement)

	draw()



def get_index_list():
	"""
	get_index_list
	"""

	n = 0

	for i in gca().lines:
		print("# " + str(n)+ "\tmarker: " + str(i.get_marker()) + "\tline: " + str(i.get_linestyle()) + "\tcolor: " + str(i.get_color()) + "\tlen: " + str(len(i.get_xdata())))
		n += 1
	return len(gca().lines)



def slice_graph(begin = 0, num = None, step = 1):

	source = gcf()
	drop = figure()

	if num == None:
		num = len(gca().lines)

	for i in range(begin, num, step):
		x, y = source.axes[-1].lines[i].get_data()
		marker = source.axes[-1].lines[i].get_marker()
		markersize = source.axes[-1].lines[i].get_markersize()
		linestyle = source.axes[-1].lines[i].get_linestyle()
		linewidth = source.axes[-1].lines[i].get_linewidth()
		color = source.axes[-1].lines[i].get_color()
		label = source.axes[-1].lines[i].get_label()
		figure(drop.number)
		plot(x, y, marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, color=color, label=label)



def copy_paste_graph(source_fig, drop_fig):

	source = figure(source_fig)
	drop = figure(drop_fig)

	for i in range(len(source.axes[-1].lines)):
		x, y = source.axes[-1].lines[i].get_data()
		marker = source.axes[-1].lines[i].get_marker()
		markersize = source.axes[-1].lines[i].get_markersize()
		linestyle = source.axes[-1].lines[i].get_linestyle()
		linewidth = source.axes[-1].lines[i].get_linewidth()
		color = source.axes[-1].lines[i].get_color()
		label = source.axes[-1].lines[i].get_label()
		figure(drop.number)
		plot(x, y, marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, color=color, label=label)



def get_norm_angle():

    a = ginput()[0]

    return {
        "norm": sqrt(a[0]**2 + a[1]**2),
        "angle_rad": arctan2(a[1], a[0]),
        "angle_deg": arctan2(a[1], a[0])*180./pi
    }



def remove_first(layer = 0):

	gca().lines.pop(layer)
	draw()



def remove_last(layer = None):

	if layer == None:
		gca().lines.pop()
	else:
		gca().lines.pop(layer)
	draw()



def line_matrix(bottom = None, top = None, xstep = 1, ystep = 1):

    xmin = gca().lines[0].get_xdata().min()
    xmax = gca().lines[0].get_xdata().max()
    ymin = gca().lines[0].get_ydata().min()
    ymax = gca().lines[0].get_ydata().max()

    xx, yy = meshgrid(arange(xmin, xmax, xstep), arange(ymin, ymax, ystep))

    cc = 0*xx

    print("grid xx: " + str(len(xx)) + "x" + str(len(xx[0])))
    print("grid yy: " + str(len(yy)) + "x" + str(len(yy[0])))
    print("grid cc: " + str(len(cc)) + "x" + str(len(cc[0])))

    intx = range((xmax - xmin)/xstep)
    inty = range((ymax - ymin)/ystep)

    for j in intx:
	for k in inty:
		cc[k][j] = 0

    if len(gca().lines) == 1:
        offset = 1
    else:
        offset = 0

    for n in range(len(gca().lines)):
        if bottom != None:
            if n < bottom:
                n = bottom
        if top != None:
            if n > top:
                n = top
        data = gca().lines[n].get_xydata()
        for i in range(len(data)):
                j = (data[i][1] - ymin)/ystep
                k = (data[i][0] - xmin)/xstep
                # print("j, k: " + str(j) + ", " + str(k))
                try:
                    cc[round(j)][round(k)] = n + offset
                except:
                    print("oups, stopped @ " + str(i) + "/" + str(len(data)))

    return xx, yy, cc


################################################################################
#                                                                              #
# Different class of usefull graph.                                            #
# * graph(...)                                                                 #
# * (im | p)graph(...)                                                         #
#                                                                              #
################################################################################

class graph:
	"""
	Overlaod of figure() + plot() function
	a 2 in 1
	graph(...) to open and plot
	plot(...) to append a line in the graph
	"""
	
	def __init__(self, *args):
		figure()
		plot(*args)



class imgraph:
	"""
	Overlaod of figure() + imshow() function
	a 2 in 1
	imgraph(...) to open and plot
	imshow(...) to append a line in the graph
	"""

	def __init__(self, *args):
		figure()
		imshow(*args)



class pgraph:
	"""
	Overlaod of figure() + pcolor() function
	a 2 in 1
	colorgraph(...) to open and plot
	pcolor(...) to append a line in the graph
	"""

	def __init__(self, *args):
		figure()
		pcolormesh(*args)


