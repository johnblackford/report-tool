#! /usr/bin/env python

"""
# File Name: nodes.py
#
# Description: Objects for the Node Tree
#
"""

# FUTURE:
# We might need to treat description as an object since it has an @action attribute
#  But not right now as we are only supporting Full CWMP-DM XML Files


class Document(object):
    """Represents the Document Element:
        Attributes: spec("@spec"),
                    file_name("@file")
        Sub-Elements: description(String::"description"),
                      data_type_list(DataType[]::"dataType"),
                      biblio_ref_list(Reference[]::"bibliography"=>"reference")"""
    def __init__(self):
        """Initialize the Document"""
        self.spec = ""
        self.file_name = ""
        self.description = ""
        self.data_type_list = []
        self.data_type_dict = {}
        self.biblio_ref_list = []
        # FUTURE:
        # Eventually need to add in support for Components, but not now as we
        #  are just supporting Full CWMP-DM XML Files
        #
        # FUTURE:
        # The XSD calls out that multiple Model elements can be present, but
        #  we are using a single instance for now as we are just supporting
        #  Full CWMP-DM XML Files
        self.model = Model()


    def get_spec(self):
        return self.spec

    def set_spec(self, value):
        self.spec = value

    def get_file(self):
        return self.file_name

    def set_file(self, value):
        self.file_name = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value

    def add_data_type(self, item):
        """Add a DataType to the Document"""
        self.data_type_list.append(item)
        self.data_type_dict[item.get_name()] = item

    def get_data_types(self):
        """Retrieve the list of DataType instances"""
        return self.data_type_list

    def has_data_type(self, name):
        """Check to see if the requested DataType is present"""
        return name in self.data_type_dict

    def get_data_type(self, name):
        """Retrieve the requested DataType"""
        return self.data_type_dict[name]

    def add_biblio_ref(self, item):
        self.biblio_ref_list.append(item)

    def get_biblio_refs(self):
        return self.biblio_ref_list

    def get_model(self):
        """Retrieve the Model object"""
        return self.model



class DataType(object):
    """Represents the DataType Element:
        Attributes: name("@name"),
                    base("@base"),
                    status("@status"="current")
        Sub-Elements: description(String::"description"),
                      list_element(ListFacet::"list"),
                      type_element(Type::"type"),
                      size_list(SizeFacet[]::"size"),
                      path_ref_list(PathRef[]::"pathRef"),
                      range_list(RangeFacet[]::"range"),
                      enumeration_list(Enumeration[]::"enumeration"),
                      enumeration_ref_list(EnumerationRef[]::"enumerationRef"),
                      pattern_list(Pattern[]::"pattern"),
                      unit_list(Unit[]::"units")"""
    def __init__(self):
        """Initialize the DataType"""
        self.name = ""
        self.base = None
        self.status = "current"
        self.description = ""
        self.list_element = None
        self.type_element = None
        self.size_list = []
        self.path_ref_list = []
        self.range_list = []
        self.enumeration_list = []
        self.enumeration_ref_list = []
        self.pattern_list = []
        self.unit_list = []
        # FUTURE:
        # We may also want an Inferred Type that is a complete
        #  DataType (combines the base and this instance).
        #  But it would not have facet types outside of the type.
        #  So, it would probably be a separate object: InferredDataType
        #  DataType could also have a generate_inferred_data_type method


    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_base(self):
        return self.base

    def set_base(self, value):
        self.base = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value

    def get_type(self):
        return self.type_element

    def set_type(self, value):
        self.type_element = value

    def get_list(self):
        return self.list_element

    def set_list(self, value):
        self.list_element = value

    def add_size(self, item):
        self.size_list.append(item)

    def get_sizes(self):
        return self.size_list

    def add_path_ref(self, item):
        self.path_ref_list.append(item)

    def get_path_refs(self):
        return self.path_ref_list

    def add_range(self, item):
        self.range_list.append(item)

    def get_ranges(self):
        return self.range_list

    def add_enumeration(self, item):
        self.enumeration_list.append(item)

    def get_enumerations(self):
        return self.enumeration_list

    def add_enumeration_ref(self, item):
        self.enumeration_ref_list.append(item)

    def get_enumeration_refs(self):
        return self.enumeration_ref_list

    def add_pattern(self, item):
        self.pattern_list.append(item)

    def get_patterns(self):
        return self.pattern_list

    def add_unit(self, item):
        self.unit_list.append(item)

    def get_units(self):
        return self.unit_list



class Reference(object):
    """Represents the Reference Element:
        Sub-Elements: name(String::"name"),
                      title(String::"title"),
                      organization(String::"organization"),
                      category(String::"category"),
                      date(String::"date"),
                      hyperlink_list(String[]::"hyperlink")"""
    def __init__(self):
        """Initialize the Reference"""
        self.name = ""
        self.title = ""
        self.organization = ""
        self.category = ""
        self.date = ""
        self.hyperlink_list = []


    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_title(self):
        return self.title

    def set_title(self, value):
        self.title = value

    def get_organization(self):
        return self.organization

    def set_organization(self, value):
        self.organization = value

    def get_category(self):
        return self.category

    def set_category(self, value):
        self.category = value

    def get_date(self):
        return self.date

    def set_date(self, value):
        self.date = value

    def add_hyperlink(self, item):
        self.hyperlink_list.append(item)

    def get_hyperlinks(self):
        return self.hyperlink_list



class Model(object):
    """Represents a Model Element:
        Attributes: name("@name"),
                    base("@base"),
                    is_service("@isService"=False)
        Sub-Elements: description(String::"description"),
                      parameter_list(Parameter[]::"parameter"),
                      model_object_list(ModelObject[]::"object"),
                      profile_list(Profile[]::"profile")"""
    def __init__(self):
        """Initialize the Model"""
        self.name = ""
        self.base = None
        self.is_service = False
        self.description = ""
        # FUTURE:
        # A Model also can have Components
        self.parameter_list = []
        self.parameter_dict = {}
        self.model_object_list = []
        self.model_object_dict = {}
        self.profile_list = []
        self.profile_dict = {}


    def get_name(self):
        """Retrieve the Model's name"""
        return self.name

    def set_name(self, value):
        """Set the Model's name"""
        self.name = value

    def get_base(self):
        """Retrieve the Model's base"""
        return self.base

    def set_base(self, value):
        """Set the Model's base"""
        self.base = value

    def is_service_data_model(self):
        """If this Model is a Service Model then return True; Otherwise return False"""
        return self.is_service

    def get_is_service(self):
        """Retrieve the Model's is_service attribute"""
        return self.is_service

    def set_is_service(self, value):
        """Set the Model's is_service attribute"""
        self.is_service = value

    def get_description(self):
        """Retrieve the Model's description"""
        return self.description

    def set_description(self, value):
        """Set the Model's description"""
        self.description = value

    def add_parameter(self, item):
        """Add a Parameter to the Model"""
        self.parameter_list.append(item)

        # If the Parameter Element is based on a previously defined Parameter
        #  then the @base attribute will be populated instead of the @name,
        #  but there won't be a conflict in this Model as it is defined in
        #  another Model instance
        if item.get_name() is not None:
            self.parameter_dict[item.get_name()] = item
        else:
            self.parameter_dict[item.get_base()] = item

    def get_parameters(self):
        """Retrieve the Model's Parameters
           - only Parameters that are directly on the Model,
             not the ones that are on the Objects"""
        return self.parameter_list

    def has_parameter(self, name):
        """Check to see if the requested Model's Parameter is present"""
        return name in self.parameter_dict

    def get_parameter(self, name):
        """Retrieve the requested Model's Parameter List"""
        return self.parameter_dict[name]

    def add_model_object(self, item):
        """Add an Object to the Model"""
        self.model_object_list.append(item)

        # If the Object Element is based on a previously defined Object
        #  then the @base attribute will be populated instead of the @name,
        #  but there won't be a conflict in this Model as the @name Object
        #  is defined in another Model instance
        if item.get_name() is not None:
            self.model_object_dict[item.get_name()] = item
        else:
            self.model_object_dict[item.get_base()] = item

    def get_model_objects(self):
        """Retrieve the Model's Object List"""
        return self.model_object_list

    def has_model_object(self, name):
        """Check to see if the requested Model's Object is present"""
        return name in self.model_object_dict

    def get_model_object(self, name):
        """Retrieve the requested Model's Object"""
        return self.model_object_dict[name]

    def add_profile(self, item):
        """Add a Profile to the Model"""
        self.profile_list.append(item)
        self.profile_dict[item.get_name()] = item

    def get_profiles(self):
        """Retrieve the Model's Profiles"""
        return self.profile_list

    def has_profile(self, name):
        """Check to see if the requested Profile is present"""
        return name in self.profile_dict

    def get_profile(self, name):
        """Retrieve the requested Profile"""
        return self.profile_dict[name]



class ModelObject(object):
    """Represents an Object Element:
        Attributes: name("@name"),
                    base("@base"),
                    access("@access"),
                    min_entries("@minEntries"=1),
                    max_entries("@maxEntries"=1),
                    num_entries_parameter("@numEntriesParameter"),
                    enable_parameter("@enableParameter")
        Sub-Elements: description(String::"description"),
                      unique_key_list(UniqueKey[]::"uniqueKey"),
                      parameter_list(Parameter[]::"parameter")"""
    def __init__(self):
        """Initialize the Object"""
        self.name = None
        self.base = None
        self.access = None
        self.min_entries = 1
        self.max_entries = 1
        self.num_entries_parameter = None
        self.enable_parameter = None
        self.description = ""
        self.unique_key_list = []
        # FUTURE:
        # Objects can have a list of Component References (@path, @ref)
        self.parameter_list = []
        self.parameter_dict = {}


    def get_name(self):
        """Retrieve the Object's name attribute"""
        return self.name

    def set_name(self, value):
        """Set the Object's name attribute"""
        self.name = value

    def get_base(self):
        """Retrieve the Object's base attribute"""
        return self.base

    def set_base(self, value):
        """Set the Object's base attribute"""
        self.base = value

    def get_access(self):
        """Retrieve the Object's access attribute"""
        return self.access

    def set_access(self, value):
        """Set the Object's access attribute"""
        self.access = value

    def get_min_entries(self):
        """Retrieve the Object's minEntries attribute"""
        return self.min_entries

    def set_min_entries(self, value):
        """Set the Object's minEntries attribute"""
        self.min_entries = value

    def get_max_entries(self):
        """Retrieve the Object's maxEntries attribute"""
        return self.max_entries

    def set_max_entries(self, value):
        """Set the Object's maxEntries attribute"""
        self.max_entries = value

    def get_num_entries_parameter(self):
        """Retrieve the Object's numEntriesParameter Reference"""
        return self.num_entries_parameter

    def set_num_entries_parameter(self, value):
        """Set the Object's numEntriesParameter Reference"""
        self.num_entries_parameter = value

    def get_enable_parameter(self):
        """Retrieve the Object's enableParameter Reference"""
        return self.enable_parameter

    def set_enable_parameter(self, value):
        """Set the Object's enableParameter Reference"""
        self.enable_parameter = value

    def get_description(self):
        """Retrieve the Object's description element"""
        return self.description

    def set_description(self, value):
        """Set the Object's description element"""
        self.description = value

    def add_unique_key(self, item):
        """Add a Unique Key to this Parameter"""
        self.unique_key_list.append(item)

    def get_unique_keys(self):
        """Retrieve the Parameter's Unique Keys"""
        return self.unique_key_list

    def add_parameter(self, item):
        """Add a Parameter to the Object"""
        self.parameter_list.append(item)

        # If the Parameter Element is based on a previously defined Parameter
        #  then the @base attribute will be populated instead of the @name,
        #  but there won't be a conflict in this Model as it is defined in
        #  another Model instance
        if item.get_name() is not None:
            self.parameter_dict[item.get_name()] = item
        else:
            self.parameter_dict[item.get_base()] = item

    def get_parameters(self):
        """Retrieve the Object's Parameters
           - only Parameters that are directly associated with this Object,
             not the ones that are on Sub-Objects"""
        return self.parameter_list

    def has_parameter(self, name):
        """Check to see if the requested Object's Parameter is present"""
        return name in self.parameter_dict

    def get_parameter(self, name):
        """Retrieve the requested Object's Parameter List"""
        return self.parameter_dict[name]



class Parameter(object):
    """Represents a Parameter Element:
        Attributes: name("@name"),
                    base("@base"),
                    access("@access"),
                    active_notify("@activeNotify"="normal"),
                    forced_inform("@forcedInform"=False)
        Sub-Elements: description(String::"description"),
                      syntax(Syntax::"syntax")"""
    def __init__(self):
        """Initialize the Parameter"""
        self.name = None
        self.base = None
        self.access = None
        self.active_notify = "normal"
        self.forced_inform = False
        self.description = ""
        self.syntax = None
        self.default = None


    def get_name(self):
        """Retrieve the Parameter's name attribute"""
        return self.name

    def set_name(self, value):
        """Set the Parameter's name attribute"""
        self.name = value

    def get_base(self):
        """Retrieve the Parameter's base attribute"""
        return self.base

    def set_base(self, value):
        """Set the Parameter's base attribute"""
        self.base = value

    def get_access(self):
        """Retrieve the Parameter's access attribute"""
        return self.access

    def set_access(self, value):
        """Set the Parameter's access attribute"""
        self.access = value

    def get_active_notify(self):
        """Retrieve the Parameter's active_notify attribute"""
        return self.active_notify

    def set_active_notify(self, value):
        """Set the Parameter's active_notify attribute"""
        self.active_notify = value

    def get_forced_inform(self):
        """Retrieve the Parameter's forced_inform attribute"""
        return self.forced_inform

    def set_forced_inform(self, value):
        """Set the Parameter's forced_inform attribute"""
        self.forced_inform = value

    def get_description(self):
        """Retrieve the Parameter's description element"""
        return self.description

    def set_description(self, value):
        """Set the Parameter's description element"""
        self.description = value

    def get_syntax(self):
        """Retrieve the Parameter's syntax element"""
        return self.syntax

    def set_syntax(self, value):
        """Set the Parameter's syntax element"""
        self.syntax = value

    def get_default(self):
        """Retrieve the Parameter's default element"""
        return self.default

    def set_default(self, value):
        """Set the Parameter's default element"""
        self.default = value



class Profile(object):
    """Represents a Profile Element:
        Attributes: name("@name"),
                    base("@base"),
                    extends("@extends"),
                    min_version("@minVersion")
        Sub-Elements: description(String::"description"),
                      profile_object_list(ProfileObject[]::"object"),
                      profile_parameter_list(ProfileParameter[]::"parameter")"""
    def __init__(self):
        """Initialize the Profile"""
        self.name = ""
        self.base = None
        self.extends = None
        self.min_version = None
        self.description = ""
        self.profile_object_list = []
        self.profile_parameter_list = []


    def get_name(self):
        """Retrieve the Profile's name attribute"""
        return self.name

    def set_name(self, value):
        """Set the Profile's name attribute"""
        self.name = value

    def get_base(self):
        """Retrieve the Profile's base attribute"""
        return self.base

    def set_base(self, value):
        """Set the Profile's base attribute"""
        self.base = value

    def get_extends(self):
        """Retrieve the Profile's extends attribute"""
        return self.extends

    def set_extends(self, value):
        """Set the Profile's extends attribute"""
        self.extends = value

    def get_min_version(self):
        """Retrieve the Profile's min_version attribute"""
        return self.min_version

    def set_min_version(self, value):
        """Set the Profile's min_version attribute"""
        self.min_version = value

    def get_description(self):
        """Retrieve the Profile's description element"""
        return self.description

    def set_description(self, value):
        """Set the Profile's description element"""
        self.description = value

    def add_profile_object(self, item):
        """Add a Profile Object to this Parameter"""
        self.profile_object_list.append(item)

    def get_profile_objects(self):
        """Retrieve the Parameter's Profile Objects"""
        return self.profile_object_list

    def add_profile_parameter(self, item):
        """Add a Profile Parameter to this Parameter"""
        self.profile_parameter_list.append(item)

    def get_profile_parameters(self):
        """Retrieve the Parameter's Profile Parameters"""
        return self.profile_parameter_list




class UniqueKey(object):
    """Represents a UniqueKey Element:
         Attributes: functional("@functional"=True)
         Sub-Elements: parameter_ref_list(String::"parameter"=>"@ref")"""
    def __init__(self):
        """Initialize the UniqueKey"""
        self.functional = True
        self.parameter_ref_list = []


    def get_functional(self):
        """Retrieve the Unique Key's functional attribute"""
        return self.functional

    def set_functional(self, value):
        """Set the Unique Key's functional attribute"""
        self.functional = value

    def add_parameter_ref(self, item):
        """Add a Parameter Ref to this Unique Key"""
        self.parameter_ref_list.append(item)

    def get_parameter_refs(self):
        """Retrieve the Unique Key's Parameter Refs"""
        return self.parameter_ref_list



class Syntax(object):
    """Represents a Syntax Element:
        Attributes: hidden("@hidden"=False),
                    command("@command"=False)
        Sub-Elements: list_element(ListFacet::"list"),
                      type_element(Type::"type"),
                      data_type_ref(DataType::"dataType"=>"@ref"),
                      default(DefaultFacet::"default")"""
    def __init__(self):
        """Initialize the Syntax"""
        self.hidden = False
        self.command = False
        self.list_element = None
        self.type_element = None
        self.data_type_ref = None
        self.default = None


    def get_hidden(self):
        """Retrieve the Syntax's hidden attribute"""
        return self.hidden

    def set_hidden(self, value):
        """Set the Syntax's hidden attribute"""
        self.hidden = value

    def get_command(self):
        """Retrieve the Syntax's command attribute"""
        return self.command

    def set_command(self, value):
        """Set the Syntax's command element"""
        self.command = value

    def get_list_element(self):
        """Retrieve the Syntax's list element"""
        return self.list_element

    def set_list_element(self, value):
        """Set the Syntax's list element"""
        self.list_element = value

    def get_type_element(self):
        """Retrieve the Syntax's type element"""
        return self.type_element

    def set_type_element(self, value):
        """Set the Syntax's type element"""
        self.type_element = value

    def get_data_type_ref(self):
        """Retrieve the Syntax's data_type_ref element"""
        return self.data_type_ref

    def set_data_type_ref(self, value):
        """Set the Syntax's data_type_ref element"""
        self.data_type_ref = value

    def get_default(self):
        """Retrieve the Syntax's default element"""
        return self.default

    def set_default(self, value):
        """Set the Syntax's default element"""
        self.default = value



class DefaultFacet(object):
    """Represents a Default Element:
        Attributes: type_attribute("@type"),
                    value("@value")
        Sub-Elements: description(String::"description")"""
    def __init__(self):
        """Initialize the DefaultFacet"""
        self.type_attribute = None
        self.value = None
        self.description = ""


    def get_type_attribute(self):
        """Retrieve the Default Facet's type attribute"""
        return self.type_attribute

    def set_type_attribute(self, value):
        """Set the Default Facet's type attribute"""
        self.type_attribute = value

    def get_value(self):
        """Retrieve the Default Facet's value attribute"""
        return self.value

    def set_value(self, value):
        """Set the Default Facet's value attribute"""
        self.value = value

    def get_description(self):
        """Retrieve the Default Facet's description element"""
        return self.description

    def set_description(self, value):
        """Set the Default Facet's description element"""
        self.description = value



class ProfileObject(object):
    """Represents a Profile Object Element:
        Attributes: ref("@ref"),
                    requirement("@requirement")
        Sub-Elements: description(String::"description"),
                      profile_parameter_list(ProfileParameter[]::"parameter")"""
    def __init__(self):
        """Initialize the ProfileObject"""
        self.ref = None
        self.requirement = None
        self.description = ""
        self.profile_parameter_list = []


    def get_ref(self):
        """Retrieve the Profile Object's ref attribute"""
        return self.ref

    def set_ref(self, value):
        """Set the Profile Object's ref attribute"""
        self.ref = value

    def get_requirement(self):
        """Retrieve the Profile Object's requirement attribute"""
        return self.requirement

    def set_requirement(self, value):
        """Set the Profile Object's requirement attribute"""
        self.requirement = value

    def get_description(self):
        """Retrieve the Profile Object's description attribute"""
        return self.description

    def set_description(self, value):
        """Set the Profile Object's description attribute"""
        self.description = value

    def add_profile_parameter(self, item):
        """Add a Profile Parameter to this Profile Object"""
        self.profile_parameter_list.append(item)

    def get_profile_parameters(self):
        """Retrieve the Profile Object's Profile Parameters"""
        return self.profile_parameter_list



class ProfileParameter(object):
    """Represents a Profile Parameter Element:
        Attributes: ref("@ref"),
                    requirement("@requirement")
        Sub-Elements: description(String::"description")"""
    def __init__(self):
        """Initialize the ProfileParameter"""
        self.ref = None
        self.requirement = None
        self.description = ""


    def get_ref(self):
        """Retrieve the Profile Parameter's ref attribute"""
        return self.ref

    def set_ref(self, value):
        """Set the Profile Parameter's ref attribute"""
        self.ref = value

    def get_requirement(self):
        """Retrieve the Profile Parameter's requirement attribute"""
        return self.requirement

    def set_requirement(self, value):
        """Set the Profile Parameter's requirement attribute"""
        self.requirement = value

    def get_description(self):
        """Retrieve the Profile Parameter's description element"""
        return self.description

    def set_description(self, value):
        """Set the Profile Parameter's description element"""
        self.description = value



class Type(object):
    """Represents an abstract Type Element:
        Sub-Classes: Base64Type, BooleanType, DateTimeType, HexBinaryType, NumericType,
                     StringType
        Attributes: name(the actual name of the type: base64, boolean, dateTime, hexBinary
                           int, long, unsignedInt, unsignedLong, string)"""
    def __init__(self, name_value):
        """Initialize the abstract Type"""
        self.name = name_value


    def get_name(self):
        return self.name



class StringType(Type):
    """Represents a String Type Element:
        Types: string
        Sub-Elements: size_list(SizeFacet[]::"size"),
                      path_ref_list(PathRef[]::"pathRef"),
                      enumeration_list(Enumeration[]::"enumeration"),
                      enumeration_ref_list(EnumerationRef[]::"enumerationRef"),
                      pattern_list(Pattern[]::"pattern")"""
    def __init__(self):
        """Initialize the StringType"""
        super(StringType, self).__init__("string")

        self.size_list = []
        self.path_ref_list = []
        self.enumeration_list = []
        self.enumeration_ref_list = []
        self.pattern_list = []

    def add_size(self, item):
        self.size_list.append(item)

    def get_sizes(self):
        return self.size_list

    def add_path_ref(self, item):
        self.path_ref_list.append(item)

    def get_path_refs(self):
        return self.path_ref_list

    def add_enumeration(self, item):
        self.enumeration_list.append(item)

    def get_enumerations(self):
        return self.enumeration_list

    def add_enumeration_ref(self, item):
        self.enumeration_ref_list.append(item)

    def get_enumeration_refs(self):
        return self.enumeration_ref_list

    def add_pattern(self, item):
        self.pattern_list.append(item)

    def get_patterns(self):
        return self.pattern_list



class NumericType(Type):
    """Represent a Numeric Type Element:
        Types: int, long, unsignedInt, unsignedLong
        Sub-Elements: range_list(RangeFacet[]::"range"),
                      unit_list(Unit[]::"units")"""
    def __init__(self, type_name):
        """Initialize the NumericType"""
        super(NumericType, self).__init__(type_name)

        self.unit_list = []
        self.range_list = []


    def add_unit(self, item):
        self.unit_list.append(item)

    def get_units(self):
        return self.unit_list

    def add_range(self, item):
        self.range_list.append(item)

    def get_ranges(self):
        return self.range_list



class BooleanType(Type):
    """Represents a Boolean Type Element:
        Types: boolean"""
    def __init__(self):
        """Initialize the BooleanType"""
        super(BooleanType, self).__init__("boolean")



class Base64Type(Type):
    """Represents a Base64 Type Element:
        Types: base64
        Sub-Elements: size_list(SizeFacet[]::"size")"""
    def __init__(self):
        """Initialize the Base64Type"""
        super(Base64Type, self).__init__("base64")

        self.size_list = []


    def add_size(self, item):
        self.size_list.append(item)

    def get_sizes(self):
        return self.size_list



class DateTimeType(Type):
    """Represents a DateTime Type Element:
        Types: dateTime"""
    def __init__(self):
        """Initialize the DateTime Type"""
        super(DateTimeType, self).__init__("dateTime")



class HexBinaryType(Type):
    """Represents a HexBinary Type Element:
        Types: hexBinary
        Sub-Elements: size_list(SizeFacet[]::"size")"""
    def __init__(self):
        """Initialize the HexBinary Type"""
        super(HexBinaryType, self).__init__("hexBinary")

        self.size_list = []


    def add_size(self, item):
        self.size_list.append(item)

    def get_sizes(self):
        return self.size_list



class FacetType(object):
    """Represents an abstract Facet Type Element:
        Sub-Classes: ListFacet, Size, PathRef, Range, Enumeration,
                     EnumeationRef, Pattern, Unit
        Sub-Elements: description(String::"description")"""
    def __init__(self):
        """Initialize the abstract FacetType"""
        self.description = ""


    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value



class ListFacet(FacetType):
    """Represents a List FacetType Element:
        Attributes: min_items("@minItems"=0),
                    max_items("@maxItems"=unbounded)
                    nested_brackets("@nestedBrackets"="legacy")
        Sub-Elements: size_list(Size[]::"size")"""
    def __init__(self):
        """Initialize the List FacetType"""
        super(ListFacet, self).__init__()
        self.min_items = 0
        self.max_items = None
        self.nested_brackets = "legacy"
        self.size_list = []


    def get_min_items(self):
        return self.min_items

    def set_min_items(self, value):
        self.min_items = value

    def get_max_items(self):
        return self.max_items

    def set_max_items(self, value):
        self.max_items = value

    def get_nested_brackets(self):
        return self.nested_brackets

    def set_nested_brackets(self, value):
        self.nested_brackets = value

    def add_size(self, item):
        self.size_list.append(item)

    def get_sizes(self):
        return self.size_list



class Size(FacetType):
    """Represents a Size FacetType Element:
        Attributes: min_length("@minLength"=0),
                    max_length("@maxLength")"""
    def __init__(self):
        """Initialize the Size FacetType"""
        super(Size, self).__init__()
        self.min_length = 0
        self.max_length = None


    def get_min_length(self):
        return self.min_length

    def set_min_length(self, value):
        self.min_length = value

    def get_max_length(self):
        return self.max_length

    def set_max_length(self, value):
        self.max_length = value



class PathRef(FacetType):
    """Represents a PathRef FacetType Element:
        Attributes: ref_type("@refType"),
                    target_parent("@targetParent"=""),
                    target_parent_scope("@targetParentScope"="normal"),
                    target_type("@targetType"="any"),
                    target_data_type("@targetDataType"="any")"""
    def __init__(self):
        """Initialize the PathRef FacetType"""
        super(PathRef, self).__init__()
        self.ref_type = ""
        self.target_parent = ""
        self.target_parent_scope = "normal"
        self.target_type = "any"
        self.target_data_type = "any"


    def get_ref_type(self):
        return self.ref_type

    def set_ref_type(self, value):
        self.ref_type = value

    def get_target_parent(self):
        return self.target_parent

    def set_target_parent(self, value):
        self.target_parent = value

    def get_target_parent_scope(self):
        return self.target_parent_scope

    def set_target_parent_scope(self, value):
        self.target_parent_scope = value

    def get_target_type(self):
        return self.target_type

    def set_target_type(self, value):
        self.target_type = value

    def get_target_data_type(self):
        return self.target_data_type

    def set_target_data_type(self, value):
        self.target_data_type = value



class Range(FacetType):
    """Represents a Range FacetType Element:
        Attributes: min_inclusive("@minInclusive"),
                    max_inclusive("@maxInclusive"),
                    step("@step"=1)"""
    def __init__(self):
        """Initialize the Range FacetType"""
        super(Range, self).__init__()
        self.min_inclusive = None
        self.max_inclusive = None
        self.step = 1


    def get_min_inclusive(self):
        return self.min_inclusive

    def set_min_inclusive(self, value):
        self.min_inclusive = value

    def get_max_inclusive(self):
        return self.max_inclusive

    def set_max_inclusive(self, value):
        self.max_inclusive = value

    def get_step(self):
        return self.step

    def set_step(self, value):
        self.step = value



class Enumeration(FacetType):
    """Represents a Enumeration FacetType Element:
        Attributes: value("@value"),
                    code("@code")"""
    def __init__(self):
        """Initialize the Enumeration FacetType"""
        super(Enumeration, self).__init__()
        self.value = ""
        self.code = None


    def get_value(self):
        return self.value

    def set_value(self, a_value):
        self.value = a_value

    def get_code(self):
        return self.code

    def set_code(self, value):
        self.code = value



class EnumerationRef(FacetType):
    """Represents a EnumerationRef FacetType Element:
        Attributes: target_param("@targetParam"),
                    target_param_scope("@targetParamScope"="normal"),
                    null_value("@nullValue")"""
    def __init__(self):
        """Initialize the EnumerationRef FacetType"""
        super(EnumerationRef, self).__init__()
        self.target_param = ""
        self.target_param_scope = ""
        self.null_value = ""


    def get_target_param(self):
        return self.target_param

    def set_target_param(self, value):
        self.target_param = value

    def get_target_param_scope(self):
        return self.target_param_scope

    def set_target_param_scope(self, value):
        self.target_param_scope = value

    def get_null_value(self):
        return self.null_value

    def set_null_value(self, value):
        self.null_value = value



class Pattern(FacetType):
    """Represents a Pattern FacetType Element:
        Attributes: value("@value")"""
    def __init__(self):
        """Initialize the Pattern FacetType"""
        super(Pattern, self).__init__()
        self.value = ""


    def get_value(self):
        return self.value

    def set_value(self, a_value):
        self.value = a_value



class Unit(FacetType):
    """Represents a Units FacetType Element:
        Attributes: value("@value")"""
    def __init__(self):
        """Initialize the Units FacetType"""
        super(Unit, self).__init__()
        self.value = ""


    def get_value(self):
        return self.value

    def set_value(self, a_value):
        self.value = a_value

