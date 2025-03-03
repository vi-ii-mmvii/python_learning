##### 1. Multiply Numbers from List
import functools, operator
lst = [ 1, 2, 3, 4, 5, 6]
print(functools.reduce(operator.mul, lst))


##### 2. Upper and Lower Case Letters in String
string = 'Ullamco Ex doLOre consECtetur fugiat aliQUIp esse culpa eIUsmod offICia ullamco.'
print(f"Uppers: {sum(1 for i in string if i.isupper())}\nLowers: {sum(1 for i in string if i.islower())}")


##### 3. Polindrome or not ?
string = "madam"
print(f"Polindrome: {string == string[::-1]}")


##### 4. Square Root after `X` miliseconds
import time, math

input, delay = 25100, 2123

time.sleep(delay / 1000)
print(f"Square root of {input} after {delay} miliseconds is {math.sqrt(input)}")


##### 5. All Elements of Tuple are True ?
tuple_1, tuple_2 = (True, 1, "Str"), (False, 1, "Str")
print(all(tuple_1))
print(all(tuple_2))
