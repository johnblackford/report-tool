#! /usr/bin/env python

"""
## File Name: abstract_classes.py
##
## Description: Define the Abstract Input/Output Handlers
##
## Functionality:
##  - Abstract Input Reader
##  - Abstract Output Writer
##  - Abstract Validator
##
"""



class AbstractInputReader(object):
    """Abstract Input Reader - sub-classes MUST implement:
            - read()
            - get_input_format()
            - process_properties(props)"""


    def read(self, filename):
        """Read the input file"""
        raise NotImplementedError()

    def get_input_format(self):
        """Retrieve the Input Format that this Input Reader supports"""
        raise NotImplementedError()

    def process_properties(self, props):
        """Process the JSON version of the properties file for this Input Reader"""
        raise NotImplementedError()



class AbstractOutputWriter(object):
    """Abstract Output Writer - sub-classes MUST implement:
            - write()
            - get_output_format()
            - process_properties(props)"""


    def write(self, document, filename):
        """Write the output"""
        raise NotImplementedError()

    def get_output_format(self):
        """Retrieve the Output Format that this Output Reader supports"""
        raise NotImplementedError()

    def process_properties(self, props):
        """Process the JSON version of the properties file for this Output Reader"""
        raise NotImplementedError()



class AbstractValidator(object):
    """ Abstract Validator - sub-classes MUST implement:
             - validate()"""


    def validate(self, document):
        """Execute the valiation code; true=passed, false=failed"""
        raise NotImplementedError()

