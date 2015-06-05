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


  def process_properties(self, props):
    logger = logging.getLogger(self.__class__.__name__)
    logger.info("This Input Reader has no Properties")
  


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
    logger.debug("Processing Document Element: spec attribute, file attribute, and description element")
    self.doc.set_spec(xml_dict["dm:document"].get("@spec", "UNKNOWN"))
    self.doc.set_file(xml_dict["dm:document"].get("@file", "UNKNOWN"))
    self.doc.set_description(xml_dict["dm:document"].get("description", "[Description not provided]"))

    ### TODO: Handle Imports

    # Process dataType elements in the document
    for data_type_item in xml_dict["dm:document"]["dataType"]:
      self.doc.add_data_type(self._process_data_type(data_type_item))

    print ""
    if "bibliography" in xml_dict["dm:document"]:
      for biblio_ref_item in xml_dict["dm:document"]["bibliography"]["reference"]:
        print biblio_ref_item.keys()

    print ""
    print xml_dict["dm:document"]["model"]["@name"]

    return self.doc



  def _process_data_type(self, item):
    data_type = nodes.DataType()
    logger = logging.getLogger(self.__class__.__name__)

    data_type.set_name(item["@name"])
    logger.debug("Processing DataType Element [{}]".format(item["@name"]))

    data_type.set_base(item.get("@base", ""))
    data_type.set_status(item.get("@status", "current"))
    data_type.set_description(item.get("description", "[Description not provided]"))

    ### TODO: check to see if there is a list element, then process it like a normal list

    # If it doesn't have a base then it has a type;
    #  If it does have a base then it won't have a type, but could have other facets
    if len(item.get("@base", "")) == 0:
      data_type.set_type(self._process_type_facet(item))
    else:
      ### TODO: Should this combine the following facets with the Base's Data Type details?
      # generic function to read other facets: size, instanceRef, pathRef, range, enumeration, enumerationRef, pattern, units
      pass

    return data_type




  def _process_type_facet(self, item):
    type_facet = None
    logger = logging.getLogger(self.__class__.__name__)

    if "base64" in item:
      type_facet = nodes.Base64Type()
      if "size" in item["base64"]:
        self._process_sizes_for_type_facet(type_facet, item["base64"]["size"])
    elif "boolean" in item:
      type_facet = nodes.BooleanType()
    elif "dateTime" in item: 
      type_facet = nodes.DateTimeType() 
    elif "hexBinary" in item: 
      type_facet = nodes.HexBinaryType() 
      if "size" in item["hexBinary"]:
        self._process_sizes_for_type_facet(type_facet, item["hexBinary"]["size"])
    elif "int" in item:
      type_facet = nodes.NumericType("int")
      ### TODO: Handle Range
      ### TODO: Handle Units
    elif "long" in item:
      type_facet = nodes.NumericType("long")
      ### TODO: Handle Range
      ### TODO: Handle Units
    elif "string" in item:
      type_facet = nodes.StringType()
      ### TODO: Redo these 2 as lists instead of single items
      type_facet.add_path_ref(item["string"].get("pathRef", ""))
      type_facet.add_enumeration_ref(item["string"].get("enumerationRef", ""))
      ### TODO: Handle Enumerations

      if "size" in item["string"]:
        self._process_sizes_for_type_facet(type_facet, item["string"]["size"])

      if "pattern" in item["string"]:
        self._process_patterns_for_type_facet(type_facet, item["string"]["pattern"])
    elif "unsignedInt" in item:
      type_facet = nodes.NumericType("unsignedInt")
      ### TODO: Handle Range
      ### TODO: Handle Units
    elif "unsignedLong" in item:
      type_facet = nodes.NumericType("unsignedLong")
      ### TODO: Handle Range
      ### TODO: Handle Units
    else:
      logger.error("Type Facet expected and not found")

    return type_facet



  def _process_sizes_for_type_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    if isinstance(item, list):
      for size_list_item in item:
        min_length = size_list_item.get("@minLength", None)
        max_length = size_list_item.get("@maxLength", None)

        a_size = nodes.Size()
        a_size.set_min_length(min_length)
        a_size.set_max_length(max_length)
        logger.debug("Adding Size: minLength={}, maxLength={}".format(min_length, max_length))
        type_facet.add_size(a_size)
    else:
      min_length = item.get("@minLength", None)
      max_length = item.get("@maxLength", None)

      a_size = nodes.Size()
      a_size.set_min_length(min_length)
      a_size.set_max_length(max_length)
      logger.debug("Adding Size: minLength={}, maxLength={}".format(min_length, max_length))
      type_facet.add_size(a_size)
  

  def _process_patterns_for_type_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: Some pattern items are lists of Ordered Dictionaries and some are just an Ordered Dictionary
    if isinstance(item, list):
      for pattern_list_item in item:
        pattern_value = pattern_list_item["@value"]

        a_pattern = nodes.Pattern()
        a_pattern.set_value(pattern_value)
        logger.debug("Adding Pattern: \"{}\"".format(pattern_value))
        type_facet.add_pattern(a_pattern)
    else:
      pattern_value = item["@value"]

      a_pattern = nodes.Pattern()
      a_pattern.set_value(pattern_value)
      logger.debug("Adding Pattern: \"{}\"".format(pattern_value))
      type_facet.add_pattern(a_pattern)

