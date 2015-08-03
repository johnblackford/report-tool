"""
## File Name: debug_validators.py
##
## Description: A set of Debug Validators
##
## Functionality:
##	- Deubug Validator for checking the Document Element has a Description
##
"""


import logging
import cStringIO

from abstract_classes import AbstractValidator



class DocDescValidator(AbstractValidator):
    """Debugging Validator - validates the Document Description is not empty"""

    def validate(self, document):
        output_buffer = cStringIO.StringIO()
        logger = logging.getLogger(self.__class__.__name__)

        logger.info("Starting Validator...")

        if len(document.get_description()) == 0:
            output_buffer.write("Validation Failure: WARN: Document Description is empty")
            print output_buffer.getvalue()
            logger.warn(output_buffer.getvalue())
        else:
            logger.debug("All Validation Passed")

        logger.info("Validator Complete")

        output_buffer.close()
