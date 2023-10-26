#DRAM (left: address) (right: data)
#The Storage can be predefined and is dynamically changeable. (When predefined => It's like starting at a CPU execution timestamp)
#Numbers must be 8bit long.
ram = [
["01010101", "00000001"],
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
    #first instruction_address must be "0001" else the cpu could start fetching the wrong instructor resulting instruction_bugs 
   ["0001", "0000", "01010101", None, "0011"], #Load data from RAM
   ["0011", "0001", None, "00000001", "0111"], #Add +1 to loaded data
   ["0111", "0110", None, None, "1111"], #Output loaded data
   ["1111", "0010", None, None, "0001"] #store result in ram for further processes
]

def instruction_search(address):
    #get index of instruction with searching address
    for index, instruction in enumerate(instruction_data):
        if instruction[0] == address:
            return index

def binary_decoder(str):
    #Convert binary string to int list
    #   "0101"  =>  [0,1,0,1] 
    if str is None:
        return None
    else:
        bin = [int(b) for b in str]
        return bin

def ram_addressing(addr):
    #Iterating through memory_words in ram and return data (binary_decoded) from given address
    for memory_word in ram:
        if binary_decoder(memory_word[0]) == addr:
            return binary_decoder(memory_word[1])
    return None
        
def ram_index(address):
    #get memory_word index with given memory_address
    for index, memory in enumerate(ram):
        if binary_decoder(memory[0]) == address:
            return index

#CPU-clock-loop
clock_count = 0 #clock start
loaded_data_register = None #prefix loaded data register
address_register = None #prefix address register
result_register = None #prefix result register
while True:
    import time
    time.sleep(1)
#Fetching (instruction iteration)
    if clock_count == 0:
        instruction_index = instruction_search("0001")
    clock_count+=1

    read_instruction = instruction_data[instruction_index]

    instruction_address = binary_decoder(read_instruction[0])
    instruction = binary_decoder(read_instruction[1])
    memory_address = binary_decoder(read_instruction[2])
    data = binary_decoder(read_instruction[3])
    instruction_continuer = binary_decoder(read_instruction[4])

    #upcoming instruction_index
    instruction_index = instruction_search(read_instruction[4])

    print(instruction_address) #debug print

#Executer
    #load instruction
    if instruction == [0,0,0,0]:
        loaded_data_register = ram_addressing(memory_address)
        address_register = memory_address
        #check requirements
        if address_register is None:
            print("Missing: 'memory_address not found'")
            break
    #add instruction
    if instruction == [0,0,0,1]:
        #check requirements
        if loaded_data_register is None:
            print("Missing: 'loaded_data in data_register'")
            break
        else:
            carry = 0
            result = []
            for i in range(7, -1, -1): #iterating bit for bit (right to left)
                bit1 = data[i]
                bit2 = loaded_data_register[i]

                bit_sum = bit1 + bit2 + carry #adding given number in binary to loaded_data_register
                result.insert(0, bit_sum % 2)
                carry = bit_sum // 2 
            if carry:
                result.insert(0, carry)
            result_register = result
            print(f"Result: {result}") #debug print
    #store instruction
    if instruction == [0,0,1,0]:
        #overwriting data from address_register with data from result_register
        address_index = ram_index(address_register)
        ram[address_index][1] = "".join(str(bit) for bit in result_register)

        print(f"RAM-result: {ram[0][1]}") #debug print