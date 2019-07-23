# Traffic-Generator
Poisson web traffic generator, allowing on-the-fly traffic's load chaning

# Usage

> traffic_generator.py --filename Y --interval X --init Z --ip W --verbose B
As:
Y = a file containing only the Poisson's Lambda parameter value (number)
X = an integer to set the interval between cheking the Lambda's file changes
Z = initial Lambda's value
W = target ip address / web server
B = set to 1 to view the log output
