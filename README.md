📘 FSM State Minimization Tool (Moore & Mealy Machines)

A Python-based tool that minimizes Moore or Mealy Finite State Machines (FSMs) using an automated partition-refinement algorithm.

This script interactively:

 - Accepts state names

 - Accepts transition tables

 - Accepts outputs (Moore: per-state; Mealy: per-input)

 - Performs full FSM minimization

 - Returns the equivalent-state groups after minimization

 - Supports any bit-width for input/output and allows detailed user validation between each step.

🔧 Features
✔️ Supports Both FSM Types:

1. Moore Machines (output depends only on state)

2. Mealy Machines (output depends on state + input)

✔️ Interactive CLI Workflow

The script:

 - Validates all user inputs

 - Guides you through transition table creation

 - Confirms steps before proceeding

 - Displays minimization results in clear groups

✔️ Implements Classical Partition Refinement

The algorithm:

1. Groups states by output equivalence

2. Splits groups based on next-state distinctions

3. Iterates until no more refinement is possible

4. Returns final minimal partition set

✔️ Handles Any Input Bit-Width

1-bit → 2 transitions

2-bit → 4 transitions

N-bit → 2ⁿ transitions


▶️ How to Run
1. Install Python (3.8+)

 - Make sure Python is installed.

2. Run the Script
python fsm_minimizer.py

📝 Usage Guide

The program walks you through these steps:

1️⃣ Choose FSM Type
Please select the type of FSM to be minimized.
Enter 0 for Moore FSM ; Enter 1 for Mealy FSM

2️⃣ Enter Number of States & Names

Example:

Enter number of states: 4
Enter the names: [A, B, C, D]

3️⃣ Enter Input Bit-Width

Example:

Bit-width of input: 2   → 4 possible input combinations

4️⃣ Enter Transition Table

Example for a 2-bit input:

Next-state list for state A:
[ B, C, A, D ]

5️⃣ Enter Output Specification
Moore example:
[00, 11, 10, 11]

Mealy example:
For State A: [00, 01, 10, 11]

📉 Output Format

Example output:

Equivalent Group 1:
A
D

Equivalent Group 2:
B
C


If no equivalence:

There are no equivalent states

🧠 Theory Behind Minimization

 - The script implements the Moore reduction algorithm (also applicable to Mealy):

 - Partition states by output

 - Split groups based on transition destinations

 - Repeat until stable

 - Final groups = minimized FSM states
