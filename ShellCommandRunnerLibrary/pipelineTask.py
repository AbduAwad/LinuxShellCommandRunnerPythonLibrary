import subprocess
from .validators import ShellCommandValidator


class PipelineTask:
    def __init__(self):
        self.output = None
        self.errors = None
        self.ret_code = None
        self.success = None
        self.command = None
        self.input_data = None
       
    def run(self):
        raise NotImplementedError("run method must be implemented in the subclass")


class ShellCommand(PipelineTask):
    def __init__(self, command,  input_data = None, ignore_return_code=False):
        super().__init__()
        self.command = command
        self.input_data = input_data
        self.ignore_return_code = ignore_return_code
        self.validators = []  # List to store the validators


    def add_validator(self, validator):
        if not isinstance(validator, ShellCommandValidator):
            raise ValueError("Invalid validator. It must be a subclass of ShellCommandValidator.")
        self.validators.append(validator)




    def run(self):
        try:
            completed_process = subprocess.run(
                self.command,
                input=self.input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )
            self.output = None if not completed_process.stdout else completed_process.stdout.strip()
            # Set errors to None if there are no errors, otherwise set it to the actual errors.
            self.errors = None if not completed_process.stderr else completed_process.stderr.strip()
            self.ret_code = completed_process.returncode


            # Ignore Return Code Functionality
            if self.ignore_return_code:
                self.success = True
            else:
                self.success = self.ret_code == 0


            # Run all the validators and set success=False if any validator returns False:
            for validator in self.validators:
                if not validator.validate(self.output, self.errors, self.ret_code):
                    self.success = False
                    break


        except Exception as e:
            self.output = None
            self.errors = str(e)
            self.ret_code = -1
            self.success = False    







