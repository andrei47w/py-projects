# Bank
## Requirements
- You will be given one of the problems below to solve
- Use procedural programing and the simple feature-driven software development process
- Provide a console-based user interface that accepts given commands **exactly** as required
- Use built-in compound types to represent entities in the problem domain and access them using *getter* and *setter* functions
- Have at least 10 items in your application at startup
- Provide **specification** and **tests** for all non-UI functions related to every functionality

## Problem Statements
### 1. Numerical List
A math teacher needs a program to help students test different properties of complex numbers, provided in the `a+bi` form (we assume `a` and `b` are integers for simplicity). Write a program that implements the functionalities exemplified below:

**(A) Add a number**\
`add <number>`\
`insert <number> at <position>`\
e.g.\
`add 4+2i` – appends `4+2i` to the list\
`insert 1+1i at 1` – insert number `1+i` at position `1` in the list (positions are numbered starting from `0`)

**(B) Modify numbers**\
`remove <position>`\
`remove <start position> to <end position>`\
`replace <old number> with <new number>`\
e.g.\
`remove 1` – removes the number at position `1`\
`remove 1 to 3` – removes the numbers at positions `1`,`2`, and `3`\
`replace 1+3i with 5-3i` – replaces all occurrences of number `1+3i` with the number `5-3i`

**(C) Display numbers having different properties**\
`list`\
`list real <start position> to <end position>`\
`list modulo [ < | = | > ] <number>`\
e.g.\
`list` – display the list of numbers\
`list real 1 to 5` – display the real numbers (imaginary part `=0`) between positions `1` and `5`\
`list modulo < 10` – display all numbers having modulo `<10`
`list modulo = 5` – display all numbers having modulo `=10`

### 4. Bank Account
John wants to manage his bank account. To do this, he needs an application to store all the bank transactions performed on his account during a month. Each transaction is stored in the application using the following elements: `day` (of the month in which the transaction was made, between 0 and 30 for simplicity), `amount of money` (transferred, positive integer), `type` (`in` - into the account, `out` – from the account), and `description`. Write a program that implements the functionalities exemplified below:

**(A) Add transaction**\
`add <value> <type> <description>`\
`insert <day> <value> <type> <description>`\
e.g.\
`add 100 out pizza` – add to the current day an `out` transaction of `100 RON` with the *"pizza"* description\
`insert 25 100 in salary` – insert to day 25 an `in` transaction of `100 RON` with the *“salary”* description\

**(B) Modify transactions**\
`remove <day>`\
`remove <start day> to <end day>`\
`remove <type>`\
`replace <day> <type> <description> with <value>`\
e.g.\
`remove 15` – remove all transactions from day 15\
`remove 5 to 10` – remove all transactions between days 5 and 10\
`remove in` – remove all `in` transactions\
`replace 12 in salary with 2000` – replace the amount for the `in` transaction having the *“salary”* description from day 12 with `2000 RON`

**(C) Display transactions having different properties**\
`list`\
`list <type>`\
`list [ < | = | > ] <value>`\
`list balance <day>`\
e.g.\
`list` – display all transactions\
`list in` – display all `in` transactions\
`list > 100` - display all transactions having an amount of money `>100`\
`list = 67` - display all transactions having an amount of money `=67`\
`list balance 10` – compute the account’s balance at the end of day 10. This is the sum of all `in` transactions, from which we subtract `out` transactions occurring before or on day 10
