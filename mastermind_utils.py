import numpy as np


COLORS = ['yellow',
          'red',
          'orange',
          'white', 
          'purple', 
          'green',
          'blue', 
          'pink',
          #'black'
         ]

def choose_random_combination(n=4):
    combination = np.random.choice(COLORS, n)
    return combination



def give_feedback(proposed_combination, true_combination):
    '''
    proposed_combination : combination currently proposed by the player
    true_combination     : combination that must be guessed
    Return : the number of correct elements in the proposition, the number of elements correctly positionned
    '''
    assert len(proposed_combination)==len(true_combination)
    
    list_temp = list(true_combination).copy()
    number_correct_elements = 0
    for element in proposed_combination:
        if element in list_temp:
            number_correct_elements += 1
            list_temp.remove(element)

    number_correct_positions = len([(proposition,solution) for proposition,solution in zip(proposed_combination, true_combination)
                                if proposition==solution])
    number_correct_elements -= number_correct_positions
    return number_correct_elements, number_correct_positions