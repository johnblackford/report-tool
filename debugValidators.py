#! /usr/bin/env python

## 
## File Name: cwmpDataModelInputReader.py
##
## Description: CWMP-DM XML Input Reader
## 
## Functionality:
##  - Input Reader for CWMP-DM XML Format
## 


import logging
import cStringIO

from abstract_classes import AbstractValidator



class DocDescValidator(AbstractValidator):
  """Debugging Validator - validates the Document Description is not empty"""

  def validate(self, document):
    output_buffer = cStringIO.StringIO()
    logger = logging.getLogger(self.__class__.__name__)

    logger.info("Starting Validator...")

    if len(document.get_description()) == 0:
      out_buffer.write("Validation Failure: WARN: Document Description is empty")
      print out_buffer.getvalue()
      logger.warn(out_buffer.getvalue())
    else:
      logger.debug("All Validation Passed")

    logger.info("Validator Complete")
      
    output_buffer.close()
