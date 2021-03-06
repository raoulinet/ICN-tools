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



def offset(offset):
    """
    Add an offset to curves
    """

    # Providing only one value for the offset means that
    # the same offset is applied
    if type(offset) in [int, float] :
        offset = offset * ones(len(gca().lines))

    # But for a fine tuning, a list can be given.
    # Be carefull, the list has to have the same size
    # as the gca().lines list.
    if type (offset) == list :
        if len(offset) != len (gca().lines) :
            print "The offset list has a size different of",
            "the gca().lines list"
            return

    total_offset = 0
    _min, _max = 1e31, -1e31

    for i, j in zip(gca().lines, offset) :
        y0 = i.get_ydata() + j + total_offset
        i.set_ydata(y0)
        if y0.min() < _min :
            print "min", y0.min()
            _min = y0.min()
        if y0.max() > _max :
            print "max", y0.max()
            _max = y0.max()
        total_offset = total_offset + j

    # Enlarge the ylim by 10 %
    _min = _min - 0.1 * abs(_max - _min)
    _max = _max + 0.1 * abs(_max - _min)
    ylim(_min,_max)
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



def hsplitlist (liste, slices) :
    return hsplit(array(liste), slices)



def vsplitlist (liste, slices) :
    return vsplit(array(liste), slices)


def deltaXY (timeout = 30) :
    a, b = hsplitlist (ginput (n = 2, timeout = timeout), 2)
    return a[1] - a[0], b[1] - b[0]



# Pyperclip v1.3
# A cross-platform clipboard module for Python. (only handles plain text for now)
# By Al Sweigart al@coffeeghost.net
# Usage:
#   import pyperclip
#   pyperclip.copy('The text to be copied to the clipboard.')
#   setcb("spam")
#   spam = getcb ()
# On Mac, this module makes use of the pbcopy and pbpaste commands, which should come with the os.
# On Linux, this module makes use of the xclip command, which should come with the os. Otherwise run "sudo apt-get install xclip"


import platform

def winGetClipboard():
    ctypes.windll.user32.OpenClipboard(0)
    pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 is CF_TEXT
    data = ctypes.c_char_p(pcontents).value
    #ctypes.windll.kernel32.GlobalUnlock(pcontents)
    ctypes.windll.user32.CloseClipboard()
    return data

def winSetClipboard(text):
    GMEM_DDESHARE = 0x2000
    ctypes.windll.user32.OpenClipboard(0)
    ctypes.windll.user32.EmptyClipboard()
    try:
        # works on Python 2 (bytes() only takes one argument)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text))+1)
    except TypeError:
        # works on Python 3 (bytes() requires an encoding)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text, 'ascii'))+1)
    pchData = ctypes.windll.kernel32.GlobalLock(hCd)
    try:
        # works on Python 2 (bytes() only takes one argument)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text))
    except TypeError:
        # works on Python 3 (bytes() requires an encoding)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text, 'ascii'))
    ctypes.windll.kernel32.GlobalUnlock(hCd)
    ctypes.windll.user32.SetClipboardData(1,hCd)
    ctypes.windll.user32.CloseClipboard()

def macSetClipboard(text):
    outf = os.popen('pbcopy', 'w')
    outf.write(text)
    outf.close()

def macGetClipboard():
    outf = os.popen('pbpaste', 'r')
    content = outf.read()
    outf.close()
    return content

def gtkGetClipboard():
    return gtk.Clipboard().wait_for_text()

def gtkSetClipboard(text):
    cb = gtk.Clipboard()
    cb.set_text(text)
    cb.store()

def qtGetClipboard():
    return str(cb.text())

def qtSetClipboard(text):
    cb.setText(text)

def xclipSetClipboard(text):
    outf = os.popen('xclip -selection c', 'w')
    outf.write(text)
    outf.close()

def xclipGetClipboard():
    outf = os.popen('xclip -selection c -o', 'r')
    content = outf.read()
    outf.close()
    return content

def xselSetClipboard(text):
    outf = os.popen('xsel -i', 'w')
    outf.write(text)
    outf.close()

def xselGetClipboard():
    outf = os.popen('xsel -o', 'r')
    content = outf.read()
    outf.close()
    return content

if os.name == 'nt' or platform.system() == 'Windows':
    import ctypes
    getcb = winGetClipboard
    setcb = winSetClipboard
elif os.name == 'mac' or platform.system() == 'Darwin':
    getcb = macGetClipboard
    setcb = macSetClipboard
elif os.name == 'posix' or platform.system() == 'Linux':
    xclipExists = os.system('which xclip') == 0
    if xclipExists:
        getcb = xclipGetClipboard
        setcb = xclipSetClipboard
    else:
        xselExists = os.system('which xsel') == 0
        if xselExists:
            getcb = xselGetClipboard
            setcb = xselSetClipboard
        try:
            import gtk
            getcb = gtkGetClipboard
            setcb = gtkSetClipboard
        except:
            try:
                import PyQt4.QtCore
                import PyQt4.QtGui
                app = QApplication([])
                cb = PyQt4.QtGui.QApplication.clipboard()
                getcb = qtGetClipboard
                setcb = qtSetClipboard
            except:
                raise Exception('Pyperclip requires the gtk or PyQt4 module installed, or the xclip command.')


def copy_to_clipboard (s) :
    setcb (str(s))
    print "------- getcb -------"
    print getcb()


def clicked_to_clipboard () :
    setcb(str(ginput(-1)))
    print "------- getcb -------"
    print getcb()
 

def place_text (s = None) :
    a, b = ginput(1)[0]
    if not s :
        s = raw_input("Text to place ? ")
    text (a, b, s)

    
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


