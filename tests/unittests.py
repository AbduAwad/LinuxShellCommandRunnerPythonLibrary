import unittest

from ShellCommandRunnerLibrary.pipeline import Pipeline
from ShellCommandRunnerLibrary.pipelineTask import ShellCommand
from ShellCommandRunnerLibrary.validators import check_output_equals_validator


class TestShellLibrary(unittest.TestCase):
    def test_shell_command_basic(self):         # Test ShellCommand basic functionality


        s = ShellCommand("echo 123")
        s.run()


        self.assertEqual(s.output.strip(), "123")
        self.assertEqual(s.errors, None)
        self.assertEqual(s.ret_code, 0)
        self.assertTrue(s.success)




    def test_shell_command_ls_not_found(self): # Test ShellCommand with "ls filethatdoesnotexist"


        command = "ls filethatdoesnotexist"
        s = ShellCommand(command)
        s.run()


        self.assertEqual(s.output, None)
        self.assertEqual(s.errors, "ls: cannot access 'filethatdoesnotexist': No such file or directory")
        self.assertNotEqual(s.ret_code, 0)
        self.assertFalse(s.success)




    def test_shell_command_with_validator_success(self): # Test ShellCommand with a validator that checks if output is "123"


        s = ShellCommand("echo 123")
        s.add_validator(check_output_equals_validator("123"))
        s.run()


        self.assertEqual(s.ret_code, 0)
        self.assertEqual(s.output, "123")
        self.assertEqual(s.errors, None)
        self.assertTrue(s.success)


       
    def test_shell_command_with_validator_failure(self): # Test ShellCommand with a validator that checks if output is "123"


        s = ShellCommand("echo 456")
        s.add_validator(check_output_equals_validator("123"))
        s.run()


        self.assertEqual(s.ret_code, 0)
        self.assertEqual(s.output, "456")
        self.assertEqual(s.errors, None)
        self.assertFalse(s.success)




    def test_pipeline_second_commands_input_frm_first_command(self):


        s1 = ShellCommand("echo 123")
        s1.run()


        self.assertEqual(s1.output.strip(), "123")
        self.assertEqual(s1.errors, None)
        self.assertEqual(s1.ret_code, 0)
        self.assertTrue(s1.success)
       
        s2 = ShellCommand("sed 's/123/456/g'", input_data=s1.output)
        s2.run()


        self.assertEqual(s2.output.strip(), "456")
        self.assertEqual(s2.errors, None)
        self.assertEqual(s2.ret_code, 0)
        self.assertTrue(s2.success)




    def test_pipeline_with_commands1(self):
        # Create ShellCommand instances
        s1 = ShellCommand("echo 123")
        s2 = ShellCommand("sed 's/123/456/g'")


        pipeline = Pipeline()
        pipeline.add(s1)
        pipeline.add(s2, pipe_input=True)
        pipeline.run()




        self.assertEqual(pipeline.output, ["123", "456"])
        self.assertEqual(pipeline.errors, None)  
        self.assertEqual(pipeline.ret_code, 0)  
        self.assertIsNone(pipeline.failed)  




    def test_pipeline_with_commands2(self):


        s1 = ShellCommand("echo 123")
        s2 = ShellCommand("sed 's/123/456/g'")
        s2.add_validator(check_output_equals_validator("123"))


        pipeline = Pipeline()
        pipeline.add(s1)
        pipeline.add(s2, pipe_input=True)
        pipeline.run()


        self.assertEqual(pipeline.output, ["123", "456"])
        self.assertEqual(pipeline.errors, None)
        self.assertEqual(pipeline.ret_code, 0)
        self.assertEqual(pipeline.failed, s2.command)  




    def test_pipeline_with_commands3(self):


        s1 = ShellCommand("echo 123")
        s2 = ShellCommand("ls filethatdoesnotexist")


        pipeline = Pipeline()
        pipeline.add(s1)
        pipeline.add(s2)
        pipeline.run()


        self.assertEqual(pipeline.output, ["123"])
        self.assertEqual(pipeline.errors, ["ls: cannot access 'filethatdoesnotexist': No such file or directory"])
        self.assertNotEqual(pipeline.ret_code, 0)  
        self.assertEqual(pipeline.failed, s2.command)  























