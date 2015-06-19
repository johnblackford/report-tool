#! /usr/bin/env python

"""
## File Name: debug_writers.py
##
## Description: Debug Text Output Writer
##
## Functionality:
##      - Output Writer for the Debug Text Format
##
"""

import logging
import cStringIO

from abstract_classes import AbstractOutputWriter


class OneLineTextOutputWriter(AbstractOutputWriter):
    """Debug Text Output Writer"""

    def __init__(self):
        """Initialize internal variables"""
        self.doc = None
        self.write_data_types = False
        self.write_biblio_refs = False
        self.write_model_objects = False
        self.write_model_parameters = False
        self.write_model_profiles = False



    def get_output_format(self):
        """Return the appropriate output format"""
        return "text"


    def process_properties(self, props):
        """Retrieve the OneLine property"""
        logger = logging.getLogger(self.__class__.__name__)
        self.write_data_types = props.get("DataTypes", False)
        self.write_biblio_refs = props.get("BiblioRefs", False)
        self.write_model_objects = props.get("ModelObjects", False)
        self.write_model_parameters = props.get("ModelParameters", False)
        self.write_model_profiles = props.get("ModelProfiles", False)
        logger.info("Write DataType Elements: {}".format(self.write_data_types))



    def write(self, doc, filename):
        """Write the output as configured"""
        output_buffer = cStringIO.StringIO()

        self._generate_content(doc, output_buffer)

        if len(filename) == 0:
            self._write_to_console(output_buffer)
        else:
            self._write_to_file(output_buffer, filename)

        output_buffer.close()



    def _generate_content(self, doc, out_buffer):
        """Internal method to generate content in the output buffer"""
        trunc_desc = doc.get_description().split("\n")[0]

        # Document Line
        out_buffer.write(
            "\nDocument [spec={}], [file={}]: {}\n"
            .format(doc.get_spec(), doc.get_file(), trunc_desc))

        # Data Type Lines
        if self.write_data_types:
            self._generate_data_type_content(doc, out_buffer)

        # Bibliography Reference Lines
        if self.write_biblio_refs:
            self._generate_biblio_ref_content(doc, out_buffer)

        # Model Line
        self._generate_model_content(doc, out_buffer)

        # Model Object Lines
        if self.write_model_objects:
            self._generate_model_object_content(doc, out_buffer)

        # Model Parameter Lines
        if self.write_model_parameters:
            self._generate_model_param_content(doc, out_buffer)

        # Model Profile Lines
        if self.write_model_profiles:
            self._generate_model_profile_content(doc, out_buffer)



    def _generate_data_type_content(self, doc, out_buffer):
        """Internal method to generate Data Type content in the output buffer"""
        out_buffer.write("\nDocument contains the following Data Types:\n")

        for data_type in doc.get_data_types():
            if data_type.get_base() is None:
                out_buffer.write(
                    "- DataType [name={}]: {}\n"
                    .format(data_type.get_name(), data_type.get_type_element().get_name()))
            else:
                ### If it has a base then it doesn't have a type
                out_buffer.write(
                    "- DataType [name={}], [base={}]\n"
                    .format(data_type.get_name(), data_type.get_base()))



    def _generate_biblio_ref_content(self, doc, out_buffer):
        """Internal method to generate Bibliography Reference content in the output buffer"""
        out_buffer.write("\nDocument contains the following Bibliography References:\n")

        for biblio_ref in doc.get_biblio_refs():
            out_buffer.write("- Reference to [{}]\n".format(biblio_ref.get_name()))



    def _generate_model_content(self, doc, out_buffer):
        base_string = ""
        data_model_type = "Root"

        if doc.get_model().is_service_data_model():
            data_model_type = "Service"

        if doc.get_model().get_base() is not None:
            base_string = " base={}]".format(doc.get_model().get_base())

        out_buffer.write(
            "\n{} {} Data Model {}\n"
            .format(doc.get_model().get_name(), data_model_type, base_string))



    def _generate_model_object_content(self, doc, out_buffer):
        """Internal method to generate Model Object content in the output buffer"""
        pass



    def _generate_model_param_content(self, doc, out_buffer):
        """Internal method to generate Model Parameter content in the output buffer"""
        pass



    def _generate_model_profile_content(self, doc, out_buffer):
        """Internal method to generate Model Profile content in the output buffer"""
        pass



    def _write_to_console(self, out_buffer):
        """Internal method to generate verbose output content to the console"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Writing to the console")
        print out_buffer.getvalue()



    def _write_to_file(self, out_buffer, filename):
        """Internal method to write the output buffer to the output file"""
        logger = logging.getLogger(self.__class__.__name__)

        # Open the File for writing
        with open(filename, "w") as out_file:
            logger.info("Writing to the file: {}".format(filename))
            out_file.write(out_buffer.getvalue())
            logger.info("Finished writing the output file")

