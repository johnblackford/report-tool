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
      self.doc.add_data_type(self._process_data_type_element(data_type_item))

    print ""
    if "bibliography" in xml_dict["dm:document"]:
      for biblio_ref_item in xml_dict["dm:document"]["bibliography"]["reference"]:
        print biblio_ref_item.keys()

    print ""
    print xml_dict["dm:document"]["model"]["@name"]

    return self.doc



  def _process_data_type_element(self, item):
    data_type = nodes.DataType()
    logger = logging.getLogger(self.__class__.__name__)

    data_type.set_name(item["@name"])
    logger.debug("Processing DataType Element [{}]".format(item["@name"]))

    data_type.set_base(item.get("@base", ""))
    data_type.set_status(item.get("@status", "current"))
    data_type.set_description(item.get("description", "[Description not provided]"))

    ### TODO: check to see if there is a list element, then process it like a normal list

    # If it doesn't have a base then it has a type;
    #  If it does have a base then it shouldn't have a type, but could have other facets
    if "@base" in item:
      ### TODO: Should this combine the following facets with the Base's Data Type details?
      # generic function to read other facets: size, instanceRef, pathRef, range, enumeration, enumerationRef, pattern, units
      pass
    else:
      data_type.set_type(self._process_data_types(item))

    return data_type




  def _process_data_types(self, item):
    type_facet = None
    logger = logging.getLogger(self.__class__.__name__)

    if "base64" in item:
      type_facet = nodes.Base64Type()
      logger.debug("- DataType Element is a \"base64\" type")
      if item["base64"] is not None:
        if "size" in item["base64"]:
          self._process_size_facet(type_facet, item["base64"]["size"])
    elif "boolean" in item:
      type_facet = nodes.BooleanType()
      logger.debug("- DataType Element is a \"boolean\" type")
    elif "dateTime" in item: 
      type_facet = nodes.DateTimeType() 
      logger.debug("- DataType Element is a \"dateTime\" type")
    elif "hexBinary" in item: 
      type_facet = nodes.HexBinaryType() 
      logger.debug("- DataType Element is a \"hexBinary\" type")
      if item["hexBinary"] is not None:
        if "size" in item["hexBinary"]:
          self._process_size_facet(type_facet, item["hexBinary"]["size"])
    elif "int" in item:
      type_facet = nodes.NumericType("int")
      logger.debug("- DataType Element is an \"int\" type")
      if item["int"] is not None:
        if "range" in item["int"]:
          self.process_range_facet(type_facet, item["int"]["range"])
        if "units" in item["int"]:
          self.process_units_facet(type_facet, item["int"]["units"])
    elif "long" in item:
      type_facet = nodes.NumericType("long")
      logger.debug("- DataType Element is a \"long\" type")
      if item["long"] is not None:
        if "range" in item["long"]:
          self.process_range_facet(type_facet, item["long"]["range"])
        if "units" in item["long"]:
          self.process_units_facet(type_facet, item["long"]["units"])
    elif "string" in item:
      type_facet = nodes.StringType()
      logger.debug("- DataType Element is a \"string\" type")
      if item["string"] is not None:
        if "pathRef" in item["string"]:
          self._process_path_ref_facet(type_facet, item["string"]["pathRef"])
        if "enumerationRef" in item["string"]:
          self._process_enum_ref_facet(type_facet, item["string"]["enumerationRef"])
        if "enumeration" in item["string"]:
          self._process_enumeration_facet(type_facet, item["string"]["enumeration"])
        if "size" in item["string"]:
          self._process_size_facet(type_facet, item["string"]["size"])
        if "pattern" in item["string"]:
          self._process_pattern_facet(type_facet, item["string"]["pattern"])
    elif "unsignedInt" in item:
      type_facet = nodes.NumericType("unsignedInt")
      logger.debug("- DataType Element is an \"unsignedInt\" type")
      if item["unsignedInt"] is not None:
        if "range" in item["unsignedInt"]:
          self.process_range_facet(type_facet, item["unsignedInt"]["range"])
        if "units" in item["unsignedInt"]:
          self.process_units_facet(type_facet, item["unsignedInt"]["units"])
    elif "unsignedLong" in item:
      type_facet = nodes.NumericType("unsignedLong")
      logger.debug("- DataType Element is an \"unsignedLong\" type")
      if item["unsignedLong"] is not None:
        if "range" in item["unsignedLong"]:
          self.process_range_facet(type_facet, item["unsignedLong"]["range"])
        if "units" in item["unsignedLong"]:
          self.process_units_facet(type_facet, item["unsignedLong"]["units"])
    else:
      logger.error("Data Type expected and not found")

    return type_facet



  def _process_size_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple patters then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        a_size = self._create_size_facet(list_item)
        logger.debug("-- Adding Size: minLength={}, maxLength={}".format(a_size.get_min_length(), a_size.get_max_length()))
        type_facet.add_size(a_size)
    else:
      a_size = self._create_size_facet(item)
      logger.debug("-- Adding Size: minLength={}, maxLength={}".format(a_size.get_min_length(), a_size.get_max_length()))
      type_facet.add_size(a_size)


  def _create_size_facet(self, item):
    a_size = nodes.Size()
    a_size.set_min_length(item.get("@minLength", None))
    a_size.set_max_length(item.get("@maxLength", None))
    if "description" in item:
      a_size.set_description(item["description"])

    return a_size


  ### NOTE: instanceRef is not implemented as I don't believe that it is used
  

  def _process_path_ref_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple instances then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        a_path_ref = self._create_path_ref_facet(list_item)
        logger.debug("-- Adding Path Reference: {}/{}".format(a_path_ref.get_target_parent(), a_path_ref.get_target_type()))
        type_facet.add_path_ref(a_path_ref)
    else:
      a_path_ref = self._create_path_ref_facet(item)
      logger.debug("-- Adding Path Reference: {}/{}".format(a_path_ref.get_target_parent(), a_path_ref.get_target_type()))
      type_facet.add_path_ref(a_path_ref)


  def _create_path_ref_facet(self, item):
    a_path_ref = nodes.PathRef()
    a_path_ref.set_ref_type(item.get("@refType", ""))
    a_path_ref.set_target_parent(item.get("@targetParent", ""))
    a_path_ref.set_target_parent_scope(item.get("@targetParentScope", ""))
    a_path_ref.set_target_type(item.get("@targetType", ""))
    a_path_ref.set_target_data_type(item.get("@targetDataType", ""))
    if "description" in item:
      a_path_ref.set_description(item["description"])

    return a_path_ref

  

  def _process_range_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple patters then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        a_range = self._create_range_facet(list_item)
        logger.debug("-- Adding Range: minInclusive={}, maxInclusive={}; step by {}"
          .format(a_range.get_min_inclusive(), a_range.get_max_inclusive(), a_range.get_step()))
        type_facet.add_range(a_range)
    else:
      a_range = self._create_range_facet(item)
      logger.debug("-- Adding Range: minInclusive={}, maxInclusive={}; step by {}"
        .format(a_range.get_min_inclusive(), a_range.get_max_inclusive(), a_range.get_step()))
      type_facet.add_range(a_range)


  def _create_range_facet(self, item):
    a_range = nodes.Range()
    a_range.set_step(item.get("@step", 1))
    a_range.set_min_inclusive(item.get("@minInclusive", None))
    a_range.set_max_inclusive(item.get("@maxInclusive", None))
    if "description" in item:
      a_range.set_description(item["description"])

    return a_range



  def _process_enumeration_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple instances then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        an_enum = self._create_enumeration_facet(list_item)
        logger.debug("-- Adding Enumeration: \"{}\"".format(an_enum.get_value()))
        type_facet.add_enumeration(an_enum)
    else:
      an_enum = self._create_enumeration_facet(item)
      logger.debug("-- Adding Enumeration: \"{}\"".format(an_enum.get_value()))
      type_facet.add_enumeration(an_enum)


  def _create_enumeration_facet(self, item):
    an_enum = nodes.Enumeration()
    an_enum.set_value(item["@value"])
    an_enum.set_code(item.get("@code", None))
    if "description" in item:
      an_enum.set_description(item["description"])

    return an_enum



  def _process_enumeration_ref_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple instances then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        an_enum_ref = self._create_enumeration_ref_facet(list_item)
        logger.debug("-- Adding Pattern: \"{}\"".format(an_enum_ref.target_param()))
        type_facet.add_enumeration_ref(an_enum_ref)
    else:
      an_enum_ref = self._create_enumeration_ref_facet(item)
      logger.debug("-- Adding Pattern: \"{}\"".format(an_enum_ref.target_param()))
      type_facet.add_enumeration_ref(an_enum_ref)


  def _create_enumeration_ref_facet(self, item):
    an_enum_ref = nodes.EnumerationRef()
    an_enum_ref.set_target_param(item["@targetParam"])
    an_enum_ref.set_target_param_scope(item.get("@targetParamScope", ""))
    an_enum_ref.set_null_value(item.get("@nullValue", ""))
    if "description" in item:
      an_enum_ref.set_description(item["description"])

    return an_enum_ref



  def _process_pattern_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple instances then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        a_pattern = self._create_pattern_facet(list_item)
        logger.debug("-- Adding Pattern: \"{}\"".format(a_pattern.get_value()))
        type_facet.add_pattern(a_pattern)
    else:
      a_pattern = self._create_pattern_facet(item)
      logger.debug("-- Adding Pattern: \"{}\"".format(a_pattern.get_value()))
      type_facet.add_pattern(a_pattern)


  def _create_pattern_facet(self, item):
    a_pattern = nodes.Pattern()
    a_pattern.set_value(item["@value"])
    if "description" in item:
      a_pattern.set_description(item["description"])

    return a_pattern



  def _process_units_facet(self, type_facet, item):
    logger = logging.getLogger(self.__class__.__name__)

    # NOTE: If there are multiple instances then they will be wrapped in a list, otherwise it won't
    if isinstance(item, list):
      for list_item in item:
        a_unit = self._create_unit_facet(list_item)
        logger.debug("-- Adding Pattern: \"{}\"".format(a_unit.get_value()))
        type_facet.add_unit(a_unit)
    else:
      a_unit = self._create_unit_facet(item)
      logger.debug("-- Adding Pattern: \"{}\"".format(a_unit.get_value()))
      type_facet.add_unit(a_unit)


  def _create_unit_facet(self, item):
    a_unit = nodes.Unit()
    a_unit.set_value(item["@value"])
    if "description" in item:
      a_unit.set_description(item["description"])

    return a_unit

