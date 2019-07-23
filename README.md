# Traffic-Generator
Poisson web traffic generator, allowing on-the-fly traffic's load chaning

# Usage
```
traffic_generator.py --filename Y --interval X --init Z --ip W --verbose B
```
As:
__Y__ = a file containing only the Poisson's Lambda parameter value (number)
__X__ = an integer to set the interval between cheking the Lambda's file changes
__Z__ = initial Lambda's value
__W__ = target ip address / web server
__B__ = set to 1 to view the log output
