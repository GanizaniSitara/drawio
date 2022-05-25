from io import StringIO

from lxml import etree
import xml.dom.minidom
import drawio_tools
import drawio_shared_functions
import csv
import pandas as pd
import sys
import os
import random
import string


# load file from disk then convert to xml
def get_drawio_from_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    dom = xml.dom.minidom.parseString(data)
    node = dom.getElementsByTagName('diagram')
    print(node[0].firstChild.nodeValue)
    return str(node[0].firstChild.nodeValue)

def get_drawio_inner_xml(filename):
    encoded = get_drawio_from_file(filename)
    decoded = drawio_tools.decode_diagram_data(encoded)
    dom = xml.dom.minidom.parseString(decoded)
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)

# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def id_generator(size=22, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '-_'):
    return ''.join(random.choice(chars) for _ in range(size))

def create_rectangle(parent, x, y, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator())
        mxcell.set('value', kwargs['value'])
        mxcell.set('style', kwargs['style'])
        mxcell.set('parent', parent)
        mxcell.set('vertex', '1')
        geometry = etree.Element('mxGeometry')
        geometry.set('x', str(x))
        geometry.set('y', str(y))
        geometry.set('width', str(width))
        geometry.set('height', str(height))
        geometry.set('as', 'geometry')
        mxcell.append(geometry)
        return mxcell
    except Exception as e:
        print(e)
        print(kwargs)
        RuntimeError('create_rectangle failed')

def create_tube(parent, x1, y1, x2, y2, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator())
        if 'name' in kwargs:
            mxcell.set('value', kwargs['name'])
        mxcell.set('style', kwargs['style'])
        mxcell.set('parent', parent)
        mxcell.set('edge', '1')
        mxGeometry = etree.Element('mxGeometry')
        mxGeometry.set('width', str(width))
        mxGeometry.set('height', str(height))
        mxGeometry.set('relative', '1')
        mxGeometry.set('as', 'geometry')
        mxSourcePoint = etree.Element('mxPoint')
        mxSourcePoint.set('x', str(x1))
        mxSourcePoint.set('y', str(y1))
        mxSourcePoint.set('as', 'sourcePoint')
        mxTargetPoint = etree.Element('mxPoint')
        mxTargetPoint.set('x', str(x2))
        mxTargetPoint.set('y', str(y2))
        mxTargetPoint.set('as', 'targetPoint')
        mxGeometry.append(mxSourcePoint)
        mxGeometry.append(mxTargetPoint)
        mxcell.append(mxGeometry)
        return mxcell
    except Exception as e:
        print(e)
        print(kwargs)
        RuntimeError('create_tube failed')

def append_grid(root):
    grid = """
    <root>
        <mxCell id="I92-6_ahHXa4w7bkStNk-1" value="" style="endArrow=none;html=1;" edge="1" parent="1">
			<mxGeometry width="50" height="50" relative="1" as="geometry">
				<mxPoint x="480" y="520" as="sourcePoint"/>
				<mxPoint x="480" y="-40" as="targetPoint"/>
			</mxGeometry>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-2" value="" style="endArrow=none;html=1;" edge="1" parent="1">
			<mxGeometry width="50" height="50" relative="1" as="geometry">
				<mxPoint x="720" y="520" as="sourcePoint"/>
				<mxPoint x="720" y="-40" as="targetPoint"/>
			</mxGeometry>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-3" value="" style="endArrow=none;html=1;" edge="1" parent="1">
			<mxGeometry width="50" height="50" relative="1" as="geometry">
				<mxPoint x="960" y="520" as="sourcePoint"/>
				<mxPoint x="960" y="-40" as="targetPoint"/>
			</mxGeometry>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-4" value="" style="endArrow=none;html=1;" edge="1" parent="1">
			<mxGeometry width="50" height="50" relative="1" as="geometry">
				<mxPoint x="1200" y="520" as="sourcePoint"/>
				<mxPoint x="1200" y="-40" as="targetPoint"/>
			</mxGeometry>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-5" value="" style="endArrow=none;html=1;" edge="1" parent="1">
			<mxGeometry width="50" height="50" relative="1" as="geometry">
				<mxPoint x="240" y="520" as="sourcePoint"/>
				<mxPoint x="240" y="-40" as="targetPoint"/>
			</mxGeometry>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-7" value="2022" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#ffffff;fontFamily=Verdana;fontSize=16;fontStyle=1" vertex="1" parent="1">
			<mxGeometry x="480" y="-40" width="240" height="40" as="geometry"/>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-9" value="2023" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#ffffff;fontFamily=Verdana;fontSize=16;fontStyle=1" vertex="1" parent="1">
			<mxGeometry x="720" y="-40" width="240" height="40" as="geometry"/>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-10" value="2024" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#ffffff;fontFamily=Verdana;fontSize=16;fontStyle=1" vertex="1" parent="1">
			<mxGeometry x="960" y="-40" width="240" height="40" as="geometry"/>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-11" value="2025" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#ffffff;fontFamily=Verdana;fontSize=16;fontStyle=1" vertex="1" parent="1">
			<mxGeometry x="1200" y="-40" width="240" height="40" as="geometry"/>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-12" value="Capability Focus" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#ffffff;fontFamily=Verdana;fontSize=16;fontStyle=1" vertex="1" parent="1">
			<mxGeometry x="240" y="-40" width="240" height="40" as="geometry"/>
		</mxCell>
		<mxCell id="I92-6_ahHXa4w7bkStNk-13" value="" style="endArrow=none;html=1;exitX=1;exitY=1;exitDx=0;exitDy=0;" edge="1" parent="1" source="I92-6_ahHXa4w7bkStNk-11">
			<mxGeometry width="50" height="50" relative="1" as="geometry">
				<mxPoint x="250" y="530" as="sourcePoint"/>
				<mxPoint as="targetPoint"/>
			</mxGeometry>
		</mxCell>
	</root>
    """
    new_tree=etree.fromstring(grid)
    cells = new_tree.findall('mxCell')
    for cell in cells:
        root.append(cell)

def create_angled_tube(parent, x1, y1, x2, y2, width, height, **kwargs):
    # based on x and y distance work out points array for angled tube

    # the further away from the origin the smaller the angle
    angle = (x2-x1)/(y2-y1)

    if not 'points_array' in kwargs:
        kwargs['points_array'] = []
        # kwargs['points_array'].append((x2 - 100, y1))
        # coef = 1/(1+abs(y1-y2)/(y1+y2))**2
        # print(coef)
        # kwargs['points_array'].append((x2 - 100*(abs(y1-y2)/(y1+y2)), y2+(y1-y2)*0.75))
        # kwargs['points_array'].append((x2,y2+(y1-y2)*0.5))
        kwargs['points_array'].append(((x2-(abs(y1-y2)*0.5)), y1))
    print(kwargs['points_array'])

    mxcell = etree.Element('mxCell')
    mxcell.set('id', drawio_shared_functions.id_generator())
    if 'name' in kwargs:
        mxcell.set('value', kwargs['name'])
    mxcell.set('style', kwargs['style'])
    mxcell.set('parent', parent.get('id'))
    mxcell.set('edge', '1')

    mxGeometry = etree.Element('mxGeometry')
    mxGeometry.set('width', str(width))
    mxGeometry.set('height', str(height))
    mxGeometry.set('relative', '1')
    mxGeometry.set('as', 'geometry')
    mxcell.append(mxGeometry)

    mxSourcePoint = etree.Element('mxPoint')
    mxSourcePoint.set('x', str(x1))
    mxSourcePoint.set('y', str(y1))
    mxSourcePoint.set('as', 'sourcePoint')
    mxGeometry.append(mxSourcePoint)

    mxTargetPoint = etree.Element('mxPoint')
    mxTargetPoint.set('x', str(x2))
    mxTargetPoint.set('y', str(y2))
    mxTargetPoint.set('as', 'targetPoint')
    mxGeometry.append(mxTargetPoint)

    mxArray = etree.Element('Array')
    mxArray.set('as', 'points')
    for point in kwargs['points_array']:
        mxPoint = etree.Element('mxPoint')
        mxPoint.set('x', str(point[0]))
        mxPoint.set('y', str(point[1]))
        mxArray.append(mxPoint)
        mxGeometry.append(mxArray)

    return mxcell

def create_station(parent, x, y, width, height, **kwargs):
    mxcell = etree.Element('mxCell')
    mxcell.set('id', drawio_shared_functions.id_generator())
    if kwargs.get('value'):
         mxcell.set('value', kwargs['value'])
    mxcell.set('style', kwargs['style'])
    mxcell.set('vertex', '1')
    mxcell.set('parent', parent)
    mxGeometry = etree.Element('mxGeometry')
    mxGeometry.set('x', str(x+width/2)) #
    mxGeometry.set('y', str(y+height/2))
    mxGeometry.set('width', str(width))
    mxGeometry.set('height', str(height))
    mxGeometry.set('as', 'geometry')
    mxcell.append(mxGeometry)
    return mxcell


class TubeLine:
    def __init__(self, name, x1, y1, x2, y2, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['name'] = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height
        self.kwargs['merge_flag'] = False
        if not 'style' in self.kwargs:
            # assume straight tube
            self.kwargs['style'] = 'endArrow=block;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=entityRelationEdgeStyle;strokeWidth=8;strokeColor=#EA6B66;endFill=0;flowAnimation=0;'
        if y1 != y2:
            # we're angled!
            self.kwargs['merge_flag'] = True
            self.kwargs['style']='endArrow=none;html=1;strokeColor=#FF0080;strokeWidth=8;fontFamily=Expert Sans Regular;flowAnimation=0;'
        print("TubeLine:", self.kwargs)


    def appender(self, root):
        if not self.kwargs['merge_flag']:
            container = create_tube(layer_id(root, 'Tubes'), self.x1, self.y1, self.x2, self.y2, self.width, self.height, **self.kwargs)
        else:
            container = create_angled_tube(layer_id(root, 'Tubes'), self.x1, self.y1, self.x2, self.y2, self.width, self.height, **self.kwargs)
            # if we're angling then we're merging and need a station
            #stations.add_station(self.x1, self.y1, 20, 20, style='ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=5;')
        root.append(container)


class Label:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = 'text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;;labelBackgroundColor=#ffffff'
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    def appender(self, root):
        container = create_rectangle(layer_id(root, 'Labels'), self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)

class Station:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs['style'] = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=5;fontFamily=Verdana;labelPosition=right;verticalLabelPosition=top;align=left;verticalAlign=bottom;fontSize=10;labelBackgroundColor=#ffffff;'
        self.kwargs['width'] = 20
        self.kwargs['height'] = 20

    def appender(self, root):
        container = create_station(layer_id(root, 'Stations'), **self.kwargs)
        root.append(container)


def get_diagram_root():
    mxGraphModel = etree.Element('mxGraphModel')
    mxGraphModel.set('dx', '981')
    mxGraphModel.set('dy', '650')
    mxGraphModel.set('grid', '1')
    mxGraphModel.set('gridSize', '10')
    mxGraphModel.set('guides', '1')
    mxGraphModel.set('tooltips', '1')
    mxGraphModel.set('connect', '1')
    mxGraphModel.set('arrows', '1')
    mxGraphModel.set('fold', '1')
    mxGraphModel.set('page', '1')
    mxGraphModel.set('pageScale', '1')
    mxGraphModel.set('pageWidth', '816')
    mxGraphModel.set('pageHeight', '1056')
    mxGraphModel.set('math', '0')
    mxGraphModel.set('shadow', '0')
    root = etree.Element('root')
    mxGraphModel.append(root)
    # top cell always there, layers inherit from it
    mxcell = etree.Element('mxCell')
    mxcell.set('id', '0')
    root.append(mxcell)
    # background layer, always there, we don't draw on it
    background = etree.Element('mxCell')
    background.set('id', '1')
    background.set('style', 'locked=1')
    background.set('parent', '0')
    background.set('visible', '1')
    root.append(background)
    return mxGraphModel


def layer_id(root, name):
    for node in root.findall('.//mxCell[@parent="0"][@value="' + name + '"]'):
        return node.get('id')


def create_layer(name):
    mxcell = etree.Element('mxCell')
    mxcell.set('id', drawio_shared_functions.id_generator())
    mxcell.set('value', name)
    mxcell.set('style', 'locked=0')
    mxcell.set('parent', '0')
    return mxcell


def append_layers(root):
    # back to front order, lowest layer first
    layers = {}
    layers['Tubes'] = create_layer('Tubes')
    layers['Labels'] = create_layer('Labels')
    layers['Stations'] = create_layer('Stations')
    for layer in layers.values():
        root.append(layer)
    return root


def __main__(file):
    mxGraphModel = get_diagram_root()
    root = mxGraphModel.find("root")
    append_layers(root)

    try:
        df = pd.read_csv(file, quoting=csv.QUOTE_ALL, delim_whitespace=False)
    except Exception as e:
        print(e)
        print(f"Issue reading:{file}")
        return

    print(df)

    # create one tube
    # tube = create_tube(layers['Tubes'], x1=520, y1=360, x2=680, y2=360, width=50, height=50,
    #             # name='straight tube',
    #             style='endArrow=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=entityRelationEdgeStyle;strokeWidth=8;strokeColor=#EA6B66;endFill=0;flowAnimation=0;')
    # root.append(tube)

    # angled_tube = create_angled_tube(layers['Tubes'], x1=520, y1=400, x2=827, y2=480, points_array=[(747, 400), (797, 430)], width=50, height=50,
    #                     name='angled tube',
    #                     style='endArrow=none;html=1;strokeColor=#FF0080;strokeWidth=8;fontFamily=Expert Sans Regular;flowAnimation=0;')
    # root.append(angled_tube)

    # create one station
    # station = create_station(layers['Stations'], x=520, y=100, width=20, height=20,
    #                          style='ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=5;')
    # root.append(station)


    YEARS = [str(x) for x in range(2022, 2025)]
    YEAR_LENGTH = 240                                   # make is divisible by 40
    DIAGRAM_LENGTH= YEAR_LENGTH * len(YEARS)
    QUARTER_LENGTH = YEAR_LENGTH / 4
    LINE_HEIGHT = 80

    append_grid(root)

    # build out the diagram logic
    for index, app in df.iterrows():
        xy_cursor = (0,  (index + 1) * LINE_HEIGHT)

        # use YEAR_LENGTH as a label width for line labels
        label = Label(app['Application'], x=xy_cursor[0], y=xy_cursor[1] - LINE_HEIGHT/2, width=YEAR_LENGTH, height=LINE_HEIGHT)
        label.appender(root)
        label = Label(app['Description'], x=xy_cursor[0] + YEAR_LENGTH, y=xy_cursor[1] - LINE_HEIGHT/2, width=YEAR_LENGTH, height=LINE_HEIGHT)
        label.appender(root)

        xy_cursor = (xy_cursor[0] + 2*YEAR_LENGTH + 40, xy_cursor[1])

        # find if we have a merge point
        merge_to_index =df.index[df['Application']==app['MergeTo']].tolist()
        print(f"merge_to_index:{merge_to_index}")
        if not merge_to_index:
            end_point = (DIAGRAM_LENGTH, (index + 1) * LINE_HEIGHT)
        else:
            end_point = (app['MergeWhen'] * 100 , (merge_to_index[0] + 1) * LINE_HEIGHT) #!!! some magic numbers here, probably to do with years and merges

        line = TubeLine(name="", x1=xy_cursor[0], y1=xy_cursor[1],
                        x2=end_point[0] + YEAR_LENGTH * len(YEARS), y2=end_point[1], width=50, height=50)
        line.appender(root)

        # add the stations
        if app['Station1']:
            station = Station(value=app['Station1Desc'],
                              x=xy_cursor[0] + int(app['Station1']) * 20,
                              y=xy_cursor[1] - LINE_HEIGHT/2 + 20)
            station.appender(root)

        if app['Station2']:
            station = Station(value=app['Station2Desc'],
                              x=xy_cursor[0] + int(app['Station2']) * 20,
                              y=xy_cursor[1] - LINE_HEIGHT/2 + 20)
            station.appender(root)

        if app['Station3']:
            station = Station(value=app['Station3Desc'],
                              x=xy_cursor[0] + int(app['Station3']) * 20,
                              y=xy_cursor[1] - LINE_HEIGHT/2 + 20)
            station.appender(root)

        if app['Station4']:
            station = Station(value=app['Station4Desc'],
                              x=xy_cursor[0] + int(app['Station4']) * 20,
                              y=xy_cursor[1] - LINE_HEIGHT/2 + 20)
            station.appender(root)

    drawio_shared_functions.pretty_print(mxGraphModel)
    drawio_shared_functions.finish(mxGraphModel)

    os.system('"C:\Program Files\draw.io\draw.io.exe" output.drawio')


# # helps to check if we're running in PyCharm debugger
# gettrace = getattr(sys, 'gettrace', None)
#
# if sys.stdin and sys.stdin.isatty():
#     # running interactively
#     print("Running interactively")
#     __main__(sys.argv[1])
# elif gettrace():
#       print("Running in debugger")
__main__(sys.argv[1])
# else:
#     print("Running as import")
#
# # this is for troubleshooting and comparison, new features
# # get_drawio_inner_xml('C:\\Documents\\2022-05\\flow.drawio')
#
# os.system('"C:\Program Files\draw.io\draw.io.exe" output.drawio')
