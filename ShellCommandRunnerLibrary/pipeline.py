from .pipelineTask import PipelineTask

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





