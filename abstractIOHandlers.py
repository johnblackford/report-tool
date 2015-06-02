#! /usr/bin/env python

## 
## File Name: abstractIOHandlers.py
##
## Description: Define the Abstract Input/Output Handlers
## 
## Functionality:
##  - Abstract Input Reader
##  - Abstract Output Writer
##  - Abstract Validator
## 



class AbstractInputReader(object):
  """Abstract Input Reader - sub-classes MUST implement:
      - read() 
      - get_input_format()"""


  def read(self, filename):
    raise NotImplementedError()

  def get_input_format(self):
    raise NotImplementedError()



class AbstractOutputWriter(object):
  """Abstract Output Writer - sub-classes MUST implement:
      - write() 
      - get_output_format()"""


  def write(self, document, filename):
    raise NotImplementedError()

  def get_output_format(self):
    raise NotImplementedError()



class AbstractValidator(object):
  """ Abstract Validator - sub-classes MUST implement:
       - validate()"""


  def validate(self, document):
    raise NotImplementedError()

