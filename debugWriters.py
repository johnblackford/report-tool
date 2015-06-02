#! /usr/bin/env python

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
import cStringIO

from abstractIOHandlers import AbstractOutputWriter


class TextOutputWriter(AbstractOutputWriter):
  """Debug Text Output Writer"""

  def __init__(self):
    self.doc = None
    self.one_line_output = False



  def get_output_format(self):
    return "text"


  def process_properties(self, props):
    logger = logging.getLogger(self.__class__.__name__)
    self.one_line_output = props.get("OneLine", False)
    logger.info("One Line Output Property now set to: {}".format(self.one_line_output))



  def write(self, doc, filename):
    console = False
    output_buffer = cStringIO.StringIO()
    logger = logging.getLogger(self.__class__.__name__)

    self._generate_content(doc, output_buffer)

    if len(filename) == 0:
      self._write_to_console(output_buffer)
    else:
      self._write_to_file(output_buffer, filename)

    output_buffer.close()



  def _generate_content(self, doc, out_buffer):
    logger = logging.getLogger(self.__class__.__name__)

    out_buffer.write("Document Spec: {}\n".format(doc.get_spec()))
    out_buffer.write("Document File: {}\n".format(doc.get_file()))

    out_buffer.write("Document Description:\n")
    out_buffer.write("{}\n".format(doc.get_description()))



  def _write_to_console(self, out_buffer):
    logger = logging.getLogger(self.__class__.__name__)
    logger.info("Writing to the console")
    print out_buffer.getvalue()



  def _write_to_file(self, out_buffer, filename):
    logger = logging.getLogger(self.__class__.__name__)

    # Open the File for writing
    with open(filename, "w") as out_file:
      logger.info("Writing to the file: {}".format(filename))
      out_file.write(out_buffer.getvalue())
      logger.info("Finished writing the output file")

