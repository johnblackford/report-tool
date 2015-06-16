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


class TextOutputWriter(AbstractOutputWriter):
    """Debug Text Output Writer"""

    def __init__(self):
        """Initialize internal variables"""
        self.doc = None
        self.one_line_output = False



    def get_output_format(self):
        """Return the appropriate output format"""
        return "text"


    def process_properties(self, props):
        """Retrieve the OneLine property"""
        logger = logging.getLogger(self.__class__.__name__)
        self.one_line_output = props.get("OneLine", False)
        logger.info("One Line Output Property now set to: {}".format(self.one_line_output))



    def write(self, doc, filename):
        """Write the output as configured"""
        output_buffer = cStringIO.StringIO()

        if self.one_line_output:
            self._generate_one_line_content(doc, output_buffer)
        else:
            self._generate_content(doc, output_buffer)

        if len(filename) == 0:
            self._write_to_console(output_buffer)
        else:
            self._write_to_file(output_buffer, filename)

        output_buffer.close()



    def _generate_one_line_content(self, doc, out_buffer):
        """Internal method to generate 1-Line output content to an output buffer"""
        trunc_desc = doc.get_description().split("\n")[0]
        out_buffer.write(
            "\nDocument [spec={}], [file={}]: {}\n"
            .format(doc.get_spec(), doc.get_file(), trunc_desc))
        for data_type in doc.get_data_types():
            if data_type.get_base() is None:
                out_buffer.write(
                    "- DataType [name={}]: {}\n"
                    .format(data_type.get_name(), data_type.get_type().get_name()))
            else:
                ### If it has a base then it doesn't have a type
                out_buffer.write(
                    "- DataType [name={}], [base={}]\n"
                    .format(data_type.get_name(), data_type.get_base()))


    def _generate_content(self, doc, out_buffer):
        """Internal method to geneate verbose output content to an output buffer"""
        out_buffer.write("\n")
        out_buffer.write("Document Spec: {}\n".format(doc.get_spec()))
        out_buffer.write("Document File: {}\n".format(doc.get_file()))

        out_buffer.write("Document Description:\n")
        out_buffer.write("{}\n".format(doc.get_description()))



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

