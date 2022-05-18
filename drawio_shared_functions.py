from lxml import etree
import random
import string
import drawio_tools
import xml.dom.minidom

# id generator
# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def id_generator(size=22, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '-_'):
    return ''.join(random.choice(chars) for _ in range(size))


def create_layer(name, locked=1):
    mxcell = etree.Element('mxCell')
    mxcell.set('id', id_generator())
    mxcell.set('value', name)
    mxcell.set('style', 'locked=' + str(locked))
    mxcell.set('parent', '0')
    return mxcell


def write_drawio_output(data, filename='output.drawio'):
    root = etree.Element('mxfile')
    root.set('host', 'Electron')
    root.set('modified', '2022-05-01T08:12:20.636Z')
    root.set('agent',
             '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/14.5.1 Chrome/89.0.4389.82 Electron/12.0.1 Safari/537.36')
    root.set('etag', 'LL0dNY7hwAR5jEqHpxG4')
    root.set('version', '14.5.1')
    root.set('type', 'device')

    # another child with text
    child = etree.Element('diagram')
    child.set('id', 'nMbIOyWw1tff--0FTw4Q')
    child.set('name', 'Page-1')
    child.text = data
    root.append(child)

    tree = etree.ElementTree(root)
    tree.write(filename)


def finish(mxGraphModel, filename='output.drawio'):
    data = etree.tostring(mxGraphModel, pretty_print=False)
    data = drawio_tools.encode_diagram_data(data)
    write_drawio_output(data, filename)


def pretty_print(mxGraphModel):
    dom = xml.dom.minidom.parseString(etree.tostring(mxGraphModel))
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)
