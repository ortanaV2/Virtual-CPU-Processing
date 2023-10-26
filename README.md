# CPU-Data-Processing-Replica
> [!NOTE]
> This program is only a rough approximation of a simple real CPU. Its purpose is to create an basic understanding of how the system works and how it computes.
## Instruction data // CPU-Programming
> How to program the CPU.

_**Example**_: `["0001", "0000", "01010101", None, "0011"]`

This block of code represents a _single instruction_ for the CPU to execute. It's structure is build like this: 

`[instruction_address, instruction_type, memory_address, data, instruction_continuer]`

The purpose of the instruction address is to establish a sequence of instructions that must be executed in a specific order. Also required is the instruction continuer, which informs the CPU about the next instruction to be processed (it appends to an already existing instruction address). To enable the CPU to determine the type of computation required, the instruction type is essential, as it defines the primary instruction from the instruction set.

## Instruction set 
> Base instructions

* 0000 = load  >  _imports data from RAM_
* 0001 = add  >  _adds number to data_
* 0010 = store  > _stores data in RAM_
* 0011 = compare  >  _compares two datasets_
* 0100 = output  >  _outputs data in terminal_

> [!NOTE]
> Updates are upcoming. Not all base functionalities are given.

## DATA-STORAGE
### RAM
> RAM structure

_**Example**_: `["00101101", "10011010"]` --> `[memory_address, data]`
### REGISTER
> Register types

* accumulator > _imported data_
* memory_address > _saved memory address_
* result_register > _calculation values_
* state_register > _(True/False) values_

## SETTINGS
(Default) `show_process = True` >  _shows the process-steps in terminal_

(Default) `clock_speed = 1` >  _instruction step speed_
### USAGE
> Program your own CPU instructions in `instruction_data`.
