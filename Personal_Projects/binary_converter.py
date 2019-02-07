#binary_converter.py
"""Takes any non-special number and converts it into IEEE 754 floating point form."""

import numpy as np

#Initialize variables
s_precision = 52    #Number of digits of precision in the significand fraction
e_precision = 11    #Number of digits of precision in the exponent
s_digits = np.zeros(s_precision+1)    #Actual digits of the significand
e_digits = np.zeros(e_precision)    #Actual digits of the exponent
while True:
    isFrac = input("Is this a fraction or a decimal? (f/d): ")
    if isFrac == "f" or isFrac == "F":
        numer = float(input("Numerator to convert to IEEE 754 floating point binary: "))
        denom = float(input("Denominator to convert to IEEE 754 floating point binary: "))
        number = numer/denom
        break
    elif isFrac == "d" or isFrac == "D":
        number = float(input("Number to convert to IEEE 754 floating point binary: "))
        break

#Get the sign
sign = 0
if number < 0:
    sign = 1
    number = abs(number)

#Iteratively find the exponent
total = 0
max_power = np.floor(np.log2(number))
max_power_shift = max_power + 1023
for i,e in enumerate(np.arange(e_precision-1, -1, -1)):
    if total + 2**e <= max_power_shift:
        total += 2**e
        e_digits[i] = 1

#Iteratively find the significand
total = 0
for i,e in enumerate(np.arange(max_power, max_power-(s_precision+1), -1)):
    if total + 2**e <= number:
        total += 2**e
        s_digits[i] = 1

#Get the significand fraction
f_digits = np.array([s_digits[i] for i in np.arange(1,s_precision+1)])

print("Sign: " + str(sign))
print("Exponent: " + str(e_digits))
print("Significand: " + str(s_digits))
print("Significand Fraction: " + str(f_digits))
print(sign, end='')
for i in range(e_precision):
    print(int(e_digits[i]), end='')
for i in range(s_precision):
    print(int(f_digits[i]), end='')