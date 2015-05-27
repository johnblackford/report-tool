#! /usr/bin/env python

## 
## File Name: nodes.py
##
## Description: Objects for the Node Tree
## 
## Functionality:
##  - Document Node (just a description for now)
## 


class Document:
  def __init__(self):
    self.spec = ""
    self.file_name = ""
    self.description = ""



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
