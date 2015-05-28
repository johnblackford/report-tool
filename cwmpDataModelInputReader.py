#! /usr/bin/env python

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



  def get_input_format(self):
    return "cwmp-dm"


  def read(self, filename):
    xml_dict = []
    logger = logging.getLogger(self.__class__.__name__)

    # Use these standard namespaces
    ### TODO: Probably need to map all versions of "dm" and "dmr" into the same value
    namespaces = {
      "urn:broadband-forum-org:cwmp:datamodel-1-5": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-report-0-1": "dmr",
      "http://www.w3.org/2001/XMLSchema-instance": "xsi"
    }

    # Open the File for reading
    with open(filename, "r") as in_file:
      logger.info("Starting to parse the input file: {}".format(filename))
      xml_dict = xmltodict.parse(in_file, process_namespaces=True, namespaces=namespaces)
      logger.info("Finished parsing the input file")

    # Process the File's Contents
    ### TODO: Complete this
    ### TODO: Create methods to handle the various parts
    self.doc.set_spec(xml_dict["dm:document"]["@spec"])
    self.doc.set_file(xml_dict["dm:document"]["@file"])
    self.doc.set_description(xml_dict["dm:document"]["description"])

    return self.doc

