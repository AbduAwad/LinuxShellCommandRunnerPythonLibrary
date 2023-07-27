# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now you can import ShellCommandRunnerLibrary
from ShellCommandRunnerLibrary.ShellPipelineRunner import ShellCommand, Pipeline, check_output_equals_validator


# Test ShellCommand basic functionality
s = ShellCommand("echo 123")
s.run()
print("ShellCommand basic functionality:")
print("Output:", s.output.strip())
print("Errors:", s.errors)
print("Return Code:", s.ret_code)
print("Success:", s.success)
print()


# Test ShellCommand with "ls filethatdoesnotexist"
command = "ls filethatdoesnotexist"
s = ShellCommand(command)
s.run()
print("ShellCommand with 'ls filethatdoesnotexist':")
print("Output:", s.output)
print("Errors:", s.errors)
print("Return Code:", s.ret_code)
print("Success:", s.success)
print()



# Test ShellCommand with a validator that checks if output is "123"
s = ShellCommand("echo 123")
s.add_validator(check_output_equals_validator("123"))
s.run()
print("ShellCommand with validator checking '123':")
print("Output:", s.output)
print("Errors:", s.errors)
print("Return Code:", s.ret_code)
print("Success:", s.success)
print()




# Test ShellCommand with a validator that checks if output is "123", but the command outputs "456"
s = ShellCommand("echo 456")
s.add_validator(check_output_equals_validator("123"))
s.run()
print("ShellCommand with validator checking '123', but outputs '456':")
print("Output:", s.output)
print("Errors:", s.errors)
print("Return Code:", s.ret_code)
print("Success:", s.success)
print()




# Test Pipeline with input from first command to the second command
s1 = ShellCommand("echo 123")
s1.run()
print("Pipeline - First command: echo 123")
print("Output:", s1.output.strip())
print("Errors:", s1.errors)
print("Return Code:", s1.ret_code)
print("Success:", s1.success)
print()


s2 = ShellCommand("sed 's/123/456/g'", input_data=s1.output)
s2.run()
print("Pipeline - Second command: sed 's/123/456/g'")
print("Output:", s2.output.strip())
print("Errors:", s2.errors)
print("Return Code:", s2.ret_code)
print("Success:", s2.success)
print()




# Test Pipeline with multiple commands
s1 = ShellCommand("echo 123")
s2 = ShellCommand("sed 's/123/456/g'")
p = Pipeline()
p.add(s1)
p.add(s2, pipe_input=True)
p.run()
print("Pipeline with multiple commands:")
print("Output:", p.output)
print("Errors:", p.errors)
print("Return Code:", p.ret_code)
print("Failed:", p.failed)
print()




# Add a validator to the second command
s1 = ShellCommand("echo 123")
s2 = ShellCommand("sed 's/123/456/g'")
s2.add_validator(check_output_equals_validator("123"))
p = Pipeline()
p.add(s1)
p.add(s2, pipe_input=True)
p.run()
print("Pipeline with validator:")
print("Output:", p.output)
print("Errors:", p.errors)
print("Return Code:", p.ret_code)
print("Failed:", p.failed)
print()




# Test Pipeline with a command that does not exist
s1 = ShellCommand("echo 123")
s2 = ShellCommand("ls filethatdoesnotexist")
p = Pipeline()
p.add(s1)
p.add(s2)
p.run()
print("Pipeline with non-existing command:")
print("Output:", p.output)
print("Errors:", p.errors)
print("Return Code:", p.ret_code)
print("Failed:", p.failed)












