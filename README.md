# ShellCommandRunner Library


The ShellCommandRunner library is a Python module that provides an easy and efficient way to execute shell linux commands and build pipelines of shell linux commands. It allows you to run shell commands, validate their outputs, and chain multiple commands together to create a pipeline of subsequent linux shell commands.
___


## Install and Import Library:


### Installation:
You can install the library using the pip package manager, which comes with Python. Open a terminal or command prompt and run the following command: pip install the location of the wheel file.


```bash
pip install path to build wheel in dist folder
```


### Import:
Once you have installed your Python library, you can import it in a python script using:


```bash
import ShellCommandRunnerLibrary.ShellPipelineRunner
```
 You can import the necessary classes/functions as seen below:


```bash
from ShellCommandRunnerLibrary.ShellPipelineRunner import Pipeline, ShellCommand, check_output_equals_validator
```
___






## How To use the Library:
___


### **Using ShellCommand to Run a Single Command** (ShellCommand Class inherits from pipelineTask Class)
-  The ShellCommand class represents a single shell command that you want to execute. You can create an instance of ShellCommand, provide the command to be executed, and then run the command using the run() method.


Example - Run a Basic Shell Command:
```Python
# Create a ShellCommand instance for the command "echo 123"
s = ShellCommand("echo 123")


# Execute the command
s.run()


# Access the results
print("Output:", s.output.strip())  # Output: 123
print("Errors:", s.errors)  # Output: None (No errors)
print("Return Code:", s.ret_code)  # Output: 0 (Command executed successfully)
print("Success:", s.success)  # Output: True (Command succeeded)
```
___
### **Using The Pipeline to Run a Sequence of Commands** (Pipeline Class)


- The Pipeline class allows you to create a pipeline of shell commands, where you have the option to make the output of one command the input of the next command. You can also add custom validators to the commands within the pipeline as needed.


Example - Run a Simple Pipeline:


```Python
# Create ShellCommand instances for the commands "echo 123" and "sed 's/123/456/g'"
s1 = ShellCommand("echo 123")
s2 = ShellCommand("sed 's/123/456/g'")


# Create a Pipeline and add the ShellCommand instances to it
pipeline = Pipeline()
pipeline.add(s1)
pipeline.add(s2, pipe_input=True)


# Execute the pipeline
pipeline.run()


# Access the results
print("Output:", pipeline.output)  # Output: ['123', '456'] (Combined outputs of all commands)
print("Errors:", pipeline.errors)  # Output: None (Combined stderr of all commands is empty)
print("Return Code:", pipeline.ret_code)  # Output: 0 (Error code of the last command that ran)
print("Failed:", pipeline.failed)  # Output: None (No commands failed)
```
___


## Validators:


- Validators in the ShellCommandRunnerLibrary are custom classes that allow you to perform additional checks on the output, errors, and return code of a shell command. Validators are useful when you want to verify whether a command executed successfully and produced the expected results.


### Create a Custom Validator:


The validate_output_equals function is a custom validator creation function. It takes a parameter output_to_check, which specifies the desired output to validate against. It returns a new instance of a custom validator subclassed from ShellCommandValidator. This custom validator will check if the command output matches the provided output_to_check. A Validator can be added to any of the shell commands on the pipeline by invoking the shellcommand instances method, 'add_validator'.


Here's an example of how to create a custom validator:


```Python
# Create a ShellCommand instance for the command "echo 123"
s1 = ShellCommand("echo 123")


# Custom validator that checks if the output is "123"
Validate123 = validate_output_equals("123")


# Add a custom validator to the second command
s1.add_validator(Validate123)


```
**Using Pipeline to Run a Sequence of Commands With Validators:**
- Example:


```Python
# Create ShellCommand instances for the commands "echo 123" and "sed 's/123/456/g'"
s1 = ShellCommand("echo 123")
s2 = ShellCommand("sed 's/123/456/g'")


#Create A custom Validator:
Validate123 = create_validator(validate_output_equals("123"))


# Add a custom validator to the second command
s2.add_validator(Validate123)


# Create a Pipeline and add the ShellCommand instances to it
pipeline = Pipeline()
pipeline.add(s1)
pipeline.add(s2, pipe_input=True)


# Execute the pipeline and perform validation
pipeline.run()


# Access the results
print("Output:", pipeline.output)  # Output: ['123', '456'] (Combined outputs of all commands)
print("Errors:", pipeline.errors)  # Output: None (Combined stderr of all commands is empty)
print("Return Code:", pipeline.ret_code)  # Output: 0 (Error code of the last command that ran)
print("Failed:", pipeline.failed)  # Output: sed 's/123/456/g' (Command that failed)


```
## Unit Tests
___




To run the unit tests for the ShellCommandRunner library using bash, follow these steps:


1. Open a terminal. Navigate to the tests directory of the ShellCommandRunner library.


```bash
cd services/orchestrator/commandpipeline/tests
```


2. Run the unit tests using the python -m unittest command and specify the test file.
```bash
python -m unittest unittests.py -v
```
The -v option stands for "verbose," which displays detailed output for each test case, including successes and failures.


### Unit Test Results:
___
- After running the unit tests, you will see the test results for each individual test case.
- The output will indicate whether each test case passed or failed.
- The "OK" at the end indicates that all tests were successful. If any test fails, the specific test case details will be displayed.




____
--
## Virtual Environment:


```bash
cd to library directory
```


### Go ahead and create a virtual environment:


```bash
python3 -m venv venv
```


### Activate Virtual Environment


```bash
source venv/bin/activate
```

___

## How to build the Library - (Already Built: This is just a reference)
___

```bash
> pip install wheel
> pip install setuptools
> pip install twine

cd to the root of your project
> python setup.py bdist_wheel
> pip install dist/ShellCommandRunnerLibrary-0.1.0-py3-none-any.whl
```
