# Temperature Converter (Celsius to Fahrenheit and vice-versa)

c = float(input("Enter temperature in Celsius: "))
f = (c * 9/5) + 32
print("Fahrenheit:", f)

f = float(input("Enter temperature in Fahrenheit: "))
c = (f - 32) * 5/9
print("Celsius:", c)