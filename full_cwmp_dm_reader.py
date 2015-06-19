#! /usr/bin/env python

"""
# File Name: full_cwmp_dm_reader.py
#
# Description: Full CWMP-DM XML Input Reader
#
# Functionality:
#  - Input Reader for Full CWMP-DM XML Files
#     This simplifies the implementation as it doesn't have to worry
#     about Import statements or Component Elements
#
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
        return "full-cwmp-dm"


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

        if "description" in xml_dict["dm:document"]:
            self.doc.set_description(xml_dict["dm:document"]["description"])

        # There are no Imports in a Full CWMP-DM XML File, so no need to process them

        # Process dataType elements in the document
        if "dataType" in xml_dict["dm:document"]:
            for data_type_item in xml_dict["dm:document"]["dataType"]:
                self.doc.add_data_type(self._process_data_type_element(data_type_item))

        # Process bibliography=>reference elements in the document
        if "bibliography" in xml_dict["dm:document"]:
            for biblio_ref_item in xml_dict["dm:document"]["bibliography"]["reference"]:
                self.doc.add_biblio_ref(self._process_biblio_ref(biblio_ref_item))

        # There are no Components in a Full CWMP-DM XML File, so no need to process them

        # There are no Parameters associated with the Model in a Full CWMP-DM XML File,
        #   so no need to look for them

        # There is only ever a single Object associated with the Model in a Full CWMP-DM XML File,
        #   and it is the Root Data Model Object (Device:2.9, Device:1.7, etc.) - so no need to look
        #   for more than that
        data_model_type = "Root"
        root_data_model = self.doc.get_model()
        model_item = xml_dict["dm:document"]["model"]

        # Process the Model's Attributes
        root_data_model.set_name(model_item["@name"])

        if "@base" in model_item:
            root_data_model.set_base(model_item["@base"])

        if "@isService" in model_item:
            data_model_type = "Service"
            root_data_model.set_is_service(model_item["@isService"])

        # Process the Model's Description (if it is present)
        if "description" in model_item:
            root_data_model.set_description(model_item["description"])

        logger.debug(
            "Processing {} {} Data Model".format(root_data_model.get_name(), data_model_type))

        # There won't be any Parameters associated with the Model in a Full CWMP-DM XML

        # Process the Model's Objects
        for object_item in model_item["object"]:
            root_data_model.add_model_object(self._process_object_element(object_item))

        # Process the Model's Profiles
        for profile_item in model_item["profile"]:
            root_data_model.add_profile(self._process_profile(profile_item))

        return self.doc



    def _process_data_type_element(self, item):
        """Internal method to process the DataType Element"""
        data_type = nodes.DataType()
        logger = logging.getLogger(self.__class__.__name__)

        data_type.set_name(item["@name"])
        logger.debug("Processing DataType Element [{}]".format(item["@name"]))

        if "@base" in item:
            data_type.set_base(item["@base"])

        if "@status" in item:
            data_type.set_status(item["@status"])

        if "description" in item:
            data_type.set_description(item["description"])

        if "list" in item:
            data_type.set_list_element(self._process_list_facet(item["list"]))

        # If it doesn't have a base then it has a type;
        #  If it does have a base then it shouldn't have a type, but could have other facets
        if "@base" in item:
            logger.debug("- Element is a \"{}\" type".format(data_type.get_base()))
            self._process_data_type_facets(data_type, item)
        else:
            data_type.set_type_element(self._process_type_element(item))

        return data_type




    def _process_type_element(self, item):
        """Internal method to process the Type Elements: string, hexBinary, etc."""
        type_facet = None
        logger = logging.getLogger(self.__class__.__name__)

        if "base64" in item:
            type_facet = nodes.Base64Type()
            logger.debug("- Element is a \"base64\" type")
            if item["base64"] is not None:
                if "size" in item["base64"]:
                    size_facet_list = self._process_size_facets(item["base64"]["size"])
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
                    size_facet_list = self._process_size_facets(item["hexBinary"]["size"])
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
                        type_facet.add_path_ref(path_ref_facet)
                if "enumerationRef" in item["string"]:
                    enumeration_ref_facet_list = self._process_enumeration_ref_facets(item["string"]["enumerationRef"])
                    for enumeration_ref_facet in enumeration_ref_facet_list:
                        type_facet.add_enumeration_ref(enumeration_ref_facet)
                if "enumeration" in item["string"]:
                    enumeration_facet_list = self._process_enumeration_facets(item["string"]["enumeration"])
                    for enumeration_facet in enumeration_facet_list:
                        type_facet.add_enumeration(enumeration_facet)
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

        return type_facet



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

        a_list = nodes.ListFacet()

        if item is not None:
            if "@minItems" in item:
                a_list.set_min_items(item["@minItems"])

            if "@maxItems" in item:
                a_list.set_max_items(item["@maxItems"])

            if "@nestedBrackets" in item:
                a_list.set_nested_brackets(item["@nestedBrackets"])

            if "description" in item:
                a_list.set_description(item["description"])

            logger.debug(
                "- Element is a List: minItems={}, maxItems={}"
                .format(a_list.get_min_items(), a_list.get_max_items()))

            if "size" in item:
                size_facet_list = self._process_size_facets(item["size"])
                for size_facet in size_facet_list:
                    a_list.add_size(size_facet)
        else:
            logger.debug("- Element is a List: minItems=0, maxItems=\"unbounded\"")

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

        if item is not None:
            if "@minLength" in item:
                a_size.set_min_length(item["@minLength"])

            if "@maxLength" in item:
                a_size.set_max_length(item["@maxLength"])

            if "description" in item:
                a_size.set_description(item["description"])

        return a_size


    ### instanceRef is not implemented as I don't believe that it is used


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
                logger.debug(
                    "-- Adding Enumeration Ref to: {}".format(an_enum_ref.get_target_param()))
                enumeration_ref_facet_list.append(an_enum_ref)
        else:
            an_enum_ref = self._create_enumeration_ref_facet(item)
            logger.debug("-- Adding Enumeation Ref to: {}".format(an_enum_ref.get_target_param()))
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
                logger.debug("-- Adding Units: \"{}\"".format(a_unit.get_value()))
                units_facet_list.append(a_unit)
        else:
            a_unit = self._create_unit_facet(item)
            logger.debug("-- Adding Units: \"{}\"".format(a_unit.get_value()))
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

        logger.debug("Processing Bibliography Reference: \"{}\"".format(a_ref.get_name()))

        if "hyperlink" in item:
            if isinstance(item["hyperlink"], list):
                for hyperlink_item in item["hyperlink"]:
                    a_ref.add_hyperlink(hyperlink_item)
                    logger.debug("- Adding Hyperlink: \"{}\"".format(hyperlink_item))
            else:
                a_ref.add_hyperlink(item["hyperlink"])
                logger.debug("- Adding Hyperlink: \"{}\"".format(item["hyperlink"]))

        return a_ref



    def _process_object_element(self, item):
        """Internal method to process the Object Element"""
        a_model_obj = nodes.ModelObject()
        logger = logging.getLogger(self.__class__.__name__)

        # In a Full CWMP-DM XML, Objects always have a @name, @access, @minEntries, and @maxEntries
        a_model_obj.set_name(item["@name"])
        a_model_obj.set_access(item["@access"])
        a_model_obj.set_min_entries(item["@minEntries"])
        a_model_obj.set_max_entries(item["@maxEntries"])

        # In a Full CWMP-DM XML, Objects never have a @base
        if "@base" in item:
            a_model_obj.set_base(item["@base"])

        if "@numEntriesParameter" in item:
            a_model_obj.set_num_entries_parameter(item["@numEntriesParameter"])

        if "@enableParameter" in item:
            a_model_obj.set_enable_parameter(item["@enableParameter"])

        if "description" in item:
            a_model_obj.set_description(item["description"])

        # In a Full CWMP-DM XML, Objects always have a @name and @access
        logger.debug(
            "Processing Object: \"{}\" with \"{}\" Access"
            .format(a_model_obj.get_name(), a_model_obj.get_access))

        # Process the Object's Unique Keys, if they are present
        if "uniqueKey" in item:
            if isinstance(item["uniqueKey"], list):
                for unique_key_item in item["uniqueKey"]:
                    a_model_obj.add_unique_key(self._process_unique_key(unique_key_item))
            else:
                a_model_obj.add_unique_key(self._process_unique_key(item["uniqueKey"]))

        # Process the Object's Parameters, if they are present
        if "parameter" in item:
            if isinstance(item["parameter"], list):
                for parameter_item in item["parameter"]:
                    a_model_obj.add_parameter(self._process_parameter(parameter_item))
            else:
                a_model_obj.add_parameter(self._process_parameter(item["parameter"]))

        # Validate the Unique Key Parameter References
        for unique_key_instance in a_model_obj.get_unique_keys():
            for unique_key_param_ref in unique_key_instance.get_parameter_refs():
                if not a_model_obj.has_parameter(unique_key_param_ref):
                    logger.warning(
                        "Unique Key for Object {} References {} Parameter that can't be found"
                        .format(a_model_obj.get_name(), unique_key_param_ref))

        return a_model_obj



    def _process_unique_key(self, item):
        """Internal method to process the Unique Key Element"""
        param_ref_list = []
        a_unique_key = nodes.UniqueKey()
        logger = logging.getLogger(self.__class__.__name__)

        if "@functional" in item:
            a_unique_key.set_functional(item["@functional"])

        if isinstance(item["parameter"], list):
            for parameter_item in item["parameter"]:
                param_ref = parameter_item["@ref"]
                param_ref_list.append(param_ref)
                a_unique_key.add_parameter_ref(param_ref)
        else:
            param_ref = item["parameter"]["@ref"]
            param_ref_list.append(param_ref)
            a_unique_key.add_parameter_ref(param_ref)

        logger.debug("- Processing Unique Key: \"{}\"".format(", ".join(param_ref_list)))

        return a_unique_key



    def _process_parameter(self, item):
        """Internal method to process the Parameter Element"""
        a_param = nodes.Parameter()
        logger = logging.getLogger(self.__class__.__name__)

        # In a Full CWMP-DM XML, Parameters always have a @name, @access, and syntax
        a_param.set_name(item["@name"])
        a_param.set_access(item["@access"])

        # In a Full CWMP-DM XML, Parameters never have a @base
        if "@base" in item:
            a_param.set_base(item["@base"])

        if "@activeNotify" in item:
            a_param.set_active_notify(item["@activeNotify"])

        if "@forcedInform" in item:
            a_param.set_forced_inform(item["@forcedInform"])

        if "description" in item:
            a_param.set_description(item["description"])

        # In a Full CWMP-DM XML, Parameters always have a @name and @access
        logger.debug(
            "Processing Parameter: \"{}\" with \"{}\" Access"
            .format(a_param.get_name(), a_param.get_access))

        a_param.set_syntax(self._process_syntax(a_param.get_name(), item["syntax"]))

        return a_param



    def _process_syntax(self, param_name, item):
        """Internal method to process the Syntax Element"""
        a_syntax = nodes.Syntax()
        logger = logging.getLogger(self.__class__.__name__)

        if "@hidden" in item:
            a_syntax.set_hidden(item["@hidden"])

        if "@command" in item:
            a_syntax.set_command(item["@command"])

        # In a Full CWMP-DM XML, Parameters always have a @name
        logger.debug(
            "- Processing Syntax: hidden=\"{}\", command=\"{}\""
            .format(a_syntax.get_hidden(), a_syntax.get_command()))

        if "list" in item:
            a_syntax.set_list_element(self._process_list_facet(item["list"]))

        # A Syntax Element will either have a DataType or a Type Element (string, int, etc.)
        if "dataType" in item:
            data_type_ref_name = item["dataType"]["@ref"]
            a_syntax.set_data_type_ref(data_type_ref_name)

            if not self.doc.has_data_type(data_type_ref_name):
                logger.warning(
                    "Parameter {} References {} Data Type that can't be found"
                    .format(param_name, data_type_ref_name))
        else:
            a_syntax.set_type_element(self._process_type_element(item))

        if "default" in item:
            a_syntax.set_default(self._process_default(item["default"]))

        return a_syntax



    def _process_default(self, item):
        """Internal method to process the Default Element"""
        a_default = nodes.DefaultFacet()
        logger = logging.getLogger(self.__class__.__name__)

        a_default.set_type_attribute(item["@type"])
        a_default.set_value(item["@value"])

        if "description" in item:
            a_default.set_description(item["description"])

        logger.debug(
            "- Processing Default: type=\"{}\", value=\"{}\""
            .format(a_default.get_type_attribute(), a_default.get_value()))

        return a_default



    def _process_profile(self, item):
        """Internal method to process the Profile Element"""
        a_profile = nodes.Profile()
        logger = logging.getLogger(self.__class__.__name__)

        a_profile.set_name(item["@name"])

        if "@base" in item:
            a_profile.set_base(item["@base"])

        if "@extends" in item:
            a_profile.set_extends(item["@extends"])

        if "@minVersion" in item:
            a_profile.set_min_version(item["@minVersion"])

        if "description" in item:
            a_profile.set_description(item["description"])

        logger.debug("Processing Profile: \"{}\"".format(a_profile.get_name()))

        if "object" in item:
            if isinstance(item["object"], list):
                for object_item in item["object"]:
                    a_profile.add_profile_object(self._process_profile_object(object_item))
            else:
                a_profile.add_profile_object(self._process_profile_object(item["object"]))

        if "parameter" in item:
            if isinstance(item["parameter"], list):
                for parameter_item in item["parameter"]:
                    a_profile.add_profile_parameter(self._process_profile_parameter(parameter_item))
            else:
                a_profile.add_profile_parameter(self._process_profile_parameter(item["parameter"]))

        return a_profile



    def _process_profile_object(self, item):
        """Internal method to process the Profile's Object Element"""
        a_profile_obj = nodes.ProfileObject()
        logger = logging.getLogger(self.__class__.__name__)

        # A Profile Object will always have an @ref and @requirement
        a_profile_obj.set_ref(item["@ref"])
        a_profile_obj.set_requirement(item["@requirement"])

        if "description" in item:
            a_profile_obj.set_description(item["description"])

        logger.debug(
            "- Adding Profile Object: \"{}\" with \"{}\" Access"
            .format(a_profile_obj.get_ref(), a_profile_obj.get_requirement()))

        if "parameter" in item:
            if isinstance(item["parameter"], list):
                for parameter_item in item["parameter"]:
                    a_profile_obj.add_profile_parameter(self._process_profile_parameter(parameter_item))
            else:
                a_profile_obj.add_profile_parameter(self._process_profile_parameter(item["parameter"]))

        return a_profile_obj



    def _process_profile_parameter(self, item):
        """Internal method to process the Profile's Object Element"""
        a_profile_param = nodes.ProfileParameter()
        logger = logging.getLogger(self.__class__.__name__)

        # A Profile Object will always have an @ref and @requirement
        a_profile_param.set_ref(item["@ref"])
        a_profile_param.set_requirement(item["@requirement"])

        if "description" in item:
            a_profile_param.set_description(item["description"])

        logger.debug(
            "-- Adding Profile Parameter: \"{}\" with \"{}\" Access"
            .format(a_profile_param.get_ref(), a_profile_param.get_requirement()))

        return a_profile_param

