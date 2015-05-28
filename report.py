#! /usr/bin/env python

## 
## File Name: report.py
##
## Description: Baseline Report Tool for BBHome
## 
## Functionality:
##  - Input Readers Supported: CWMP-DM XML
##  - Output Writers Supported: Debug Text
## 

# High Level Design Concepts
# Input Readers : CWMP-DM XML Reader, CWMP-DT XML Reader, YIN Reader, YANG Reader
#  Readers need to accept a file and convert the contents into objects: Document, Component, Model, Object, Parameter, Profile
# Output Writers : Text Debug Writer, CWMP-DM HTML Writer, CWMP-DT XML Writer, CWMP-DT HTML Writer
#  Writers need to accept a Document and write the contents to the intended format
# Objects should be structured as a "node tree" 
#  (Model would have a list of Parameters and a list of Objects and a list of Profiles; Object would have a list of Parameters and a list of Objects etc).


### TODO:
# - Remove verbose logging
# - Add -v | --validate as a command line option
# - Add in validators (abstract class, config file, loading, calling)


import json
import logging
import xmltodict
import sys, getopt
import importlib

import debugWriters
#import cwmpDataModelInputReader


# Global Constants
_VERSION = "0.1.0-alpha"



def _get_class_from_property(class_type, prop_item):
  name = prop_item["Name"]
  mod_name = prop_item["Module"]
  class_name = prop_item["Class"]
  target_class = None

  logging.debug("Processing [{}] {} within Module [{}], and using Class [{}]"
    .format(name, class_type, mod_name, class_name))

  # import the module, get the class, and instantiate the class
  try:
    mod = importlib.import_module(mod_name)
    target_class = getattr(mod, class_name)
  except ImportError:
    logging.warning("Issue with [{}] {}: Module [{}] could not be imported... Skipping"
      .format(name, class_type, mod_name))
  except AttributeError:
    logging.warning("Issue with [{}] {}: Class [{}] within Module [{}] could not be found... Skipping"
      .format(name, class_type, class_name, mod_name))

  return target_class;



def main(argv):
  input_file = ""
  input_format = ""
  output_file = ""
  output_format = ""
  verbose_logging = False

  input_reader = None
  output_writer = None
  input_reader_list = []
  output_writer_list = []

  error_list = []
  fatal_arg_error = False

  logging_level = logging.DEBUG
  logging_level_failure = False
  

  ## Get the Configuration from the properties file
  ### TODO: The file name should probably be absolute instead of relative (based on standard install location?)
  with open("config/installation.properties", "r") as prop_file:
    prop_data = json.load(prop_file)
    log_level = prop_data["LogLevel"]
    readers_prop = prop_data["InputReaders"]
    writers_prop = prop_data["OutputWriters"]
    ### TODO: Where should we put the properties?  
    ### TODO:  Should we have some kind of global Properties Manager object that can be accessed everywhere?


  # Get the Logging level based on LogLevel Property
  try:
    logging_level = getattr(logging, log_level)
  except AttributeError:
    logging_level_failure = True

  ### TODO: The file name should probably be absolute instead of relative (based on standard install location?)
  logging.basicConfig(filename="logs/report.log", format='%(asctime)-15s %(name)s %(levelname)-8s %(message)s')
  logging.getLogger().setLevel(logging_level)

  logging.info("#######################################################")
  logging.info("## Starting report.py                                ##")
  logging.info("#######################################################")

  # Log the properties that were read in
  logging.info("The installation.properties file contained:")
  logging.debug("[LogLevel] property has value [{}]".format(log_level))
  if logging_level_failure:
    logging.warn("[LogLevel] property had an invalid value, using DEBUG instead")
  logging.debug("[InputReaders] property has value [{}]".format(readers_prop))
  logging.debug("[OutputWriters] property has value [{}]".format(writers_prop))


  # Add Input Readers to the list
  for reader_item in readers_prop:
    target_class = _get_class_from_property("Input Reader", reader_item)
    if target_class is not None:
      input_reader_list.append(target_class())


  # Add Output Writers to the list
  for writer_item in writers_prop:
    target_class = _get_class_from_property("Output Writer", writer_item)
    if target_class is not None:
      output_writer_list.append(target_class())


  # Build out Input Reader Dictionary
  input_reader_dict = {}
  for ir in input_reader_list:
    ir_format = ir.get_input_format()
    input_reader_dict[ir_format] = ir

  # Build out Output Writer Dictionary
  output_writer_dict = {}
  for ow in output_writer_list:
    ow_format = ow.get_output_format()
    output_writer_dict[ow_format] = ow

  available_input_formats = input_reader_dict.keys()
  available_output_formats = output_writer_dict.keys()

  
  # Usage string for input argument handling
  usage_str = "report.py -i <iput format> -I <input file> -o <output format> [-O <output file>]"

  # Retrieve the input arguments
  logging.info("Processing the Input Arguments...")
  logging.debug("Found Input Arguments: {}".format(argv))

  try:
    opts, args = getopt.getopt(argv, "hi:I:o:O:vV", 
                   ["input-format=", "input-file=", "output-format=", "output-file=",
                    "help", "verbose", "version"])
  except getopt.GetoptError:
    print "Error Encountered:"
    logging.error("Error Encountered:")
    print " - Unknown command line argument encountered"
    logging.error(" - Unknown command line argument encountered")
    print ""
    print usage_str
    sys.exit(2)


  # Process the input arguments
  for opt, arg in opts:
    if opt in ('-h', "--help"):
      print usage_str
      print "  -i|--input-format   :: Specify the input format (choice of: {})".format(available_input_formats)
      print "  -I|--input-file     :: Specify the input file"
      print "  -o|--output-format  :: Specify the output format (choice of: {})".format(available_output_formats)
      print "  -O|--output-file    :: Specify the output file (defaults to console)"
      print "  -v|--verbose        :: Enable verbose logging"
      print "  -V|--version        :: Print the version of the tool"
      sys.exit()
    elif opt in ("-i", "--input-format"):
      input_format = arg
    elif opt in ("-I", "--input-file"):
      input_file = arg
    elif opt in ("-o", "--output-format"):
      output_format = arg
    elif opt in ("-O", "--output-file"):
      output_file = arg
    elif opt in ("-v", "--verbose"):
      verbose_logging = True
      logging.info("Verbose Logging Enabled")
    elif opt in ("-V", "--version"):
      print "Report Tool :: version={}".format(_VERSION)
      sys.exit()


  # Validate the required input arguments are not empty
  logging.info("Validating the Input Arguments...")

  if len(input_file) == 0:
    fatal_arg_error = True
    error_list.append("ERROR: Input File not provided")

  if len(input_format) == 0:
    fatal_arg_error = True
    error_list.append("ERROR: Input Format not provided")

  if len(output_format) == 0:
    fatal_arg_error = True
    error_list.append("ERROR: Output Format not provided")


  # Validate the input arguments have the proper values
  if input_reader_dict.has_key(input_format):
    input_reader = input_reader_dict[input_format]
    if verbose_logging:
      input_reader.enable_verbose_logging()
  else:
    fatal_arg_error = True
    error_list.append("ERROR: Input Format not supported")

  if output_writer_dict.has_key(output_format):
    output_writer = output_writer_dict[output_format]
    if verbose_logging:
      output_writer.enable_verbose_logging()
  else:
    fatal_arg_error = True
    error_list.append("ERROR: Output Format not supported")


  # Processing input argument validation
  if fatal_arg_error:
    print "Errors Encountered:"
    logging.error("Errors Encountered:")
    for err_msg in error_list:
      logging.error(" - {}".format(err_msg))
      print " - {}".format(err_msg)
    print ""
    print usage_str
    sys.exit(1)
  else:
    if verbose_logging:
      logging.info("Input Arguments have been validated")
      logging.info(" - Input Format = {}".format(input_format))
      logging.info(" - Input File = {}".format(input_file))
      logging.info(" - Output Format = {}".format(output_format))
      if len(output_file) == 0:
        logging.info(" - No Output File specified; writing Output to console")
      else:
        logging.info(" - Output File = {}".format(output_file))


  output_writer.write(input_reader.read(input_file), output_file)



if __name__ == "__main__":
  main(sys.argv[1:])
