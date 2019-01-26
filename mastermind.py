import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, row, column
from bokeh.io import curdoc
from bokeh.models.widgets import RadioGroup, Button

from mastermind_utils import choose_random_combination, give_feedback, COLORS



# Choice of the combination to guess
true_combination = choose_random_combination()

#Dataframe containing historic of trials and answers
df_historic = pd.DataFrame(columns=['slot_1','slot_2','slot_3','slot_4',
                                    'correct_elements','correctly_positioned', 'try'])

# Button to choose the color in first, second, third and fourth position
slot_1 = RadioGroup(labels=COLORS, active=None,name='Place 1')
slot_2 = RadioGroup(labels=COLORS, active=None,name='Place 2')
slot_3 = RadioGroup(labels=COLORS, active=None,name='Place 3')
slot_4 = RadioGroup(labels=COLORS, active=None,name='Place 4')

# List of slots
list_slots = [slot_1, slot_2, slot_3, slot_4]

# Check button to have feedback on current proposal
check = Button(label="Check", button_type="success")

# Restart button 
restart = Button(label="Restart", button_type="success")

# Current iteration
current_try = 0

# Function triggered when the "check" button is clicked on
def check_button():
    '''
    This function collects the current proposition, then plots the feedback and the current proposition.
    '''
    global current_try, df_historic, true_combination, p, ds

    # Current proposal by the player
    proposed_combination = [COLORS[slot.active] for slot in list_slots]
    
    # Compute the correct elements and correctly positioned elements
    curr_correct, curr_correct_pos = give_feedback(proposed_combination, true_combination)
   
    # Update the current trial number
    current_try +=1
 
    # Gather previous data in order to add information of the current trial
    # NB : The add function below for datasource do not append the new data to previous data, but seem to replace it
    
    previous_x = ds.data['x'].copy()
    previous_y = ds.data['y'].copy()
    previous_colors = ds.data['fill_color'].copy()
    previous_line_colors = ds.data['line_color'].copy()
    previous_size = ds.data['size'].copy()
    
    # Possible coordinates for red pins
    x_red = [-1.5, -1, -1.5, -1]
    y_red = [current_try +0.2, current_try+0.2, current_try, current_try]
    
    # Possible coordinates for white pins
    x_white = [-0.5, 0, -0.5, 0]
    y_white = [current_try +0.2, current_try+0.2, current_try, current_try]
    
    
    # The new x coordinates are composed of the previous one, the slots 1,2,3,4 and then the red and white pins, depending on the correct answers
    x = previous_x + [1,2,3,4] + x_red[:curr_correct_pos] + x_white[:curr_correct]
    
     # The new y coordinates are composed of the previous one, the current number of trials and then the red and white pins, depending on the correct answers
    y = previous_y + [current_try]*4 + y_red[:curr_correct_pos] + y_white[:curr_correct]
    
    # The colors are composed of the previous ones, the current proposal, and the red and white pins
    col = previous_colors + [COLORS[slot.active] for slot in list_slots] + ['red']*curr_correct_pos + ['white']*curr_correct
    
    # Idem for line color and size
    line = previous_line_colors + ['black']*4 + ['black']*curr_correct_pos + ['black']*curr_correct 
    size = previous_size + [20]*4 + [10]*curr_correct_pos + [10]*curr_correct
    
    # Update of data source of circle plot
    ds.add(x, 'x')
    ds.add(y, 'y')
    ds.add(col, 'fill_color')
    ds.add(line, 'line_color')
    ds.add(size, 'size')
    
# When the check button is clicked, the function check_button() is triggered
check.on_click(check_button)


def restart_button():
    global ds, df_historic, true_combination, current_try

    #Dataframe containing historic of trials and answers
    df_historic = pd.DataFrame(columns=['slot_1','slot_2','slot_3','slot_4', 'correct_elements','correctly_positioned', 'try'])

    # Choice of the combination to guess
    true_combination = choose_random_combination()

    # Restart trial counter
    current_try = 0
  
    # Update of data source of circle plot
    ds.add([], 'x')
    ds.add([], 'y')
    ds.add([], 'fill_color')
    ds.add([], 'line_color')
    ds.add([], 'size')
 
# When the check button is clicked, the function check_button() is triggered
restart.on_click(restart_button)

# Declaration of the plot
p = figure(plot_height=600, plot_width=800, title="", x_range = (-2,5), y_range=(-1,10))
p.grid.visible = False

# Declaration of the (for now empty) scatter plot
plot_scatter = p.circle(x=[], y=[], line_color=[], fill_color=[], size=[])

# Declaration of the data source of this scatter plot
ds = plot_scatter.data_source

# Configuration of widgets
row_slots = row(slot_1, slot_2, slot_3, slot_4)
buttons = row(check, restart)
col_left = column(row_slots, buttons)
layout = row(col_left, p)

curdoc().add_root(layout)
curdoc().title = "Mastermind"
