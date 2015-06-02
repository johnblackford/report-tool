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
    self.size = None
    self.instance_ref = ""
    self.path_ref = ""
    self.range = None
    self.enumeration = []
    self.enumeration_ref = ""
    self.pattern = []
    self.units = ""


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

  ### TODO: Implement the rest of the things
  #    self.type = None
  #    self.list = None
  #    self.size = None
  #    self.instance_ref = ""
  #    self.path_ref = ""
  #    self.range = None
  #    self.enumeration = []
  #    self.enumeration_ref = ""
  #    self.pattern = []
  #    self.units = ""



class Type(object):
  def __init__(self, name_value):
    self.name = name_value


  def get_name(self):
    return self.name



class StringType(Type):
  def __init__(self):
    super(StringType, self).__init__("string")

    self.size = None
    self.path_ref = ""
    self.enumeration = []
    self.enumeration_ref = ""
    self.pattern = []



class Size(object):
  def __init__(self):
    self.min_length = 0
    self.max_length = None
