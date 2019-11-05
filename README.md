# Traffic-Generator
Poisson web traffic generator, allowing on-the-fly traffic's load chaning

# Usage
```
traffic_generator.py --filename Y --interval X --init Z --ip W --verbose B
```
__Y__ = a file containing only the Poisson's Lambda parameter value (number)

__X__ = an integer to set the interval between checking the Lambda's file changes

__Z__ = initial Lambda's value

__W__ = target ip address / web server

__B__ = turn the log output on or off (1 or 0)
