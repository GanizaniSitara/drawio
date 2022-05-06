from lxml import etree
import string
import random
import drawio_tools
import pandas as pd
import itertools as it
import math

def write_drawio_output(data):
    # create XML
    root = etree.Element('mxfile')
    root.set('host', 'Electron')
    root.set('modified', '2022-05-01T08:12:20.636Z')
    root.set('agent', '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/14.5.1 Chrome/89.0.4389.82 Electron/12.0.1 Safari/537.36')
    root.set('etag', 'LL0dNY7hwAR5jEqHpxG4')
    root.set('version', '14.5.1')
    root.set('type', 'device')

    # another child with text
    child = etree.Element('diagram')
    child.set('id','nMbIOyWw1tff--0FTw4Q')
    child.set('name','Page-1')
    child.text = data
    root.append(child)

    tree = etree.ElementTree(root)
    tree.write('output.drawio')

# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def id_generator(size=22, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '-_'):
    return ''.join(random.choice(chars) for _ in range(size))

def create_layer(name):
    mxcell = etree.Element('mxCell')
    mxcell.set('id', id_generator())
    mxcell.set('value', name)
    mxcell.set('style', 'locked=1')
    mxcell.set('parent', '0')
    return mxcell

# from number of elements return number of columns and rows needed for landscape layout
# this was generated by GitHub Copilot just from the comment above
# first error was made count 36 where 7x5 was suggested
def get_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements == 2:
        return 2, 1
    elif elements == 3:
        return 3, 1
    elif elements == 4:
        return 2, 2
    elif elements == 5:
        return 3, 2
    elif elements == 6:
        return 3, 2
    elif elements == 7:
        return 3, 3
    elif elements == 8:
        return 3, 3
    elif elements == 9:
        return 3, 3
    elif elements == 10:
        return 3, 4
    elif elements == 11:
        return 3, 4
    elif elements == 12:
        return 3, 4
    elif elements == 13:
        return 3, 5
    elif elements == 14:
        return 3, 5
    elif elements == 15:
        return 3, 5
    elif elements == 16:
        return 5, 4
    elif elements == 17:
        return 5, 4
    elif elements == 18:
        return 5, 4
    elif elements == 19:
        return 5, 4
    elif elements == 20:
        return 5, 4
    elif elements == 21:
        return 6, 4
    elif elements == 22:
        return 6, 4
    elif elements == 23:
        return 6, 4
    elif elements == 24:
        return 6, 4
    elif elements == 25:
        return 6, 5
    elif elements == 26:
        return 6, 5
    elif elements == 27:
        return 6, 5
    elif elements == 28:
        return 6, 5
    elif elements == 29:
        return 6, 5
    elif elements == 30:
        return 6, 5
    elif elements == 31:
        return 7, 5
    elif elements == 32:
        return 7, 5
    elif elements == 33:
        return 7, 5
    elif elements == 34:
        return 7, 5
    elif elements == 35:
        return 7, 5
    else:
        raise ValueError('Unsupported number of elements.')


# mxGraphModel is the true "root" of the graph
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
background.set('visible', '0')
root.append(background)


# back to front order, lowest layer first
# while building out dict of layers
layers= {}
layers['Containers'] = create_layer('Containers')
layers['Applications'] = create_layer('Applications')
layers['Strategy'] = create_layer('Strategy')
layers['Resilience'] = create_layer('Resilience')
layers['Hosting'] = create_layer('Hosting')
layers['Metrics'] = create_layer('Metrics')
layers['TransactionCycle'] = create_layer('TransactionCycle')
for layer in layers.values():
    root.append(layer)


def create_rectangle(parent, x, y, width, height, **kwargs):
    mxcell = etree.Element('mxCell')
    mxcell.set('id', id_generator())
    mxcell.set('value', kwargs['value'])
    mxcell.set('style', kwargs['style'])
    mxcell.set('parent', parent.get('id'))
    mxcell.set('vertex', '1')
    geometry = etree.Element('mxGeometry')
    geometry.set('x',str(x))
    geometry.set('y',str(y))
    geometry.set('width',str(width))
    geometry.set('height',str(height))
    geometry.set('as','geometry')
    mxcell.append(geometry)
    return mxcell


class Application:
    height = 80
    width = 160

    def __init__(self, name, **kwargs):
        self.name = name
        self.x = 0
        self.y = 0
        self.kwargs = kwargs
        self.style = ''
        #self.mxcell = create_rectangle(layers['Applications'], self.x, self.y, self.width, self.height, **self.kwargs)

    # TC,StatusRAG,Status,HostingPercent,HostingPattern1,HostingPattern2,Arrow1,Arrow

    def get_style_for_hosting_pattern(self, hosting_pattern):
        if hosting_pattern == 'Azure':
            style='verticalLabelPosition=bottom;html=1;verticalAlign=top;align=center;strokeColor=none;fillColor=#00BEF2;shape=mxgraph.azure.azure_instance;fontFamily=Expert Sans Regular;aspect=fixed;'
        elif hosting_pattern == 'AWS':
            style='dashed=0;outlineConnect=0;html=1;align=center;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;shape=mxgraph.webicons.amazon;gradientColor=#DFDEDE;strokeColor=#FFFFFF;strokeWidth=1;fontFamily=Expert Sans Regular;aspect=fixed;'
        elif hosting_pattern == 'Linux':
            style="pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#DF8C42;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;shape=mxgraph.veeam2.linux;fontFamily=Expert Sans Regular;aspect=fixed;"
        elif hosting_pattern == 'Windows':
            style="shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#EF8F21;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;shape=mxgraph.veeam.ms_windows;fontFamily=Expert Sans Regular;"
        elif hosting_pattern == 'OpenShift':
            style="aspect=fixed;html=1;points=[];align=center;image;fontSize=12;image=img/lib/mscae/OpenShift.svg;strokeColor=#FFFFFF;strokeWidth=1;fillColor=#333333;"
        elif hosting_pattern == 'WindowsVM':
            style="shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#4495D1;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;shape=mxgraph.veeam.vm_windows;fontFamily=Expert Sans Regular;aspect=fixed;"
        return style


    def appender(self, root):
        # Base app rectangle
        container = create_rectangle(parent=layers['Applications'], value=self.name,
                                      style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=10;arcSize=4;',
                                      x=self.x, y=self.y, width=self.width, height=self.height)
        root.append(container)

        # StatusRAG - colour of the shole application on the Strategy layer
        if self.kwargs['StatusRAG'] == 'red':
            self.style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=11;arcSize=4;fillColor=#F8CECC;strokeColor=#b85450;'
        elif self.kwargs['StatusRAG'] == 'amber':
            self.style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=11;arcSize=4;fillColor=#fff2cc;strokeColor=#d6b656;'
        elif self.kwargs['StatusRAG'] == 'green':
            self.style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=11;arcSize=4;fillColor=#D5E8D4;strokeColor=#82b366;'
        container = create_rectangle(parent=layers['Strategy'], value=self.name,
                                     style=self.style,
                                     x=self.x, y=self.y, width=self.width, height=self.height)
        root.append(container)

        # Resilience - colour of the resilience indicator
        if self.kwargs['Status'] == 'red':
            self.style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=11;arcSize=4;fillColor=#b1ddf0;strokeColor=#10739e;'
        elif self.kwargs['Status'] == 'amber':
            self.style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=11;arcSize=4;fillColor=#f9f7ed;strokeColor=#36393d;'
        elif self.kwargs['Status'] == 'green':
            self.style = 'rounded=1;whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=14;fontStyle=0;verticalAlign=top;spacing=11;arcSize=4;fillColor=#dae8fc;strokeColor=#6c8ebf;'
        container = create_rectangle(parent=layers['Resilience'], value=self.name,
                                     style=self.style,
                                     x=self.x, y=self.y, width=self.width, height=self.height)
        root.append(container)

        # TC - TC indicator
        container = create_rectangle(parent=layers['TransactionCycle'], value=str(self.kwargs['TC']),
                                     style = 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=none;fontFamily=Helvetica;fontStyle=1;fontSize=14;fontColor=#333333;',
                                     x=self.x + 1, y=self.y + 1, width=30, height=20)
        root.append(container)

        # Harvey - Harvey ball
        angle = self.kwargs['HostingPercent']/100
        if angle == 1:
            container = create_rectangle(parent=layers['Hosting'], value='',
                                         style = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeColor=none;fillColor=#333333;',
                                         x=self.x + 5, y=self.y + 52, width=25, height=25)
            root.append(container)
        elif angle != 0:
            container = create_rectangle(parent=layers['Hosting'], value='',
                                         style = 'verticalLabelPosition=bottom;verticalAlign=top;html=1;shape=mxgraph.basic.pie;startAngle=' + str(1-angle) +';endAngle=1;strokeWidth=5;strokeColor=none;aspect=fixed;direction=east;fillColor=#333333;',
                                         x=self.x + 5, y=self.y + 52, width=25, height=25)
            root.append(container)


        # HostingPattern1
        container = create_rectangle(parent=layers['Hosting'], value='',
                                     style = self.get_style_for_hosting_pattern(self.kwargs['HostingPattern1']),
                                     x=self.x + 40, y=self.y + 52, width=25, height=25)
        root.append(container)

        #Hosting Pattern2
        container = create_rectangle(parent=layers['Hosting'], value='',
                                     style = self.get_style_for_hosting_pattern(self.kwargs['HostingPattern2']),
                                     x=self.x + 68, y=self.y + 52, width=25, height=25)
        root.append(container)

        #Arrow1
        container = create_rectangle(parent=layers['Metrics'], value='',
                                    style= "html=1;shadow=0;dashed=0;align=center;verticalAlign=middle;shape=mxgraph.arrows2.arrow;dy=0.5;dx=13.86;direction=" + ("north" if self.kwargs['Arrow1'] == 'up' else "south") + ";notch=0;strokeColor=#FFFFFF;strokeWidth=1;fillColor=#333333;fontFamily=Expert Sans Regular;",
                                    x=self.x + 103, y=self.y + 52, width=25, height=25)
        root.append(container)

        #Arrow2
        container = create_rectangle(parent=layers['Metrics'], value='',
                                    style= "html=1;shadow=0;dashed=0;align=center;verticalAlign=middle;shape=mxgraph.arrows2.arrow;dy=0.5;dx=13.86;direction=" + ("north" if self.kwargs['Arrow2'] == 'up' else "south") + ";notch=0;strokeColor=#FFFFFF;strokeWidth=1;fillColor=#333333;fontFamily=Expert Sans Regular;",
                                    x=self.x + 130, y=self.y + 52, width=25, height=25)
        root.append(container)

        # Metric
        (self.x + self.y)
        container = create_rectangle(parent=layers['Metrics'], value='',
                                     style= "html=1;shadow=0;dashed=0;align=center;verticalAlign=middle;shape=mxgraph.arrows2.arrow;dy=0.5;dx=13.86;direction=" + ("north" if self.kwargs['Arrow2'] == 'up' else "south") + ";notch=0;strokeColor=#FFFFFF;strokeWidth=1;fillColor=#333333;fontFamily=Expert Sans Regular;",
                                     x=self.x + 130, y=self.y + 52, width=25, height=25)
        root.append(container)

        # Incident
        #style="rounded=1;whiteSpace=wrap;html=1;strokeWidth=1;strokeColor=none;fontFamily=Expert Sans Regular;spacing=0;verticalAlign=top;fillColor=#4CAF50;"
        #style="rounded=1;whiteSpace=wrap;html=1;strokeWidth=1;strokeColor=none;fontFamily=Expert Sans Regular;spacing=0;verticalAlign=top;fillColor=#FFC107;"
        #style="rounded=1;whiteSpace=wrap;html=1;strokeWidth=1;strokeColor=none;fontFamily=Expert Sans Regular;spacing=0;verticalAlign=top;fillColor=#F44336;"




class Level2:
    def __init__(self, name):
        self.name = name
        self.applications = []
        self.grid_y = 0
        self.grid_x = 0
        self.vertical_spacing = 10
        self.horizontal_spacing = 10
        self.vertical_elements = 0
        self.horizontal_elements = 0

    # def grid_total(self):
    #     return self.vertical * self.horizontal

    def height(self):
        self.vertical_elements, self.horizontal_elements = get_layout_size(len(self.applications))
        ret_val = 70 # header and footer text
        ret_val += self.vertical_elements * Application.height + (self.vertical_elements - 1) * self.vertical_spacing
        return ret_val

    def width(self):
        self.vertical_elements, self.horizontal_elements = get_layout_size(len(self.applications))
        ret_val = 20 # borders
        ret_val += self.horizontal_elements * Application.width + (self.horizontal_elements - 1) * self.horizontal_spacing
        return ret_val

    def __str__(self):
        return 'Level2: %s %s %s %s' % (self.level1, self.level2, self.height, self.width)

    def placements(self):
        return list(it.product(range(self.horizontal_elements),range(self.vertical_elements)))

class Level1:
    def __init__(self, name):
        self.name = name
        self.level2s = []
        self.grid_y = 0
        self.grid_x = 0

    # def number_of_elements(self):
    #     return self.vertical * self.horizontal

    def height(self):
        # Copilot
        ret_val = 70 # header
        ret_val += max(level2.height() for level2 in self.level2s) + 10
        return ret_val

    def width(self):
        # Copilot
        ret_val = 10 # borders
        for level2 in self.level2s:
            ret_val += level2.width() + 10
        return ret_val

    def __str__(self):
        return 'Leve1: %s %s %s %s' % (self.name, self.vertical, self.horizontal)


def finish(mxGraphModel):
    data = etree.tostring(mxGraphModel, pretty_print=False)
    data = drawio.encode_diagram_data(data)
    # c:\Solutions\Tutorial\output.drawio
    write_drawio_output(data)

    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(etree.tostring(mxGraphModel))
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)




df = pd.read_csv('Application_Diagram_Builder.csv')

# build the structure
level1s = []
for index, app in df.iterrows():
    L1 = next((x for x in level1s if x.name == app['Level1']), None)

    if not L1:
        L1 = Level1(app['Level1'])
        level1s.append(L1)


    L2 = next((x for x in L1.level2s if x.name == app['Level2']), None)

    if not L2:
        L2 = Level2(app['Level2'])
        L1.level2s.append(L2)

    L2.applications.append(Application(app['AppName'],TC=app['TC'],StatusRAG=app['StatusRAG'],Status=app['Status']
                                       ,HostingPercent=app['HostingPercent'],HostingPattern1=app['HostingPattern1'],
                                       HostingPattern2=app['HostingPattern2'],Arrow1=app['Arrow1'],Arrow2=app['Arrow2']))




# iterate over the structure and create the mxcells
MAX_PAGE_WIDTH = 1600
L1_x_cursor = 0
L1_y_cursor = 0
for level1 in level1s:
    if L1_x_cursor + level1.width() > MAX_PAGE_WIDTH:
        L1_x_cursor = 0
        L1_y_cursor += level1.height() + 10

    level1.grid_y = L1_y_cursor
    level1.grid_x = L1_x_cursor

    # Level1
    container = create_rectangle(parent=layers['Containers'], value=level1.name,
                                 style = ';whiteSpace=wrap;html=1;fontFamily=Expert Sans Regular;fontSize=36;fontColor=#333333;strokeColor=none;fillColor=#D6D6D6;verticalAlign=top;spacing=10;fontStyle=0',
                                 x=level1.grid_x, y=level1.grid_y, width=level1.width(), height=level1.height())
    root.append(container)

    # Level2
    L2_x_cursor = L1_x_cursor + 10
    L2_y_cursor = L1_y_cursor + 70
    for level2 in level1.level2s:
        container = create_rectangle(parent=layers['Containers'],
                                     value=level2.name,
                                     style = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=none;verticalAlign=bottom;spacing=10;fontStyle=0;fontSize=24;fontFamily=Expert Sans Regular;',
                                     x=L2_x_cursor, y=L2_y_cursor, width=level2.width(), height=level2.height())
        root.append(container)

        # Applications
        for i, app in enumerate(level2.applications):
            app.x = L2_x_cursor + 10 + level2.placements()[i][0] * (Application.width + 10)
            app.y = L2_y_cursor + 10 + level2.placements()[i][1] * (Application.height + 10)
            app.appender(root)

        L2_x_cursor += level2.width() + 10

    L1_x_cursor += level1.width() + 10

finish(mxGraphModel)


exit(-1)







