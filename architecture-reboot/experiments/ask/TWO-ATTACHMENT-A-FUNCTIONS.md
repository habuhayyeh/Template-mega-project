# FILE A â€” FUNCTION LIBRARY

DO NOT EXECUTE THIS FILE.

This file defines functions only. It contains no call script. Example lines are illustrations, not calls.

## Functions

F_ADD1(x) => x + 1

F_DOUBLE(x) => x * 2

F_APPEND(history, token) => history with token appended at the end

F_WRAP(text) => "[" + text + "]"

F_SUB3(x) => x - 3

F_MAX(x, y) => the larger of x and y

F_IF_POS(x, a, b) => a if x is greater than 0, otherwise b

F_JOIN(history, separator) => the history strings joined by separator

F_LEN(list) => the number of items in the list

F_PAIR(x, y) => [y, x]

F_UNUSED(x) => x - 1

F_UNUSED2(x) => x * 100

## Illustrations only

F_MAX(2, 3) => 3

F_JOIN(["x", "y"], "-") => "x-y"

F_SUB3(10) => 7

END FUNCTION LIBRARY

