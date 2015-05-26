#! /usr/bin/python

## 
## File Name: debugWriters.py
##
## Description: Debug Text Output Writer
## 
## Functionality:
##  - Output Writer for the Debug Text Format
## 

import nodes
import logging

from abstractIOHandlers import AbstractOutputWriter


class TextOutputWriter(AbstractOutputWriter):
  """Debug Text Output Writer"""

  def __init__(self):
    self.doc = None
    self.verbose_logging = False



  def enable_verbose_logging(self):
    self.verbose_logging = True


  def get_output_format(self):
    return "text"


  def write(self, doc, filename):
    console = False
    logger = logging.getLogger(self.__class__.__name__)

    if len(filename) == 0:
      self._write_to_console(doc)
    else:
      self._write_to_file(doc, filename)



  def _write_to_console(self, doc):
    logger = logging.getLogger(self.__class__.__name__)

    if self.verbose_logging:
      logger.info("Writing to the console")

    print "Document Description:"
    print doc.get_description()


  def _write_to_file(self, doc, filename):
    logger = logging.getLogger(self.__class__.__name__)

    # Open the File for writing
    with open(filename, "w") as out_file:
      if self.verbose_logging:
        logger.info("Writing to the file: {}".format(filename))

      out_file.write("Document Description:\n")
      out_file.write("{}\n".format(doc.get_description()))

      if self.verbose_logging:
        logger.info("Finished writing the output file")

