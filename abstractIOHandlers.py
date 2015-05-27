#! /usr/bin/env python

## 
## File Name: abstractIOHandlers.py
##
## Description: Define the Abstract Input/Output Handlers
## 
## Functionality:
##  - Abstract Input Reader
##  - Abstract Output Writer
## 



class AbstractInputReader:
  """Abstract Input Reader - sub-classes MUST implement:
      - read() 
      - get_input_format()
      - enable_verbose_logging()"""


  def read(self, filename):
    raise NotImplementedError()

  def get_input_format(self):
    raise NotImplementedError()

  def enable_verbose_logging(self):
    raise NotImplementedError()



class AbstractOutputWriter:
  """Abstract Output Writer - sub-classes MUST implement:
      - write() 
      - get_output_format()
      - enable_verbose_logging()"""


  def write(self, document, filename):
    raise NotImplementedError()

  def get_output_format(self):
    raise NotImplementedError()

  def enable_verbose_logging(self):
    raise NotImplementedError()

