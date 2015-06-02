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
    namespaces = {
      "urn:broadband-forum-org:cwmp:datamodel-1-0": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-1-1": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-1-2": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-1-3": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-1-4": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-1-5": "dm",
      "urn:broadband-forum-org:cwmp:datamodel-report-0-1": "dmr",
      "http://www.w3.org/2001/XMLSchema-instance": "xsi"
    }

    # Open the File for reading
    with open(filename, "r") as in_file:
      logger.info("Starting to parse the input file: {}".format(filename))
      xml_dict = xmltodict.parse(in_file, process_namespaces=True, namespaces=namespaces)
      logger.info("Finished parsing the input file")

    # Process the document attributes and elements
    self.doc.set_spec(xml_dict["dm:document"].get("@spec", "UNKNOWN"))
    self.doc.set_file(xml_dict["dm:document"].get("@file", "UNKNOWN"))
    self.doc.set_description(xml_dict["dm:document"].get("description", "[Description not provided]"))

    ### TODO: Handle Imports

    # Process dataType elements in the document
    for data_type_item in xml_dict["dm:document"]["dataType"]:
      data_type = nodes.DataType()
      data_type.set_name(data_type_item["@name"])
      data_type.set_base(data_type_item.get("@base", ""))
      data_type.set_status(data_type_item.get("@status", "current"))
      data_type.set_description(data_type_item.get("description", "[Description not provided]"))

      ### TODO: check to see if there is a list element, then process it like a normal list

      # If it doesn't have a base then it has a type;
      #  If it does have a base then it won't have a type, but could have other facets
      if len(data_type_item.get("@base", "")) == 0:
        type_facet = self._process_type_facet(data_type_item)
        print type_facet
        # generic function to read the type facet: base64, boolean, dateTime, hexBinary, int, long, string, unsignedInt, unsignedLong
      else:
        # generic function to read other facets: size, instanceRef, pathRef, range, enumeration, enumerationRef, pattern, units
        pass

    print ""
    if "bibliography" in xml_dict["dm:document"]:
      for biblio_ref_item in xml_dict["dm:document"]["bibliography"]["reference"]:
        print biblio_ref_item.keys()

    print ""
    print xml_dict["dm:document"]["model"]["@name"]

    # TODO: Add in Data Types next

    return self.doc



  def _process_type_facet(self, item):
    type_facet = None
    logger = logging.getLogger(self.__class__.__name__)

    if "base64" in item:
      pass
    elif "boolean" in item:
      pass
    elif "dateTime" in item:
      pass
    elif "hexBinary" in item:
      pass
    elif "int" in item:
      pass
    elif "long" in item:
      pass
    elif "string" in item:
      type_facet = nodes.StringType()
    elif "unsignedInt" in item:
      pass
    elif "unsignedLong" in item:
      pass
    else:
      logger.error("Type Facet expected and not found")

    return type_facet

