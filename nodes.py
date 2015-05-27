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
    self.description = ""



  def get_description(self):
    return self.description

  def set_description(self, value):
    self.description = value
