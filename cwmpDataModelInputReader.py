#! /usr/bin/python

## 
## File Name: cwmpDataModelInputReader.py
##
## Description: CWMP-DM XML Input Reader
## 
## Functionality:
##  - Input Reader for CWMP-DM XML Format
## 


import nodes
import logging
import xmltodict

from abstractIOHandlers import AbstractInputReader



class DataModelInputReader(AbstractInputReader):
  """CWMP-DM XML Input Reader"""

  def __init__(self):
    self.doc = nodes.Document()
    self.verbose_logging = False



  def enable_verbose_logging(self):
    self.verbose_logging = True


  def get_input_format(self):
    return "cwmp-dm"


  def read(self, filename):
    xml_dict = []
    logger = logging.getLogger(self.__class__.__name__)

    # Open the File for reading
    with open(filename, "r") as in_file:
      if self.verbose_logging:
        logger.info("Starting to parse the input file: {}".format(filename))

      ### TODO: We need to handle namespaces when parsing
      xml_dict = xmltodict.parse(in_file)

      if self.verbose_logging:
        logger.info("Finished parsing the input file")

    # Process the File's Contents
    ### TODO: Complete this
    ### TODO: Create methods to handle the various parts
    self.doc.set_description(xml_dict["dm:document"]["description"])

    return self.doc

