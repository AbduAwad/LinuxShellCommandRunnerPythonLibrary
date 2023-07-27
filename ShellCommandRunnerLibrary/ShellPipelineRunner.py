# Encapsulates the excecution of a single shell command
import subprocess


# Custom Validators
class ShellCommandValidator:
    def validate(self, output, errors, ret_code):
        raise NotImplementedError("validate method must be implemented in the subclass")

# Example custom validator creation function
def check_output_equals_validator(output_to_check):
    class OutputEqualsValidator(ShellCommandValidator):
        def validate(self, output, errors, ret_code):
            return output == output_to_check
    return OutputEqualsValidator()


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




class Pipeline:
    def __init__(self):
        self.shell_command_pipeline = []
        self.failed = None


    def add(self, task: PipelineTask, pipe_input=False):
        if not isinstance(task, PipelineTask):
            raise ValueError("Invalid task. It must be a subclass of PipelineTask.")
        self.shell_command_pipeline.append((task, pipe_input))


    def run(self):
        previous_output = None
        for task, pipe_input in self.shell_command_pipeline:
            if pipe_input and previous_output is not None:
                task.input_data = previous_output
            task.run()


            if not hasattr(task, "success") or not task.success:
                self.failed = task.command
                break


            previous_output = task.output


        # After all tasks are executed, set the pipeline's properties
        output_list = []
        for task, _ in self.shell_command_pipeline:
            if task.output is not None:
                output_list.append(task.output)

        if any(output_list):
            self.output = output_list
        else:
            self.output = None
           


        errors_list = []
        for task, _ in self.shell_command_pipeline:
            if task.errors is not None:
                errors_list.append(task.errors)


        if any(errors_list):
            self.errors = errors_list
        else:
            self.errors = None


        #Set thepipeline return code of the last item in the list, and 0 index of the  tuple (task, pipe_input)'s return code
        self.ret_code = self.shell_command_pipeline[-1][0].ret_code














