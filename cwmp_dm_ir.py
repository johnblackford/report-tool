#! /usr/bin/env python

"""
## File Name: cwmp_dm_ir.py
##
## Description: CWMP-DM XML Input Reader
##
## Functionality:
##  - Input Reader for CWMP-DM XML Format
##
"""


import nodes
import logging
import xmltodict

from abstract_classes import AbstractInputReader



class DataModelInputReader(AbstractInputReader):
    """CWMP-DM XML Input Reader"""

    def __init__(self):
        """Initialize internal variables"""
        self.doc = nodes.Document()



    def get_input_format(self):
        """Return the appropriate input format"""
        return "cwmp-dm"


    def process_properties(self, props):
        """No properties to retrieve"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("This Input Reader has no Properties")



    def read(self, filename):
        """Read the CWMP-DM XML file and process the contents"""
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
        logger.debug(
            "Processing Document Element: spec attribute, file attribute, and description element")
        self.doc.set_spec(xml_dict["dm:document"].get("@spec", "UNKNOWN"))
        self.doc.set_file(xml_dict["dm:document"].get("@file", "UNKNOWN"))
        self.doc.set_description(
            xml_dict["dm:document"].get("description", "[Description not provided]"))

        ### TODO: Handle Imports

        # Process dataType elements in the document
        for data_type_item in xml_dict["dm:document"]["dataType"]:
            self.doc.add_data_type(self._process_data_type_element(data_type_item))

        print ""
        if "bibliography" in xml_dict["dm:document"]:
            for biblio_ref_item in xml_dict["dm:document"]["bibliography"]["reference"]:
                self.doc.add_biblio_ref(self._process_biblio_ref(biblio_ref_item))

        ### TODO: Work on the Model next
        print ""
        print xml_dict["dm:document"]["model"]["@name"]

        return self.doc



    def _process_data_type_element(self, item):
        """Internal method to process the DataType Element"""
        data_type = nodes.DataType()
        logger = logging.getLogger(self.__class__.__name__)

        data_type.set_name(item["@name"])
        logger.debug("Processing DataType Element [{}]".format(item["@name"]))

        data_type.set_base(item.get("@base", ""))
        data_type.set_status(item.get("@status", "current"))
        data_type.set_description(item.get("description", "[Description not provided]"))

        if "list" in item:
            data_type.set_list(self._process_list_facet(item["list"]))

        # If it doesn't have a base then it has a type;
        #  If it does have a base then it shouldn't have a type, but could have other facets
        if "@base" in item:
            logger.debug("- Element is a \"{}\" type".format(data_type.get_base()))
            self._process_data_type_facets(data_type, item)
        else:
            self._process_data_type(data_type, item)

        return data_type




    def _process_data_type(self, data_type, item):
        """Internal method to process the type for this DataType"""
        type_facet = None
        logger = logging.getLogger(self.__class__.__name__)

        if "base64" in item:
            type_facet = nodes.Base64Type()
            logger.debug("- Element is a \"base64\" type")
            if item["base64"] is not None:
                if "size" in item["base64"]:
                    size_facet_list = self._process_size_facets(item["string"]["size"])
                    for size_facet in size_facet_list:
                        type_facet.add_size(size_facet)
        elif "boolean" in item:
            type_facet = nodes.BooleanType()
            logger.debug("- Element is a \"boolean\" type")
        elif "dateTime" in item:
            type_facet = nodes.DateTimeType()
            logger.debug("- Element is a \"dateTime\" type")
        elif "hexBinary" in item:
            type_facet = nodes.HexBinaryType()
            logger.debug("- Element is a \"hexBinary\" type")
            if item["hexBinary"] is not None:
                if "size" in item["hexBinary"]:
                    size_facet_list = self._process_size_facets(item["string"]["size"])
                    for size_facet in size_facet_list:
                        type_facet.add_size(size_facet)
        elif "int" in item:
            type_facet = nodes.NumericType("int")
            logger.debug("- Element is an \"int\" type")
            if item["int"] is not None:
                if "range" in item["int"]:
                    range_facet_list = self._process_range_facets(item["int"]["range"])
                    for range_facet in range_facet_list:
                        type_facet.add_range(range_facet)
                if "units" in item["int"]:
                    units_facet_list = self._process_units_facets(item["int"]["units"])
                    for units_facet in units_facet_list:
                        type_facet.add_unit(units_facet)
        elif "long" in item:
            type_facet = nodes.NumericType("long")
            logger.debug("- Element is a \"long\" type")
            if item["long"] is not None:
                if "range" in item["long"]:
                    range_facet_list = self._process_range_facets(item["long"]["range"])
                    for range_facet in range_facet_list:
                        type_facet.add_range(range_facet)
                if "units" in item["long"]:
                    units_facet_list = self._process_units_facets(item["long"]["units"])
                    for units_facet in units_facet_list:
                        type_facet.add_unit(units_facet)
        elif "string" in item:
            type_facet = nodes.StringType()
            logger.debug("- Element is a \"string\" type")
            if item["string"] is not None:
                if "pathRef" in item["string"]:
                    path_ref_facet_list = self._process_path_ref_facets(item["string"]["pathRef"])
                    for path_ref_facet in path_ref_facet_list:
                        data_type.add_path_ref_facet(path_ref_facet)
                if "enumerationRef" in item["string"]:
                    enumeration_ref_facet_list = self._process_enumeration_ref_facets(item["string"]["enumerationRef"])
                    for enumeration_ref_facet in enumeration_ref_facet_list:
                        type_facet.add_enumeration_ref(enumeration_ref_facet)
                if "enumeration" in item["string"]:
                    enumeration_facet_list = self._process_enumeration_facets(item["string"]["enumeration"])
                    for enumeration_facet in enumeration_facet_list:
                        data_type.add_enumeration(enumeration_facet)
                if "size" in item["string"]:
                    size_facet_list = self._process_size_facets(item["string"]["size"])
                    for size_facet in size_facet_list:
                        type_facet.add_size(size_facet)
                if "pattern" in item["string"]:
                    pattern_facet_list = self._process_pattern_facets(item["string"]["pattern"])
                    for pattern_facet in pattern_facet_list:
                        type_facet.add_pattern(pattern_facet)
        elif "unsignedInt" in item:
            type_facet = nodes.NumericType("unsignedInt")
            logger.debug("- Element is an \"unsignedInt\" type")
            if item["unsignedInt"] is not None:
                if "range" in item["unsignedInt"]:
                    range_facet_list = self._process_range_facets(item["unsignedInt"]["range"])
                    for range_facet in range_facet_list:
                        type_facet.add_range(range_facet)
                if "units" in item["unsignedInt"]:
                    units_facet_list = self._process_units_facets(item["unsignedInt"]["units"])
                    for units_facet in units_facet_list:
                        type_facet.add_unit(units_facet)
        elif "unsignedLong" in item:
            type_facet = nodes.NumericType("unsignedLong")
            logger.debug("- Element is an \"unsignedLong\" type")
            if item["unsignedLong"] is not None:
                if "range" in item["unsignedLong"]:
                    range_facet_list = self._process_range_facets(item["unsignedLong"]["range"])
                    for range_facet in range_facet_list:
                        type_facet.add_range(range_facet)
                if "units" in item["unsignedLong"]:
                    units_facet_list = self._process_units_facets(item["unsignedLong"]["units"])
                    for units_facet in units_facet_list:
                        type_facet.add_unit(units_facet)
        else:
            logger.error("Data Type expected and not found")

        data_type.set_type(type_facet)



    def _process_data_type_facets(self, data_type, item):
        """Internal method to process the facet Elements associated with the DataType"""
        if "size" in item:
            size_facet_list = self._process_size_facets(item["size"])
            for size_facet in size_facet_list:
                data_type.add_size(size_facet)

        if "pathRef" in item:
            path_ref_facet_list = self._process_path_ref_facets(item["pathRef"])
            for path_ref_facet in path_ref_facet_list:
                data_type.add_path_ref(path_ref_facet)

        if "range" in item:
            range_facet_list = self._process_range_facets(item["range"])
            for range_facet in range_facet_list:
                data_type.add_range(range_facet)

        if "enumeration" in item:
            enumeration_facet_list = self._process_enumeration_facets(item["enumeration"])
            for enumeration_facet in enumeration_facet_list:
                data_type.add_enumeration(enumeration_facet)

        if "enumerationRef" in item:
            enumeration_ref_facet_list = self._process_enumeration_ref_facets(item["enumerationRef"])
            for enumeration_ref_facet in enumeration_ref_facet_list:
                data_type.add_enumeration_ref(enumeration_ref_facet)

        if "pattern" in item:
            pattern_facet_list = self._process_pattern_facets(item["pattern"])
            for pattern_facet in pattern_facet_list:
                data_type.add_pattern(pattern_facet)

        if "units" in item:
            unit_facet_list = self._process_units_facets(item["units"])
            for unit_facet in unit_facet_list:
                data_type.add_unit(unit_facet)



    def _process_list_facet(self, item):
        """Internal method to process the List Facet"""
        logger = logging.getLogger(self.__class__.__name__)

        a_list = nodes.List()
        a_list.set_min_items(item.get("@minItems", None))
        a_list.set_max_items(item.get("@maxItems", None))
        a_list.set_nested_brackets(item.get("@nestedBrackets", None))
        a_list.set_description(item.get("description", ""))
        logger.debug(
            "- Element is a List: minItems={}, maxItems={}"
            .format(a_list.get_min_items(), a_list.get_max_items()))

        if "size" in item:
            size_facet_list = self._process_size_facets(item["size"])
            for size_facet in size_facet_list:
                a_list.add_size(size_facet)

        return a_list



    def _process_size_facets(self, item):
        """Internal method to process the Size Facet"""
        size_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple patters then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                a_size = self._create_size_facet(list_item)
                logger.debug(
                    "-- Adding Size: minLength={}, maxLength={}"
                    .format(a_size.get_min_length(), a_size.get_max_length()))
                size_facet_list.append(a_size)
        else:
            a_size = self._create_size_facet(item)
            logger.debug(
                "-- Adding Size: minLength={}, maxLength={}"
                .format(a_size.get_min_length(), a_size.get_max_length()))
            size_facet_list.append(a_size)

        return size_facet_list


    def _create_size_facet(self, item):
        """Internal method to create a Size node object"""
        a_size = nodes.Size()
        a_size.set_min_length(item.get("@minLength", None))
        a_size.set_max_length(item.get("@maxLength", None))
        if "description" in item:
            a_size.set_description(item["description"])

        return a_size


    ### NOTE: instanceRef is not implemented as I don't believe that it is used


    def _process_path_ref_facets(self, item):
        """Internal method to process the PathRef Facet"""
        path_ref_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple instances then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                a_path_ref = self._create_path_ref_facet(list_item)
                logger.debug(
                    "-- Adding Path Reference: {}/{}"
                    .format(a_path_ref.get_target_parent(), a_path_ref.get_target_type()))
                path_ref_facet_list.append(a_path_ref)
        else:
            a_path_ref = self._create_path_ref_facet(item)
            logger.debug(
                "-- Adding Path Reference: {}/{}"
                .format(a_path_ref.get_target_parent(), a_path_ref.get_target_type()))
            path_ref_facet_list.append(a_path_ref)

        return path_ref_facet_list


    def _create_path_ref_facet(self, item):
        """Internal method to create a PathRef node object"""
        a_path_ref = nodes.PathRef()
        a_path_ref.set_ref_type(item.get("@refType", ""))
        a_path_ref.set_target_parent(item.get("@targetParent", ""))
        a_path_ref.set_target_parent_scope(item.get("@targetParentScope", ""))
        a_path_ref.set_target_type(item.get("@targetType", ""))
        a_path_ref.set_target_data_type(item.get("@targetDataType", ""))
        if "description" in item:
            a_path_ref.set_description(item["description"])

        return a_path_ref



    def _process_range_facets(self, item):
        """Internal method to process the Range Facet"""
        range_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple patters then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                a_range = self._create_range_facet(list_item)
                logger.debug(
                    "-- Adding Range: minInclusive={}, maxInclusive={}; step by {}"
                    .format(
                        a_range.get_min_inclusive(),
                        a_range.get_max_inclusive(),
                        a_range.get_step()))
                range_facet_list.append(a_range)
        else:
            a_range = self._create_range_facet(item)
            logger.debug(
                "-- Adding Range: minInclusive={}, maxInclusive={}; step by {}"
                .format(
                    a_range.get_min_inclusive(),
                    a_range.get_max_inclusive(),
                    a_range.get_step()))
            range_facet_list.append(a_range)

        return range_facet_list


    def _create_range_facet(self, item):
        """Internal method to create a Range node object"""
        a_range = nodes.Range()
        a_range.set_step(item.get("@step", 1))
        a_range.set_min_inclusive(item.get("@minInclusive", None))
        a_range.set_max_inclusive(item.get("@maxInclusive", None))
        if "description" in item:
            a_range.set_description(item["description"])

        return a_range



    def _process_enumeration_facets(self, item):
        """Internal method to process the Enumeration Facet"""
        enumeration_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple instances then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                an_enum = self._create_enumeration_facet(list_item)
                logger.debug("-- Adding Enumeration: \"{}\"".format(an_enum.get_value()))
                enumeration_facet_list.append(an_enum)
        else:
            an_enum = self._create_enumeration_facet(item)
            logger.debug("-- Adding Enumeration: \"{}\"".format(an_enum.get_value()))
            enumeration_facet_list.append(an_enum)

        return enumeration_facet_list


    def _create_enumeration_facet(self, item):
        """Internal method to create an Enumeration node object"""
        an_enum = nodes.Enumeration()
        an_enum.set_value(item["@value"])
        an_enum.set_code(item.get("@code", None))
        if "description" in item:
            an_enum.set_description(item["description"])

        return an_enum



    def _process_enumeration_ref_facets(self, item):
        """Internal method to process the EnumerationRef Facet"""
        enumeration_ref_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple instances then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                an_enum_ref = self._create_enumeration_ref_facet(list_item)
                logger.debug("-- Adding Pattern: \"{}\"".format(an_enum_ref.target_param()))
                enumeration_ref_facet_list.append(an_enum_ref)
        else:
            an_enum_ref = self._create_enumeration_ref_facet(item)
            logger.debug("-- Adding Pattern: \"{}\"".format(an_enum_ref.target_param()))
            enumeration_ref_facet_list.append(an_enum_ref)

        return enumeration_ref_facet_list


    def _create_enumeration_ref_facet(self, item):
        """ Internal method to create an EnumerationRef node object"""
        an_enum_ref = nodes.EnumerationRef()
        an_enum_ref.set_target_param(item["@targetParam"])
        an_enum_ref.set_target_param_scope(item.get("@targetParamScope", ""))
        an_enum_ref.set_null_value(item.get("@nullValue", ""))
        if "description" in item:
            an_enum_ref.set_description(item["description"])

        return an_enum_ref



    def _process_pattern_facets(self, item):
        """Internal method to process the Pattern Facet"""
        pattern_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple instances then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                a_pattern = self._create_pattern_facet(list_item)
                logger.debug("-- Adding Pattern: \"{}\"".format(a_pattern.get_value()))
                pattern_facet_list.append(a_pattern)
        else:
            a_pattern = self._create_pattern_facet(item)
            logger.debug("-- Adding Pattern: \"{}\"".format(a_pattern.get_value()))
            pattern_facet_list.append(a_pattern)

        return pattern_facet_list


    def _create_pattern_facet(self, item):
        """Internal method to create a Pattern node object"""
        a_pattern = nodes.Pattern()
        a_pattern.set_value(item["@value"])
        if "description" in item:
            a_pattern.set_description(item["description"])

        return a_pattern



    def _process_units_facets(self, item):
        """Internal method to process the Units Facet"""
        units_facet_list = []
        logger = logging.getLogger(self.__class__.__name__)

        # If there are multiple instances then they will be wrapped in a list
        if isinstance(item, list):
            for list_item in item:
                a_unit = self._create_unit_facet(list_item)
                logger.debug("-- Adding Pattern: \"{}\"".format(a_unit.get_value()))
                units_facet_list.append(a_unit)
        else:
            a_unit = self._create_unit_facet(item)
            logger.debug("-- Adding Pattern: \"{}\"".format(a_unit.get_value()))
            units_facet_list.append(a_unit)

        return units_facet_list


    def _create_unit_facet(self, item):
        """Internal method to create a Unit node object"""
        a_unit = nodes.Unit()
        a_unit.set_value(item["@value"])
        if "description" in item:
            a_unit.set_description(item["description"])

        return a_unit



    def _process_biblio_ref(self, item):
        """Internal method to process the Reference Elements within a Bibliography element"""
        a_ref = nodes.Reference()
        logger = logging.getLogger(self.__class__.__name__)

        a_ref.set_name(item["name"])
        a_ref.set_title(item.get("title", ""))
        a_ref.set_organization(item.get("organization", ""))
        a_ref.set_category(item.get("category", ""))
        a_ref.set_date(item.get("date", ""))

        if "hyperlink" in item:
            if isinstance(item["hyperlink"], list):
                for hyperlink_item in item["hyperlink"]:
                    a_ref.add_hyperlink(hyperlink_item)
                    logger.debug("- Adding Hyperlink: \"{}\"".format(hyperlink_item))
            else:
                a_ref.add_hyperlink(item["hyperlink"])
                logger.debug("- Adding Hyperlink: \"{}\"".format(item["hyperlink"]))

        logger.debug("Processing Bibliography Reference: \"{}\"".format(a_ref.get_name()))

        return a_ref

