from lxml import etree
import xml.dom.minidom
import drawio_tools
import drawio_shared_functions
import os
import random
import string


import data


# function to converts 0xXXXXXX hexadecimal number to rgb string leading with hash
# https://coolors.co/palette/ef476f-ffd166-06d6a0-118ab2-073b4c
# https://coolors.co/palette/264653-2a9d8f-e9c46a-f4a261-e76f51
# https://coolors.co/palette/004777-a30000-ff7700-efd28d-00afb5

palette = [0x2E5EAA, 0x2A9D8F, 0xE9C46A, 0xEB9A57, 0xE76F51, 0xAAFAC8, 0xE3FFB6, 0x739E82, 0xA3B9C9]
palette_lighter = [x + 0x080808 for x in palette]
palette_ligthtest = [x + 0x0f0f0f for x in palette]
palette_road = [x + 0x142020 for x in palette]


def webcol(color):
    return f"#{color:x}"

def main():
    # draw_architecture_v1()
    draw_architecture_v2()
    # draw_architecture_v3()

def draw_architecture_v3():
    mxGraphModel = get_diagram_root()
    root = mxGraphModel.find("root")
    append_layers(root)

    UNIT_SIZE = 40

    prev_cuboid_bottom_left_x = None
    prev_cuboid_bottom_left_y = None

    OFFSET = 20

    x, y = 0, 0

    placement_order = 0

    df1_grouped = data.df.groupby(['class'])
    # keys = groups.groups.keys()

    class_color_index = 0
    previous_group_width = 0

    for group_name, df_group in df1_grouped:
        class_name = group_name

        # Need these here so we can place Front Roads
        color_top = None  # of the last cuboid in group
        depth = None  # of the last cuboid in group
        height = None  # of the last cuboid in group

        road_length_counter = 0
        block_counter = 0

        color_top = webcol(palette_ligthtest[class_color_index % len(palette_ligthtest)])
        print(f"{class_name} {color_top}")
        color_side = webcol(palette_lighter[class_color_index % len(palette_lighter)])
        color_front = webcol(palette[class_color_index % len(palette)])
        color_road = webcol(palette_road[class_color_index % len(palette_road)])

        # work out max height for a group
        group_max_depth, group_width = 0, 0
        for index, row in df_group.iterrows():
            if row['cost'] * UNIT_SIZE > group_max_depth:
                group_max_depth = row['cost'] * UNIT_SIZE
            group_width += row['infra'] * UNIT_SIZE + OFFSET
        print(f"{class_name} max depth {group_max_depth}")
        group_max_depth += (OFFSET * 3)

        if class_color_index != 0:
            y += group_max_depth / 2
        x += previous_group_width / 2
        previous_group_width = 0

        prev_cuboid_bottom_left_x = None
        prev_cuboid_bottom_left_y = None

        for row_index, row in df_group.iterrows():
            system_name = row['name']
            system_infra_size = row['infra']
            system_cost = row['cost']
            system_rescat = row['rescat']
            system_infra_cost = row['infra_cost']
            print('{} {} {} {} {}'.format(class_name, system_name, system_infra_size, system_cost, system_rescat))

            width = system_infra_size * UNIT_SIZE
            height = system_rescat * UNIT_SIZE
            depth = system_cost * UNIT_SIZE
            infra_cost = system_infra_cost * UNIT_SIZE

            cuboid = drawio_cuboid_stencil_xml(width, height, depth, f"{system_name} {placement_order}",
                                               infra_cost=infra_cost,
                                               color_top=color_top,
                                               color_side=color_side, color_front=color_front)
            placement_order += 1

            # first element placement at 0, 0
            if not prev_cuboid_bottom_left_x:
                rectangle = create_rectangle(layer_id(root, 'Buildings'), x, y, width=width + depth,
                                             height=height + depth / 2 + width / 2, value="", style=cuboid)
                root.append(rectangle)


            else:
                x = prev_cuboid_bottom_left_x - depth - width
                y = prev_cuboid_bottom_left_y - (height + depth / 2)

                rectangle = create_rectangle(layer_id(root, 'Buildings'), x, y, width=width + depth,
                                             height=height + depth / 2 + width / 2, value="", style=cuboid)
                root.append(rectangle)

            road_length_counter += width
            block_counter += 1
            prev_cuboid_bottom_left_x = x + depth - OFFSET
            prev_cuboid_bottom_left_y = y + height + (depth + width) / 2 + OFFSET / 2

        front_road = drawio_road_stencil_xml(road_length_counter + block_counter * OFFSET - OFFSET, 40,
                                             f"{road_length_counter + block_counter * OFFSET + OFFSET}",
                                             color_top=color_road)
        rectangle = create_rectangle(layer_id(root, 'Roads'),
                                     prev_cuboid_bottom_left_x + 60,  # one unit in front
                                     prev_cuboid_bottom_left_y - (
                                                 road_length_counter + block_counter * OFFSET) / 2 + 10,
                                     width=road_length_counter + block_counter * OFFSET + OFFSET,
                                     height=(40 + road_length_counter + block_counter * OFFSET + OFFSET) / 2,
                                     value="",
                                     style=front_road)
        root.append(rectangle)

        # front_road = drawio_road_stencil_xml(road_length_counter, 40, "", color_top=color_top)
        # rectangle = create_rectangle(layer_id(root, 'Roads'),
        #                              prev_cuboid_bottom_left_x + OFFSET - depth, # one unit in front
        #                              prev_cuboid_bottom_left_y - road_length_counter / 2 + 10,
        #                              width=road_length_counter + depth,
        #                              height= 40 / 2 + road_length_counter / 2, value="", style=front_road)
        # root.append(rectangle)

        class_color_index += 1

        for index, row in df_group.iterrows():
            previous_group_width += row['infra'] * UNIT_SIZE + OFFSET

    # save xml to file
    # drawio_shared_functions.pretty_print(mxGraphModel)
    drawio_shared_functions.finish(mxGraphModel)
    os.system('"C:\Program Files\draw.io\draw.io.exe" output.drawio')


def draw_architecture_v2():
    mxGraphModel = get_diagram_root()
    root = mxGraphModel.find("root")
    append_layers(root)

    UNIT_SIZE = 40

    prev_cuboid_bottom_left_x = None
    prev_cuboid_bottom_left_y = None

    OFFSET = 20

    x, y = 0, 0

    placement_order = 0

    df1_grouped = data.df.groupby(['class'])
    #keys = groups.groups.keys()

    class_color_index = 0
    for group_name, df_group in df1_grouped:
        class_name = group_name

        # Need these here so we can place Front Roads
        color_top = None # of the last cuboid in group
        depth = None # of the last cuboid in group
        height = None # of the last cuboid in group

        road_length_counter = 0
        block_counter = 0

        color_top = webcol(palette_ligthtest[class_color_index % len(palette_ligthtest)])
        print(f"{class_name} {color_top}")
        color_side = webcol(palette_lighter[class_color_index % len(palette_lighter)])
        color_front = webcol(palette[class_color_index % len(palette)])
        color_road = webcol(palette_road[class_color_index % len(palette_road)])
        print(color_road)

        for row_index, row in df_group.iterrows():
            system_name = row['name']
            system_infra_size = row['infra']
            system_cost = row['cost']
            system_rescat = row['rescat']
            system_infra_cost = row['infra_cost']
            print('{} {} {} {} {}'.format(class_name, system_name, system_infra_size, system_cost, system_rescat))

            width = system_infra_size * UNIT_SIZE
            height = system_rescat * UNIT_SIZE
            depth = system_cost * UNIT_SIZE
            infra_cost = system_infra_cost * UNIT_SIZE

            cuboid = drawio_cuboid_stencil_xml(width, height, depth, f"{system_name} {placement_order}",
                                               infra_cost=infra_cost,
                                               color_top=color_top,
                                               color_side=color_side, color_front=color_front)
            placement_order += 1

            # first element placement at 0, 0
            if not prev_cuboid_bottom_left_x:
                rectangle = create_rectangle(layer_id(root, 'Buildings'), x, y, width=width + depth,
                                             height=height + depth / 2 + width / 2, value="", style=cuboid)
                root.append(rectangle)

                # these two guys will help us work out end of Front Road
                first_cuboid_bottom_right_x = width + depth
                first_cuboid_bottom_right_y = height + depth/2




            else:
                x = prev_cuboid_bottom_left_x - depth - width
                y = prev_cuboid_bottom_left_y - (height + depth / 2)

                rectangle = create_rectangle(layer_id(root, 'Buildings'), x, y, width=width + depth,
                                             height=height + depth / 2 + width / 2, value="", style=cuboid)
                root.append(rectangle)

            road_length_counter += width
            block_counter += 1
            prev_cuboid_bottom_left_x = x + depth - OFFSET
            prev_cuboid_bottom_left_y = y + height + (depth + width) / 2 + OFFSET / 2


        front_road = drawio_road_stencil_xml(road_length_counter + block_counter*OFFSET - OFFSET, 40, f"{road_length_counter + block_counter*OFFSET + OFFSET}", color_top=color_road)
        rectangle = create_rectangle(layer_id(root, 'Roads'),
                                     prev_cuboid_bottom_left_x + 60, # one unit in front
                                     prev_cuboid_bottom_left_y - (road_length_counter + block_counter*OFFSET)/2 + 10,
                                     width = road_length_counter + block_counter*OFFSET + OFFSET,
                                     height = (40 + road_length_counter + block_counter*OFFSET + OFFSET)/2,
                                     value="",
                                     style=front_road)
        root.append(rectangle)

        # front_road = drawio_road_stencil_xml(road_length_counter, 40, "", color_top=color_top)
        # rectangle = create_rectangle(layer_id(root, 'Roads'),
        #                              prev_cuboid_bottom_left_x + OFFSET - depth, # one unit in front
        #                              prev_cuboid_bottom_left_y - road_length_counter / 2 + 10,
        #                              width=road_length_counter + depth,
        #                              height= 40 / 2 + road_length_counter / 2, value="", style=front_road)
        # root.append(rectangle)

        class_color_index += 1

    # save xml to file
    # drawio_shared_functions.pretty_print(mxGraphModel)
    drawio_shared_functions.finish(mxGraphModel)
    os.system('"C:\Program Files\draw.io\draw.io.exe" output.drawio')

# get non-isometric line length from 2 sets of points
def get_line_length(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def analyze_drawio_file(filename):
    pass
    # inner = get_drawio_inner_xml("isometric_shape.drawio")
    # temp = get_drawio_from_file("isometric_shape.drawio")
    #
    # stencil = "zVVRToQwED1Nf01tzYZfg3oCL9CUYWmsDCl1F29v2+luZFdwXTRICOS9GV6HoY9hsuwb1QETvGHygQlxy3m4BrzPeJOx6jvQnsjaDFAR3XuHL7A3lc8Cpm3AGR+j8pHx+5ATT1nW6GDr8K2tRoFDuFNR4SxwCL/iLlY50CJFLuqdYEZMPM0oWNN+Uji+V5a4u0LjpIpiucSx+z/RGEtsFitc1orxB1mpmX9cxEUK2mIPk1myDPzE3g7mS+7RaNEFgu5pZSYk51JqPVdB8JSx9uunta7D8f3TVMFM0hJfruWIU3Nf44nVfhD/cz8VxS/tJw9DGA5xbpD2c8JiysUZ7ZQ125Yoj10mwXmjlR1lOvTKG8y5/Gai56mPZyMpsTQRE/EB"
    # decoded_stencil = drawio_tools.decode_diagram_data(stencil)
    # dom = xml.dom.minidom.parseString(decoded_stencil)
    # pretty_xml_as_string = dom.toprettyxml()
    # print(pretty_xml_as_string)

def tests():
    pass
    # TEST VARIOUS CUBOID SIZES
    # width, height, depth, unit_size = 2, 1, 4, 40
    # cuboid = drawio_cuboid_stencil_xml(width, height, depth, unit_size)
    # rectangle = create_rectangle(layer_id(root, 'Buildings'), 0, 0, width=(width + depth) * unit_size,
    #                              height=(height + (width + depth) / 2) * unit_size, value="", style=cuboid)
    # root.append(rectangle)
    #
    # width, height, depth, unit_size = 1, 1, 1, 40
    # cuboid = drawio_cuboid_stencil_xml(width, height, depth, unit_size)
    # rectangle = create_rectangle(layer_id(root, 'Buildings'), 0, 0, width=(width+depth)*unit_size, height=(height+(width+depth)/2)*unit_size, value="", style=cuboid)
    # root.append(rectangle)
    #
    # width, height, depth, unit_size = 4, 2, 1, 40
    # cuboid = drawio_cuboid_stencil_xml(width, height, depth, unit_size)
    # rectangle = create_rectangle(layer_id(root, 'Buildings'), 0, 0, width=(width + depth) * unit_size,
    #                              height=(height + (width + depth) / 2) * unit_size, value="", style=cuboid)
    # root.append(rectangle)


def draw_architecture_v1():
    # inner = get_drawio_inner_xml("isometric_shape.drawio")
    # temp = get_drawio_from_file("isometric_shape.drawio")
    #
    # stencil = "zVVRToQwED1Nf01tzYZfg3oCL9CUYWmsDCl1F29v2+luZFdwXTRICOS9GV6HoY9hsuwb1QETvGHygQlxy3m4BrzPeJOx6jvQnsjaDFAR3XuHL7A3lc8Cpm3AGR+j8pHx+5ATT1nW6GDr8K2tRoFDuFNR4SxwCL/iLlY50CJFLuqdYEZMPM0oWNN+Uji+V5a4u0LjpIpiucSx+z/RGEtsFitc1orxB1mpmX9cxEUK2mIPk1myDPzE3g7mS+7RaNEFgu5pZSYk51JqPVdB8JSx9uunta7D8f3TVMFM0hJfruWIU3Nf44nVfhD/cz8VxS/tJw9DGA5xbpD2c8JiysUZ7ZQ125Yoj10mwXmjlR1lOvTKG8y5/Gai56mPZyMpsTQRE/EB"
    # decoded_stencil = drawio_tools.decode_diagram_data(stencil)
    # dom = xml.dom.minidom.parseString(decoded_stencil)
    # pretty_xml_as_string = dom.toprettyxml()
    # print(pretty_xml_as_string)

    mxGraphModel = get_diagram_root()
    root = mxGraphModel.find("root")
    append_layers(root)

    UNIT_SIZE = 40

    prev_cuboid_bottom_left_x = None
    prev_cuboid_bottom_left_y = None

    OFFSET = 20

    x, y = 0, 0

    placement_order = 0

    for i, system in enumerate(data.systems_loaded):
        print(f"{system.name} {system.infra_size} {system.annualized_cost_in_thousands} \
                   {system.itsm_resilience_category}")

        width = system.infra_size * UNIT_SIZE
        height = system.itsm_resilience_category * UNIT_SIZE
        depth = system.annualized_cost_in_thousands * UNIT_SIZE
        color_top = webcol(palette_ligthtest[i % len(palette_ligthtest)])
        color_side = webcol(palette_lighter[i % len(palette_lighter)])
        color_front = webcol(palette[i % len(palette)])

        cuboid = drawio_cuboid_stencil_xml(width, height, depth, f"Text {placement_order}", color_top=color_top,
                                           color_side=color_side, color_front=color_front)
        placement_order += 1

        # first element placement at 0, 0
        if not prev_cuboid_bottom_left_x:
            rectangle = create_rectangle(layer_id(root, 'Buildings'), x, y, width=width + depth,
                                         height=height + depth / 2 + width / 2, value="", style=cuboid)
            root.append(rectangle)

        else:
            x = prev_cuboid_bottom_left_x - depth - width
            y = prev_cuboid_bottom_left_y - (height + depth / 2)

            rectangle = create_rectangle(layer_id(root, 'Buildings'), x, y, width=width + depth,
                                         height=height + depth / 2 + width / 2, value="", style=cuboid)
            root.append(rectangle)

        prev_cuboid_bottom_left_x = x + depth - OFFSET
        prev_cuboid_bottom_left_y = y + height + (depth + width) / 2 + OFFSET / 2

    # TEST VARIOUS CUBOID SIZES
    # width, height, depth, unit_size = 2, 1, 4, 40
    # cuboid = drawio_cuboid_stencil_xml(width, height, depth, unit_size)
    # rectangle = create_rectangle(layer_id(root, 'Buildings'), 0, 0, width=(width + depth) * unit_size,
    #                              height=(height + (width + depth) / 2) * unit_size, value="", style=cuboid)
    # root.append(rectangle)
    #
    # width, height, depth, unit_size = 1, 1, 1, 40
    # cuboid = drawio_cuboid_stencil_xml(width, height, depth, unit_size)
    # rectangle = create_rectangle(layer_id(root, 'Buildings'), 0, 0, width=(width+depth)*unit_size, height=(height+(width+depth)/2)*unit_size, value="", style=cuboid)
    # root.append(rectangle)
    #
    # width, height, depth, unit_size = 4, 2, 1, 40
    # cuboid = drawio_cuboid_stencil_xml(width, height, depth, unit_size)
    # rectangle = create_rectangle(layer_id(root, 'Buildings'), 0, 0, width=(width + depth) * unit_size,
    #                              height=(height + (width + depth) / 2) * unit_size, value="", style=cuboid)
    # root.append(rectangle)

    drawio_shared_functions.pretty_print(mxGraphModel)
    drawio_shared_functions.finish(mxGraphModel)

    os.system('"C:\Program Files\draw.io\draw.io.exe" output.drawio')


def drawio_road_stencil_xml(width, depth, text="Text", infra_cost=0, **kwargs):

    data = {
        "back_right_x": width,
        "back_right_y": 0,

        "back_left_top_x": 0,
        "back_left_top_y": width / 2,

        "front_right_top_x": width + depth,
        "front_right_top_y": depth / 2,


        "front_left_top_x": depth,
        "front_left_top_y": width / 2 + depth / 2,

        # if kwargs exists then use it, otherwise use default
        "color_top": kwargs['color_top'] if "color_top" in kwargs else "#ff0000",

        "diagram_width": int(width + depth),
        "diagram_height": int(width / 2 + depth / 2),
        # surprisingly, the aspect doesn't quite behave as you'd expect see
        # https://drawio.freshdesk.com/support/solutions/articles/16000052874-create-and-edit-complex-custom-shapes

        "text": text,
        "text_x": depth + 2,
        "text_y": width / 2 + depth / 2 - 15,

    }

    # TODO: finish template replacements

    # we draw our cuboid in order - lid, front, side
    cuboidTemplate = """
          <shape h="{diagram_height}" w="{diagram_width}" aspect="fixed" strokewidth="inherit">  
          <foreground>    
            <path>      
              <move x="{back_right_x}" y="{back_right_y}" />
              <line x="{front_right_top_x}" y="{front_right_top_y}" />      
              <line x="{front_left_top_x}" y="{front_left_top_y}" />      
              <line x="{back_left_top_x}" y="{back_left_top_y}" />      
              <close />
            </path>                
            <strokecolor color="{color_top}"/>
            <fillcolor color="{color_top}"/>    
            <fillstroke />                         
            <text str="{text}" x="{text_x}" y="{text_y}" valign="top" vertical="0" rotation="26.6"/>
          </foreground>  
        </shape>
    """

    xml = cuboidTemplate.format(**data)
    # print(xml)
    return f"shape=stencil({drawio_tools.encode_stencil(xml)});whiteSpace=wrap;html=1;"


def drawio_cuboid_stencil_xml(width, height, depth, text="Text", infra_cost=0, **kwargs):

    data = {
        "back_right_x": width,
        "back_right_y": 0,

        "back_left_top_x": 0,
        "back_left_top_y": width/2,

        "back_left_bottom_x": 0,
        "back_left_bottom_y": height + width/2,

        "front_right_top_x": width + depth,
        "front_right_top_y":  depth/2,

        "front_right_bottom_x": width + depth,
        "front_right_bottom_y": height + depth/2,

        "front_left_top_x": depth,
        "front_left_top_y": width/2 + depth/2,

        "front_left_bottom_x": depth,
        "front_left_bottom_y": height + (depth + width)/2,

        # if kwargs exists then use it, otherwise use default
        "color_top": kwargs['color_top'] if "color_top" in kwargs else "#ff0000",
        "color_side": kwargs['color_side'] if "color_side" in kwargs else "#0000ff",
        "color_front": kwargs['color_front'] if "color_front" in kwargs else "#00ff00",

        "diagram_width": int(width + depth),
        "diagram_height": int(width/2 + height + depth/2), # surprisingly, the aspect doesn't quite behave as you'd expect see
        # https://drawio.freshdesk.com/support/solutions/articles/16000052874-create-and-edit-complex-custom-shapes

        "text": text,
        "text_x": depth + 2,
        "text_y": width/2 + depth/2 + height - 15,

        # in the section below 10 creates a quarter unit bar graph, 20 half etc.
        # 5s need to be scaled up accordingly
        "cost_back_right_x": depth - infra_cost + 10, # one unit size
        "cost_back_right_y": width/2 + depth/2 - infra_cost/2 - 5, #(width-40)/2, # one unit size
        "cost_back_left_x": depth - infra_cost, # 0
        "cost_back_left_y": width/2 + depth/2 - infra_cost/2, # width/2
        "cost_front_right_x": depth + 10, #one unit size
        "cost_front_right_y": depth/2 + (width-10)/2, #one unit size
        "cost_front_left_x": depth,
        "cost_front_left_y": width/2 + depth/2,

    }

    # TODO: finish template replacements

    # we draw our cuboid in order - lid, front, side
    cuboidTemplate = """
          <shape h="{diagram_height}" w="{diagram_width}" aspect="fixed" strokewidth="inherit">  
          <foreground>    
            <path>      
              <move x="{back_right_x}" y="{back_right_y}" />
              <line x="{front_right_top_x}" y="{front_right_top_y}" />      
              <line x="{front_left_top_x}" y="{front_left_top_y}" />      
              <line x="{back_left_top_x}" y="{back_left_top_y}" />      
              <close />
            </path>    
            <strokecolor color="#000000"/>
            <fillcolor color="{color_top}"/>              
            <fillstroke />
           <path>      
              <move x="{front_right_top_x}" y="{front_right_top_y}" />
              <line x="{front_right_bottom_x}" y="{front_right_bottom_y}" />      
              <line x="{front_left_bottom_x}" y="{front_left_bottom_y}" />      
              <line x="{front_left_top_x}" y="{front_left_top_y}" />            
              <close />
            </path>    
            <strokecolor color="#000000"/>
            <fillcolor color="{color_front}"/>               
            <fillstroke />
           <path>      
              <move x="{back_left_top_x}" y="{back_left_top_y}" />
              <line x="{front_left_top_x}" y="{front_left_top_y}" />
              <line x="{front_left_bottom_x}" y="{front_left_bottom_y}" />
              <line x="{back_left_bottom_x}" y="{back_left_bottom_y}" />              
              <close />
            </path>    
            <strokecolor color="#000000"/>
            <fillcolor color="{color_side}"/>            
            <fillstroke />
            <path>      
              <move x="{cost_back_left_x}" y="{cost_back_left_y}" />
              <line x="{cost_back_right_x}" y="{cost_back_right_y}" />
              <line x="{cost_front_right_x}" y="{cost_front_right_y}" />
              <line x="{cost_front_left_x}" y="{cost_front_left_y}" />              
              <close />
            </path>    
            <strokecolor color="#000000"/>
            <fillcolor color="#FF0000"/>            
            <fillstroke />
            
            <text str="{text}" x="{text_x}" y="{text_y}" valign="top" vertical="0" rotation="26.6"/>
          </foreground>  
        </shape>
    """

    xml = cuboidTemplate.format(**data)
    # print(xml)
    return f"shape=stencil({drawio_tools.encode_stencil(xml)});whiteSpace=wrap;html=1;"


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
    layers['Buildings'] = create_layer('Buildings')
    layers['Roads'] = create_layer('Roads')
    for layer in layers.values():
        root.append(layer)
    return root


if __name__ == "__main__":
    main()

