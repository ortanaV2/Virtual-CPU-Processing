#DRAM (left: address) (right: data)
#The Storage can be predefined and is dynamically changeable. (When predefined => It's like starting at a CPU execution timestamp)
ram = [
[01010101, 00000001],
]

"""
4bit Instruction-Set:
0000 = load
0001 = add 
0010 = store
0011 = compare
0100 = jump
0101 = jump if
0110 = output
"""

#programmable instructions
#(instruction_address) (instruction) (memory_address) (data) (instruction_continuer)
instruction_data = [
    #first instruction_address must be 0001 else the cpu could start fetching the wrong instructor resulting instruction_bugs 
   [0001, 0000, 01010101, None, 0011], #Load data from RAM
   [0011, 0001, None, 00000001, 0111], #Add +1 to loaded data
   [0111, 0110, None, None, 0011] #Output loaded data
]

def instruction_search(address):
    for index, instruction in enumerate(instruction_data):
        if instruction[0] == address:
            return index

#CPU-clock-loop
clock_count = 0
while True:
    #Fetching
    start_instruction_index = instruction_search(0001)
    read_instruction = instruction_data[start_instruction_index]

    instruction_address = read_instruction[0]
    instruction = read_instruction[1]
    memory_address = read_instruction[2]
    data = read_instruction[3]
    instruction_continuer = read_instruction[4]

    print(read_instruction)   #Ended up here (int literals not permitted (obv))
    #Further plans: Build executer for instruction execution loop



    