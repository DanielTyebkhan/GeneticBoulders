import pathlib
import os
import matplotlib.pyplot as plt
from matplotlib import cbook
import re

def plot_route(route):
    plot_problem(route.to_strings())

def plot_problem(stringList, start_num = 1, title = None, key = None, save = None):    
    p_dir = pathlib.Path(__file__).parent
    image_path = os.path.join(p_dir, 'moonboard2016Background.jpg')
    image_file = cbook.get_sample_data(image_path)
    plt.rcParams["figure.figsize"] = (30,10)
    img = plt.imread(image_file)
    x = []
    y = []
    for hold in stringList:
        # Using re.findall() 
        # Splitting text and number in string  
        res = [re.findall(r'(\w+?)(\d+)', hold.split("-")[0])[0]] 
        
        alphabateList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"] 
        ixInXAxis = alphabateList.index(res[0][0]) 
     
        x = x + [(90 + 52 * ixInXAxis)]# * img.shape[0] / 1024]
        y = y + [(1020 - 52 * int(res[0][1]))]# * img.shape[1] / 1024]

    # Create a figure. Equal aspect so circles look circular
    fig, ax = plt.subplots(1, dpi = 100)
    ax.set_aspect('equal')
    plt.axis('off')

    # Show the image
    ax.imshow(img)

    # Now, loop through coord arrays, and create a circle at each x,y pair
    count = 0
    for xx,yy in zip(x,y):
        if yy == 84:
            circ = plt.Circle((xx,yy), 30, color = 'r', fill=False, linewidth = 2)
        elif count < start_num:
            circ = plt.Circle((xx,yy), 30, color = 'g', fill=False, linewidth = 2)
        else:
            circ = plt.Circle((xx,yy), 30, color = 'b', fill=False, linewidth = 2)
        ax.add_patch(circ)
        count = count + 1
        
    if title:
        plt.title(title)
    if save:
        plt.savefig(key + '.jpg', dpi = 200)
    # Show the image
    plt.show()