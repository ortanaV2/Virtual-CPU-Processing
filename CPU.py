import time

show_process: bool = True # shows processing steps of the cpu
clock_speed: float = 0.2 # 0 => max_speed (based on cpu speed)

# DRAM (left: address) (right: data)
# The Storage can be predefined and is dynamically changeable. (When predefined => It's like starting at a CPU execution timestamp)
# NOTE: numbers must be 8bit long.
ram: list[list[str]] = [
["01010101", "00000001"],
]

# Programmable instructions (EXAMPLE)
instruction_data = [
# NOTE: first instruction_address must be "0001" else the cpu could start fetching the wrong instructor resulting in program-bugs 
# (instruction_address) (instruction) (memory_address) (data) (instruction_continuer)
   ["0001", "0000", "01010101", None, "0011"],              # load data from RAM (accumulate)
   ["0011", "0001", None, "00000001", "0111"],              # add +1 to accumulator
   ["0111", "0100", None, None, "1111"],                    # output accumulator (in decimal)
   ["1111", "0010", None, None, "0001"]                     # store result in RAM for further processes   
]

def instruction_search(address):
    # get index of instruction with searching address
    for index, instruction in enumerate(instruction_data):
        if instruction[0] == address:
            return index

def binary_decoder(binary_str: str) -> list[int]:
    # convert binary string to bit-list
    # example: "0101"  =>  [0,1,0,1] 
    if binary_str is None:
        return None
    else:
        bit_list = [int(bit) for bit in binary_str]
        return bit_list

def ram_addressing(addr):
    # iterating through memory_words in RAM and return data (binary_decoded) from given address
    for memory_word in ram:
        if binary_decoder(memory_word[0]) == addr:
            return binary_decoder(memory_word[1])
    return None
        
def ram_index(address):
    # get memory_word index with given memory_address
    for index, memory in enumerate(ram):
        if binary_decoder(memory[0]) == address:
            return index

def show_steps(txt):
    global show_process
    if show_process:
        time.sleep(clock_speed)
        print(txt)

clock_count: int = 0 # clock start
accumulator = None # prefix loaded-data register
memory_address_register = None #prefix memory-address-register
result_register = None #prefix result-register
state_register = None #prefix state-register

# CPU-Clock-Loop
while True:
    show_steps(f"[Clock_Count]: {clock_count}")
# Fetching (instruction iteration)
    if clock_count == 0:
        instruction_index = instruction_search("0001")
    clock_count+=1

    read_instruction = instruction_data[instruction_index]
    show_steps(f"[Loading instruction]")

    instruction_address = binary_decoder(read_instruction[0])
    instruction = binary_decoder(read_instruction[1])
    memory_address = binary_decoder(read_instruction[2])
    data = binary_decoder(read_instruction[3])
    instruction_continuer = binary_decoder(read_instruction[4])
    show_steps(f"[Instruction loaded]: {instruction_address}")
    show_steps(f"[Full Instruction]: {read_instruction}")

    # set upcoming instruction_index
    instruction_index = instruction_search(read_instruction[4])

# Executer
    # load-instruction
    if instruction == [0,0,0,0]:
        accumulator = ram_addressing(memory_address)
        memory_address_register = memory_address
        # check requirements
        if memory_address_register is None:
            print("Missing: 'memory_address not found'")
            break
        show_steps("[Accumulator set up]")

    # add-instruction
    if instruction == [0,0,0,1]:
        # check requirements
        if accumulator is None:
            print("Missing: 'loaded_data in data_register'")
            break
        else:
            carry = 0
            result = []
            for i in range(7, -1, -1): # iterating bit for bit (right to left)
                bit1 = data[i]
                bit2 = accumulator[i]
                show_steps(f"(reading single bits [{bit1}], [{bit2}])")

                bit_sum = bit1 + bit2 + carry # adding given number to accumulator
                show_steps(f"(adding [{bit1}]+[{bit2}]+[{carry}(carry)])")
                result.insert(0, bit_sum % 2)
                carry = bit_sum // 2 
                show_steps("{process carry}")
            if carry:
                result.insert(0, carry)
            result_register = result
            show_steps(f"[Result-register updated]: {result_register}")

    # store-instruction
    if instruction == [0,0,1,0]:
        # overwriting data from memory_address_register with data from result_register
        show_steps(f"[Searching ram-index]: {memory_address_register}")
        address_index = ram_index(memory_address_register)
        show_steps(f"[Found ram-index]: [{address_index}]")
        ram[address_index][1] = "".join(str(bit) for bit in result_register)
        show_steps(f"[Updating ram-data]: addr({memory_address}) // data({result_register})")

    # compare-instruction
    if instruction == [0,0,1,1]:
        # check requirements
        if data is None:
            print("Missing: 'key: data'")
        else:
            show_steps(f"[Compare]: ({data})==({accumulator})")
            if data == accumulator:
                state_register = True
            else:
                state_register = False
            show_steps(f"[Updating state-register]: {state_register}")

    # output-instruction
    if instruction == [0,1,0,0]:
        decimal_value = 0
        for i, bit in enumerate(reversed(accumulator)): # translate binary to decimal
            decimal_value += bit*(2**i)

        show_steps(f"[Converting bit_list to decimal]: {accumulator} => {decimal_value}")
        if not show_process:
            print(decimal_value)