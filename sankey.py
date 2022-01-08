#!/usr/bin/env python3 
"""Draw a sankey diagram using data from a given input file.
Student number : 20049301
Additional Challenge 2 attempted.
"""
import sys
from ezgraphics import GraphicsWindow
import random

WIDTH = 1000
HEIGHT = 700
MARGIN = 100
COLOURS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
           (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), 
           (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), 
           (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), 
           (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), 
           (255, 255, 255), (0, 0, 0)]


def read_file(file_name):
    """ Opens and reads the file. Returns the title, left-hand axis label and 
    the data values in the file.

    Args:
        file_name (str): File containing the data.

    Raises:
        FileNotFoundError: If file not found or is not readable, this exception is raised

    Return:
        title (str): diagram title 
        left_axis_label (str): name of the source
        lines (list): contains the lines of the file

    """
    #assert(file_name[-4:])== '.txt', 'Input file is not a text file'

    try:
        with open(file_name, 'r') as file:
            title = file.readline()
            left_axis_label = convert_source(file.readline())
            lines = file.readlines()
            lines.append(left_axis_label[1])
            return title, left_axis_label, lines

    except:
        raise FileNotFoundError

def convert_source(label):
    """
    Put the optional colour to source if there is one

    Args:
        label(string): line in the file containing the name of the source
    
    Return:
        label(list): Contains an empty string or the optional colour in RGB format
    
    Examples:
        Optional colour: ['Country', [' 0', '255', '255']]
        No optional colour: ['Country \n', '']
    """

    if ',' in label:
        label = label.strip().split(',') 
        label = [label[0], label[1:]]
    else:
        label = [label, '']

    assert type(label) == list, 'This is not a list'
    assert len(label) == 2, 'The list does not contain 2 elements'

    return label

        
def set_up_graph(title, left_axis_label):
    """
    Creates a window and canvas. Displays the title, left-hand axis label.
    Returns a reference to the window. 

    Args:
        title (str): title for the window
        left_axis_label (str): left-hand axis label

    Return:
        GraphicsWindow: reference to the window

    """

    assert(type(title)) == str, 'Title is not a string'
    assert(type(left_axis_label)) == list, 'Title is not a list'


    win = GraphicsWindow(WIDTH, HEIGHT)

    canvas = win.canvas()
    canvas.drawText(0, 0, title)
    canvas.drawText(10, HEIGHT/2, left_axis_label[0])

    return win    


def process_data(data_list):
    """Returns a dictionary produced by processing the data in the list.

    Args:
        data_list (list): list containing the data read from the file

    Raises:
        ValueError: raised if there are errors in the data values in the file

    Returns:
        dict (dict): contains data about the flows
    
    Examples:
        With optional source colour : 
            {'Australia': [529.0], 'Jamaica': [466.0], 'England': [450.0], 
            'New Zealand': [391.0], 'South Africa': [363.0], 
            'source': [' 0', '255', '255']}
        
        Without:
            {'Electricity': [72.88, [255, 255, 0]], 'Natural Gas': [48.11, [0, 170, 0]], 
            'Water': [96.47, [0, 0, 192]], 'Waste/Recycling': [23.49], 'Tax': [6.05], 
            'source': ''}    

    """

    dict = {}
    value = data_list.pop() #optional source colour 

    for i in range(len(data_list)): #For each destination
        line = data_list[i].strip().split(',')
        check_for_error(line, i+3)
        dict[line[0]] = create_value(line[1:]) 
    
    dict['source'] = value #last item
    return dict

def check_for_error(liste, line_number):
    """Check if there is an error on the line.
    
    Args:
        liste (list): List of strings on line i
        i (int): number of the line in the text file
    
    Raise:
        ValueError: If the key or value is empty, or if the value is not a number, this exception is raised.

    """

    if liste[0] == '': #Checking if key is empty
        print(f"Error on line: {line_number}, key is empty.")
        raise ValueError

    if liste[1] == '': #Checking if value is empty
        print(f"Error on line: {line_number}, value is empty.")
        raise ValueError

    try:  #Checking if value can ve converted to a float successfully
        float(liste[1])
    except:
        print(f"Error on line: {line_number}, value '{liste[1]}' is not a number.")
        raise ValueError


def create_value(liste):
    """
    Creates the value for each key in the dictionary. 
    
    Args 
        liste (list): liste of the potential multiple keys 
    
    Returns:
        [float(flow)] (list): Amount of flow for the destination
        [float(flow), colour] (list): Amount of flow with optional colour
        colour (list): RGB color values
        
    """

    flow = liste[0]

    if len(liste) > 1:
        RGB_values = liste[1:]
        colour = list(map(int, RGB_values)) #convert strings value into int
        return [float(flow), colour]

    else:
        return [float(flow)]

def calculus(data_dic):
    """
    Calculates the dimension of the sankey diagram in terms of pixel and layouts.

    Args:
        data_dic (dict): contains data about destinations and their respective flow

    Returns:
        pixel_per_unit_flow (float): Number of pixels for one unit of flow
        height_source (int): Height of the source rectangle
    
    """

    total_flow = 0
    
    for i in data_dic:
        total_flow += data_dic[i][0]
    
    assert total_flow != 0
      
    available_pixels = HEIGHT - 2 * MARGIN - (len(data_dic.keys())-1) * 10
    pixel_per_unit_flow = available_pixels / total_flow
    height_source = pixel_per_unit_flow * total_flow

    return pixel_per_unit_flow, height_source

def pick_random_colours(colours_list):
    """
    Pick a random colour in RGB format.

    Args :
        colours_list (list): list containing colours in RGB format
    
    Returns:
        R_value (int): Red colour value 
        G_value (int): Green colour value
        B_value (int): Blue colour value
        number (int): Random number

    """

    number = random.randint(0, len(colours_list) -1)
    colour_picked = colours_list[number]
    R_value = colour_picked[0] 
    G_value = colour_picked[1]
    B_value = colour_picked[2]
    COLOURS.remove(COLOURS[number]) #randomness

    return R_value, G_value, B_value


def difference(colour_source, colour_destination):
    """
    Compute the difference between the elements of the source and destination 
    RGB colour values.

    Args:
        colour_source (tuple): colour of the source rectangle in RGB format
        colour_destination (tuple): colour of the destination rectangle in RGB format

    Returns:
        list_diff (list): Differences between source and destination colour values.

    """

    list_diff = []
    for index in range (3):
        list_diff.append(colour_source[index] - colour_destination[index])
    
    return list_diff    
    
def new_colour(list_diff, colour_dest, delta):
    """
    Compute the new RGB colour values for each line.

    Args:
        list_diff (list): Differences between source and destination colour values.
        colour_dest (tuple): Colour of the destination in RGB format
        delta (float):  Ssmall increment by which y1 increases for each line 
        
    Returns:
        new_colour (tuple): colour of the new line drawn
        
    """

    # As delta increases, the difference between the source and destination colour value decreases
    new_R = colour_dest[0] + int((1-delta)*list_diff[0])
    new_G = colour_dest[1] + int((1-delta)*list_diff[1])
    new_B = colour_dest[2] + int((1-delta)*list_diff[2])
    new_colour = (new_R, new_G, new_B)

    return new_colour

def draw_lines(canva , y1, height_dest, y_destination, colour_source, colour_dest, x = 94):
    """
    Draw the vertical lines and colour them.


    Fill the polygon shape between the source and destination rectangle 
    by drawing a series of vertical lines from left to right. 

    Colour the lines so that the colour graduates 
    from the source colour to the destination colour.


    Args:
        canva (GraphicsCanvas): area intended for drawing pictures or other layouts 
        y1 (float): top y value of source rectangle 
        height_dest (float): small increment by which y1 increases for each line 
        y_destination (int): top y value of the destination rectangle
        colour_source (tuple): colour of the source rectangle in RGB format
        colour_dest (tuple): colour of the destination rectangle in RGB format
        x (int): top-right x value of the source rectangle
            Ref value = 94 : depends on horizontal margin chosen 

    """

    y2 = y1 + height_dest
    delta = y_destination - y1 
    list_diff = difference(colour_source, colour_dest)
    position = 0

    while position < 1:
        R, G, B = new_colour(list_diff, colour_dest, position)
        position += 1/756 # 756 = Distance between source and destination on x-absis.
        canva.setColor(R, G, B)
        canva.drawLine(x, y1 + position*delta , x, y2 + position*delta) 
        x += 1

    canva.setColor('black')

def draw_source_rectangle(canva, y_source, height_source, option_colour):
    """
    Draw the source rectangle on the canva.
    
    The colour of the rectangle is randomly chosen amongst tuples 
    contained in the 'COLOURS' list.

    Args:
        y_source (int): top y value of the source rectangle
        height_source (int): height of the source rectangle
        option_colour (str): optional colour for the source rectangle
            
    Returns:
        colour_source (tuple): colour of the source rectangle in RGB format

    """
    
    if option_colour != '': #If option colour is in RGB format
        R_source, G_source, B_source = int(option_colour[0]), int(option_colour[1]), int(option_colour[2])
        
    else : 
        R_source, G_source, B_source = pick_random_colours(COLOURS)

    canva.setFill(R_source, G_source, B_source)
    canva.drawRect(75, y_source, 20, height_source)
    colour_source = (R_source, G_source, B_source)

    return colour_source

def destination_rectangle(canva, destination, height_dest, y_source, y_destination, data_dic):
    """
    Draw the the destination rectangle within the canva. 

    Args:
        canva (GraphicsCanvas): Area intended for drawing pictures or other layouts 
        destination (string): destination name
        pixel_per_unit (int): height of the destination rectangle
    
    Returns:
        colour_dest (tuple): colour of the destination rectangle in RGB format
     
    """

    if len(data_dic[destination]) > 1: #If destination has optional colour value
        R_dest, G_dest, B_dest = data_dic[destination][1]

    else:
        R_dest, G_dest, B_dest = pick_random_colours(COLOURS)
        
    canva.setFill(R_dest, G_dest, B_dest)
    canva.drawRect(WIDTH - 150, y_destination , 20, height_dest)
    canva.drawText(WIDTH - 120, y_destination + height_dest/2, destination)
    canva.drawPoly((95, y_source), (95, y_source + height_dest), 
                    (WIDTH - 150, y_destination + height_dest), (WIDTH - 150, y_destination))

    colour_dest  = (R_dest, G_dest, B_dest)

    return  colour_dest


def draw_sankey(window, data_dic):
    """
    Draw the sankey diagram.

    Draw the source and destination rectangle, along with the polygon relying them.
    And the lines used to fill these polygons,
    with a colour that graduates from the source colour to the destination colour.

    Args:
        window (GraphicsWindow): contains the graph
        data_dic (dictionary): ccontains data about destinations and their respective flow
    
    """
    #Section a : Calculations
    opt_source_colour = data_dic.popitem()
    pixel_per_unit_flow, height_source = calculus(data_dic)
    canva = window.canvas()
    y_destination = MARGIN
    y_source = MARGIN + ((len(data_dic.keys()) - 1) * 10) / 2
    
    #Section b: Drawing the source bar
    colour_source = draw_source_rectangle(canva, y_source, height_source, 
                                          option_colour = opt_source_colour[1])
    
    #Section c: Draw polygons and vertical lines
    for destination in list(data_dic.keys()):  #list(data_dic.keys()) = the destinations

        height_dest = data_dic[destination][0] * pixel_per_unit_flow 

        colour_dest = destination_rectangle(canva, destination, height_dest, y_source, 
                                            y_destination, data_dic)

        draw_lines(canva, round(y_source), round(height_dest), y_destination, 
                   colour_source, colour_dest)

        y_destination += height_dest + 10 #Takes into account the gap
        y_source += height_dest
        
def main():
    # DO NOT EDIT THIS CODE
    input_file = ""
    args = sys.argv[1:]  
    
    if len(args) == 0:
        input_file = input("Please enter the name of the file: ")                    
    elif len(args) > 1:
        print('\n\nUsage\n\tTo visualise data using a sankey diagram type:\
            \n\n\tpython sankey.py infile\n\n\twhere infile is the name of \
            the file containing the data.\n')
        return         
    else:
        input_file = args[0]
    
    # Section 1: Read the file contents
    try:
        title, left_axis_label, data_list = read_file(input_file)
    except FileNotFoundError:
        print(f"File {input_file} not found or is not readable.")
        return

    # Section 2: Create a window and canvas
    win = set_up_graph(title, left_axis_label)

    # Section 3: Process the data
    try:
        data_dic = process_data(data_list)
    except:
        print("Content of file is invalid")
        return

    # Section 4: Draw the graph
    draw_sankey(win, data_dic)

    win.wait()


if __name__ == "__main__":
    main()