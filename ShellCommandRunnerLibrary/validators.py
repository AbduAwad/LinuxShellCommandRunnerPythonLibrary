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