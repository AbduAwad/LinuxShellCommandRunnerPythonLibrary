from setuptools import find_packages, setup

setup(
    name='ShellCommandRunnerLibrary',
    packages=find_packages(include=['ShellCommandRunnerLibrary']),
    version='0.1.0',
    description='The ShellCommandRunner library is a Python module that provides an easy and efficient way to execute shell linux commands and build pipelines of shell linux commands. It allows you to run shell commands, validate their outputs, and chain multiple commands together to create complex pipelines.',
    author='Abdulrahman Awad',
    install_requires=[],
    test_suite='tests',
)

