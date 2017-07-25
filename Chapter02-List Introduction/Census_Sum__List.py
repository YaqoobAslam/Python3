newEngland=[["Massachusetts",6692824],["Connecticut",3596080],
              ["Maine",1328302],["New Hampshire",1323459],
              ["Rhode Island",1051511],["Vermont",626630]]
def Polulation(state_data):
    Sum =0
    number_states=len(state_data)
    for i in range(0,number_states):
        one_state=state_data[i]
        pop = one_state[1]
        Sum= Sum + pop
    print("The total population of this list of states is:",Sum)

Polulation(newEngland)

output:
The total population of this list of states is 14618806