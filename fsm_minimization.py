"""
Created on Fri Nov 28 12:31:29 2025

@author: Jing Yuen Ng
email : jngg0200@student.monash.edu
Title : Moore FSM State Minimization
"""

import itertools
import time

# Code for minimization 

def raw_data_to_dictionary(state_names,next_state_list,output,opcode):
    # to convert raw data into a look up table for easier computation in the next operation
    # state names is a list of strings representing each state's name
    # next_state-list is a nested list where each of the inner list is a list of strings where each string represent the next state that the FSm will transition to provided certain input combinations is given
    # output is a list of binary strings if it is a Moore FSM where each binary strings represent the output for a certain state
    # output is a nested list if it is a Mealy FSM where each inner list is a similar list compared to the list that will be given if its a Moore FSM
    #opcode = 0 if Moore and opcode = 1 if Mealy

    result = {}    #empty dictionary to hold the result

    for index,state in enumerate(state_names):
        #each states will have its own key in the main dictionary
        temp_dict ={}   #temperarory dictionary holder for each state in each iteration of the for loop
        count = 0

        # storing data that tells us the next state logic for each state
        #eg any arbitraty state : {'input0' : state1 , 'input1' : state2 .......}
        for next_states in next_state_list[index]: 
            key = f"input{count:.0f}"
            temp_dict[key] = next_states
            count +=1
        
        #storing data that tells us the output 
        if opcode == 0:  #if it is moore, the output is always the same at every state
            temp_dict["Output"] = output[index]
        else:
            #for mealy, the approach is similar to how we store the data for next state logic
            count = 0

            for out in output[index]:
                key = f'Output{count:.0f}'
                temp_dict[key] = out
                
                count+=1

        result[state] = temp_dict
    
    return result


        
def single_step_cleaning(nested_list,master_dict,input_combination):
    #this function look up the current nested list and the data provided from the master_dict to proceed to the next iteration of cleaning the nested list
    #this is done by breaking done each inner list in the nested list into different lists if the states are known to be not equivalent

    #EG : nested list = [[1,2],[3,4]]
    #if based on the master_dict, we know that state 1 and 2 are certainly not equivalent but we are still unsure about state 3 and 4
    #this function will convert the nested list to [[1],[2],[3,4]]

    lookUpDict = {}   #temperorary look up table that store the index of the list that each state is currently located in within the nested list
    '''
    {
    'State1' : 1
    'State2' : 2
    'state3' : 2} if nested list = [[state1],[state2,state3]]
    '''

    new_list = []   

    #making the temperorary look up table
    for index, sublist in enumerate(nested_list):
        for state in sublist:
            lookUpDict[state] = index


    for group in nested_list:
        if len(group) > 1:
            group_list = []   #list holder

            for state in group:
                target_dict = master_dict[state]   #get the info for the target state from the master dictionary

                holding_list = []  #to store the index of the states that the target state will transition to
                n = 0
                for key,next_state in target_dict.items():

                    if n == input_combination:   
                        #if the transition information is already obtained, we can break the for loop to prevent information about output to be registered as well
                        break

                    else:
                        next_state_index = lookUpDict[next_state]    #get the index of the next state within the nested list
                        holding_list.append(next_state_index)   #gather the info into a temperorary holding list
                        n += 1

                #group list gather the transition index of each member state within the same inner list in the nested list
                group_list.append(holding_list)

            #to check if any of the member state within the same group has the same transition index, if they have the same, this means that particular states are equivalent to each other
            group_indexes = {}
            for index, sublist in enumerate(group_list):
                key = tuple(sublist)
                group_indexes.setdefault(key,[]).append(index)
            
            for indexes_list in group_indexes.values():
                new_group = []
                if len(indexes_list) == 1:
                    new_group.append(group[indexes_list[0]])
                    new_list.append(new_group)
                else:
                    for index in indexes_list:
                        new_group.append(group[index])
                    new_list.append(new_group)

        #if there's only one state in a group : the state will definitely not have any equivalent state, thus we can add straightaway to our list holder
        else:
            new_list.append(group)
    return new_list



def fsm_minimization(state_names,next_state_list,output,operand):

    input_combinations = len(next_state_list[0])

    #convert the raw data to a master dictionary before starting the minimization
    master_dict = raw_data_to_dictionary(state_names,next_state_list,output,operand)

    #to hold the first list
    first_list = []

    first_dict = {}

    #group the states into different list based on their output 
    for index, out in enumerate(output):
        if operand == 1:
            out = tuple(out)   #convert to tuple because it is hashable so that it can become a dictionary's key
        first_dict.setdefault(out,[]).append(index)
        
    #grouping is done here
    for index_list in first_dict.values():
        nested = []
        for index in index_list:
            nested.append(state_names[index])
        first_list.append(nested)
    
    #carry out the first iteration of cleaning
    cleaned = single_step_cleaning(first_list,master_dict,input_combinations)
    prev_list = first_list

    #keep on cleaning the nested list until a same nested list is returned by the function
    #frozenset is used so that it is hashable and can be contained by an outer set
    #list is avoided as the sequence in which the groups are arranged in the nested list is not important
    while {frozenset(x) for x in prev_list} != {frozenset(x) for x in cleaned}:
        prev_list = cleaned
        cleaned = single_step_cleaning(prev_list,master_dict,input_combinations)
    return cleaned

def is_valid_response(input, boo):
    #used to check if the response is valid when asking whether to proceed to the next stage when prompting the user
    #boo is a mode where True means it is checking for ['', 1] whereas False means it is checking for [0,1] 
    if input == "" and boo:
        return True, input
    try:
        input = int(input)
        if (input in [0,1] and not boo) or (boo and input == 1):
            return True , input
        else:
            print("Invalid input. Please try again")
            return False, None
    except ValueError:
        print("Invalid input, Please try again")
        return False, None

def to_proceed(input):
    #to check whether to proceed or not based on the input from the user
    if input == "":
        return True
    else:
        return False

def check_to_proceed():
    #check whether the user want to proceed to the next stage by utilizing the function defined previously
    while True:
        print("Press ENTER to proceed ; Press 1 to change your previous input")
        response = input("Enter Here : ")
        is_valid, response = is_valid_response(response, True)
        if not is_valid:
            continue
        break
    return response

def main_program():
    print("Welcome to the FSM Minimization Machine")

    #to determine the type of FSM to be minimized : MOORE OR MEALY
    while True:
        print("Please select the type of FSM to be minimized. Enter 0 for Moore FSM ; Enter 1 for Mealy FSM")

        response = input("Enter here (NO DECIMAL POINTS) : ")

        is_valid, operand = is_valid_response(response, False)
        if not is_valid:
            continue
        print()

        if operand == 0:
            print("Moore FSM is selected")
        else:
            print("Mealy FSM is selected")

        response = check_to_proceed()

        if not to_proceed(response):
            continue
        break
    print()

    #obtain the number of states and names while making sure all inputs are valid
    while True:
        print("Please enter the number of states")
        try:
            num_states = int(input("Enter here (MUST BE INTEGER and AT LEAST 2 STATES) : "))
            if num_states <= 1:
                print("The number of states must be greater than or equal to 2")
                print("Please try again")
                continue
            print()
            print("Please enter the names of the states in a list. Eg : [alpha, beta, gamma, delta]")
            state_names = input("Enter here (FOLLOW THE FORMAT PROVIDED) : ")
            state_list = [x.strip() for x in state_names.strip("[]").split(',')]
            if len(state_list) != num_states:
                print("The number of states in the list doesn't match the number of states inputed previously")
                print("Please try again")
                continue
            
            #to check if there are repeated states
            temp_list = []
            num = 0
            for state in state_list:
                if state not in temp_list:
                    temp_list.append(state)
                    num += 1
            if num != num_states:
                print("There are repeated state in your state list. Please try again")
                continue

            print()
            print(f"States inputed : {state_list}")
            response = check_to_proceed()

            if not to_proceed(response):
                continue

            break
        except ValueError:
            print("Non-integer detected. Please try again")
            continue
    print()

    print("Now, you are required to enter information regarding states transition")

    #obtain bit width of the input
    while True:
        print("Please enter the bit width of the input")
        try:
            bit_width = int(input("Enter the bit width here (POSITIVE INTEGER ONLY) : "))
            if bit_width < 1 :
                print("Invalid input. Please try again")
                continue
            break
        except ValueError:
            print("Non-integer detected. Please try again")
            continue

    #obtain the next state logic for each state that has been inputed by the user
    print()
    print("Next, Please enter the info regarding the state transitions")
    
    next_state_list = []
    for i in range(num_states):

        print('''
        Input Guide : Please follow the example given
        The states of a particular FSM : [alpha, beta, gamma, delta]

        If the input,X is 1 bit:
        - alpha transition to beta when X = 0
        - alpha transition to delta when X = 1
        Next state list for alpha is -----> [beta, delta]
            
        If the input,X is 2 bit:
        - alpha transition to beta when X = 00
        - alpha transition to delta when X = 01
        - alpha transition to alpha when X = 10
        - alpha transition to gamma when X = 11
        Next state list for alpha is -----> [beta, delta, alpha,gamma] ''')

        while True:
            print(f"Please input next state list for state {state_list[i]}")
            next_state_transitions = input("Enter here (PLEASE FOLLOW THE GUIDE GIVEN) : ")
            next_state_transitions = [x.strip() for x in next_state_transitions.strip("[]").split(",")]
            if len(next_state_transitions) != 2**bit_width:
                print(f"The number of transitions doesn't match the number of transitions available. There should be {(2**bit_width):.0f} transitions for each states")
                continue

            error = 0
            for state in next_state_transitions:
                if state not in state_list:
                    error += 1
                    print("Invalid state input detected")
                    print(f"{state} is not a valid state based on your list of states given at the beginning. Please try again")
                    break
            if error != 0:
                continue
            print()
            print(f"Next State Transition for state {state_list[i]} : {next_state_transitions}")

            response = check_to_proceed()

            if not to_proceed(response):
                continue
            break

        next_state_list.append(next_state_transitions)
    
    #obtain the output for each states while making sure they are in the right format depending on whether it is a MOORE or MEALY FSM
    print("Next, Please enter information regarding the output for each states")

    while True:
        print("Please enter the bit width of the output")
        try:
            output_bit_width = int(input("Enter here (INTEGER ONLY) :"))
            if output_bit_width < 1:
                print("Invalid input. Please try again")
                continue
            break
        except ValueError:
            print("Non-integer input detected. Please try again")
            continue
    
    combinations_tuple = itertools.product([0,1],repeat = output_bit_width)
    binary_strings = [''.join(map(str,x)) for x in combinations_tuple]

    

    if operand == 0:
        print("Please enter the output based on the following guide")
        print('''
Input Guide :
Input Guide : Please follow the example given
The states of a particular FSM : [alpha, beta, gamma, delta]
Output for each states:
    - Alpha : 01
    - Beta : 11
    - Gamma : 10
    - Delta : 11
Output List = [01,11,10,11]
              ''')
        while True:
            output_list = input("Enter the output list here : ")
            output_list = [x.strip() for x in output_list.strip("[]").split(",")]
            if len(output_list) != num_states:
                print("Number of output inputed doesn't match the number of states available")
                print("Please try again")
                continue
            
            error = False
            for output in output_list:
                if len(output) != output_bit_width:
                    error = True
                    print(f"{output} doesn't match the output bit width provided")
                    print("Please try again")
                    break
                
                if output not in binary_strings:
                    error = True
                    print(f"{output} is invalid. Please try again")
                    break
            if error:
                continue

            print()
            print(f"The output list : {output_list}")

            response = check_to_proceed()

            if not to_proceed(response):
                continue
            break

        master_output_list = output_list

    else:
        print('''
Input Guide : Please follow the example given
The states of a particular FSM : [alpha, beta, gamma, delta]
The output bit width is 2

If the input,X is 1 bit:
- alpha output '01' when x = 0
- alpha output '00' when X = 1
output_list for alpha is -----> [01, 00]
    
If the input,X is 2 bit:
- alpha output '11' when X = 00
- alpha output '11' when X = 01
- alpha output '10' when X = 10
- alpha output '01' when X = 11
Next state list for alpha is -----> [00,01,10,11] ''')
        
        master_output_list = []
        for i in range(num_states):

            while True:
                print(f"Please input output list for state {state_list[i]}")
                output_list = input("Enter here (PLEASE FOLLOW THE GUIDE GIVEN) : ")
                output_list = [x.strip() for x in output_list.strip("[]").split(",")]
                if len(output_list) != 2**bit_width:
                    print(f"Please make sure there's an output for each input combination. There should be {(2**bit_width):.0f} outputs for each states")
                    continue

                error = False
                for output in output_list:
                    if len(output) != output_bit_width:
                        print(f"The bit width of {output} is invalid. Please try again")
                        error = True
                        break

                    if output not in binary_strings:
                        error = True
                        print(f"{output} is invalid. Please try again")
                        break

                if error:
                    continue

                print()
                print(f"The output list for state {state_list[i]} : {output_list}")

                response = check_to_proceed()
                if not to_proceed(response):
                    continue
                break

            master_output_list.append(output_list)  

    answer = fsm_minimization(state_list,next_state_list,master_output_list,operand)
    print("loading...........")
    print()
    time.sleep(2)

    print("Result : ")
    print(answer)
    count  = 1

    for inner_list in answer:
        if len(inner_list) >1:
            print(f"Equivalent Group {count:.0f} :")
            for state in inner_list:
                print(f"{state}")
            count += 1
    if count == 1:
        print("There are no equivalent states")

main_program()









                








    


