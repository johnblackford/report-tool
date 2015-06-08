#! /usr/bin/env python

## 
## File Name: nodes.py
##
## Description: Objects for the Node Tree
## 
## Functionality:
##  - Document Node (just a description for now)
## 


class Document(object):
  def __init__(self):
    self.spec = ""
    self.file_name = ""
    self.description = ""
    self.data_type_list = []


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
    self.data_type_list.append(item)

  def get_data_types(self):
    return self.data_type_list



class DataType(object):
  def __init__(self):
    self.name = ""
    self.base = ""
    self.status = "current"
    self.description = ""
    self.type = None
    self.list = None
    self.size_list = []
    self.path_ref_list = []
    self.range_list = []
    self.enumeration_list = []
    self.enumeration_ref_list = []
    self.pattern_list = []
    self.unit_list = []
    ### TODO: We may also want an Inferred Type that is a complete definition with respect to the base


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
    return self.type

  def set_type(self, value):
    self.type = value

  def get_list(self):
    return self.list

  def set_list(self, value):
    self.list = value

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



class Type(object):
  def __init__(self, name_value):
    self.name = name_value


  def get_name(self):
    return self.name



class StringType(Type):
  def __init__(self):
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
    return self.patter_list



class NumericType(Type):
  def __init__(self, type_name):
    super(NumericType, self).__init__(type_name)

    self.unit_list = []
    self.range_list = []


  def add_unit(self, item):
    self.unit_list.appen(item)

  def get_units(self):
    return self.unit_list

  def add_range(self, item):
    self.range_list.append(item)

  def get_ranges(self):
    return self.range



class BooleanType(Type):
  def __init__(self):
    super(BooleanType, self).__init__("boolean")



class Base64Type(Type):
  def __init__(self):
    super(Base64Type, self).__init__("base64")

    self.size_list = []


  def add_size(self, item):
    self.size_list.append(item)

  def get_sizes(self):
    return self.size_list



class DateTimeType(Type):
  def __init__(self):
    super(DateTimeType, self).__init__("dateTime")



class HexBinaryType(Type):
  def __init__(self):
    super(HexBinaryType, self).__init__("hexBinary")

    self.size_list = []


  def add_size(self, item):
    self.size_list.append(item)

  def get_sizes(self):
    return self.size_list



class List(object):
  def __init__(self):
    self.min_items = 0
    self.max_items = None
    self.nested_brackets = "legacy"
    self.description = ""
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

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value

  def add_size(self, item):
    self.size_list.append(item)

  def get_sizes(self):
    return self.size_list



class Size(object):
  def __init__(self):
    self.min_length = 0
    self.max_length = None
    self.description = ""


  def get_min_length(self):
    return self.min_length

  def set_min_length(self, value):
    self.min_length = value

  def get_max_length(self):
    return self.max_length

  def set_max_length(self, value):
    self.max_length = value

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value



class PathRef(object):
  def __init__(self):
    self.ref_type = ""
    self.target_parent = ""
    self.target_parent_scope = ""
    self.target_type = ""
    self.target_data_type = ""
    self.description = ""


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

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value



class Range(object):
  def __init__(self):
    self.min_inclusive = None
    self.max_inclusive = None
    self.step = 1
    self.description = ""


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

  def set_Step(self, value):
    self.step = value

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value



class Enumeration(object):
  def __init__(self):
    self.value = ""
    self.code = None
    self.description = ""


  def get_value(self):
    return self.value

  def set_value(self, a_value):
    self.value = a_value

  def get_code(self):
    return self.code

  def set_code(self, value):
    self.code = value

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value



class EnumerationRef(object):
  def __init__(self):
    self.target_param = ""
    self.target_param_scope = ""
    self.null_value = ""
    self.description = ""


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

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value



class Pattern(object):
  def __init__(self):
    self.value = ""
    self.description = ""


  def get_value(self):
    return self.value

  def set_value(self, a_value):
    self.value = a_value

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value



class Unit(object):
  def __init__(self):
    self.value = ""
    self.description = ""


  def get_value(self):
    return self.value

  def set_value(self, a_value):
    self.value = a_value

  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value
