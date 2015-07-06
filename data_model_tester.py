#! /usr/bin/env python

"""
# File Name: data_model_tester.py
#
# Description: Data Model Tester
#
# Functionality:
#  - DataModelSanityTester:
#     A concrete Tester that performs a sanity check on the implemented
#     data model for a Device by walking it via GetParameterNames and
#     GetParameterValues RPC calls.  Essentialy it is that starting point
#     of an ID-106 Test Client
#
"""

# TODO: Probably want an AbstractTester in abstract_classes.py


import nodes
import logging
import xmltodict
import cStringIO

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer



class DataModelSanityTester(object):
    """A contrete Tester that performs a Data Model Sanity Check via
        an HTTP Request Handler"""
    def __init__(self):
        """Initialize the Tester"""
        self.implemented_data_model = None
        self.cwmp = CWMPServer(8000)


    def start_server(self):
        """Start the CWMP Server, which walks the device's data model"""
        # Start the Server
        self.cwmp.start_server()

        # Retreive the implemented data model from the Server
        self.implemented_data_model = self.cwmp.get_implemented_data_model()


    def test(self):
        """Test the implemented data model"""
        print "Testing..."
        print "The Root Data Model is: " + self.cwmp.get_root_data_model()



class CWMPServer(object):
    """An CWMP Server that is also an HTTP Server that can be stopped"""
    def __init__(self, port):
        self.data_model = []
        self.device_id = None
        self.root_data_model = None
        self.requested_gpn = None
        self.requested_gpv = None
        self.pending_gpn_list = []
        self.http_server = StoppableHTTPServer(("", port), CWMPHandler)
        self.http_server.set_cwmp_server(self)


    def start_server(self):
        """Keep the CWMP Server up until it is stopped"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Starting the CWMP Server")
        print "Waiting for CWMP Inform..."
        self.http_server.serve_forever()


    def stop_server(self):
        """Terminate the CWMP Server"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Stopping the CWMP Server")
        self.http_server.stop_serving()


    def get_device_id(self):
        """Retrieve the Device ID that is being worked on"""
        return self.device_id

    def is_device_id_present(self):
        """Check to see if the Device ID has been set"""
        return self.device_id is not None

    def set_device_id(self, value):
        """Set the Device ID for the device to be worked on"""
        self.device_id = value


    def get_root_data_model(self):
        """Retrieve the Root Data Model of the device being worked on"""
        return self.root_data_model

    def set_root_data_model(self, value):
        """Set the Root Data Model for the device to be be worked on"""
        self.root_data_model = value


    def get_implemented_data_model(self):
        """Get the implemented data model, as built out during the walk"""
        return self.data_model

    def add_object_to_data_model(self, data_model_obj):
        """Add a Data Model Object to the implemented data model"""
        self.data_model.append(data_model_obj)


    def get_requested_gpn(self):
        """Retrieve the Requested GPN that is being worked on"""
        return self.requested_gpn

    def set_requested_gpn(self, value):
        """Set the Requested GPN to be worked on"""
        self.requested_gpn = value


    def get_requested_gpv(self):
        """Retrieve the Requested GPV that is being worked on"""
        return self.requested_gpv

    def set_requested_gpv(self, value):
        """Set the Requested GPV to be worked on"""
        self.requested_gpv = value


    def append_gpn_items(self, partial_path_list):
        """Add the DataModelObject List to the end of the Pending GPN List"""
        self.pending_gpn_list.extend(partial_path_list)

    def get_next_gpn_item(self):
        """Get the next DataModelObject item from the Pending GPN List"""
        return self.pending_gpn_list.pop(0)

    def more_gpn_items(self):
        """Check to see if there are more DataModelObject items in the Pending GPN List"""
        items_in_list = False
        if len(self.pending_gpn_list) > 0:
            items_in_list = True

        return items_in_list



class StoppableHTTPServer(HTTPServer):
    """A Stoppable HTTP Server"""
    def serve_forever(self):
        """Keep the HTTP Server up until it is stopped"""
        self.stop = False
        logger = logging.getLogger(self.__class__.__name__)

        logger.info("Starting the HTTP Server")
        while not self.stop:
            logger.info("Waiting for an HTTP Request")
            self.handle_request()


    def stop_serving(self):
        """Terminate the HTTP Server"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Stopping the HTTP Server")
        self.stop = True


    def get_cwmp_server(self):
        """Retrieve the value of the CWMP Server"""
        return self.cwmp_server

    def set_cwmp_server(self, value):
        """Set the value of the CWMP Server"""
        self.cwmp_server = value



class CWMPHandler(BaseHTTPRequestHandler):
    """An HTTP Request Handler for the following CWMP RPCs:
        - Inform, GetParameterNamesResponse, GetParameterValuesResponse"""
    def log_message(self, format, *args):
        """Change logging from stderr to debug log"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.debug("%s - - %s" % (self.address_string(), format % args))


    def do_GET(self):
        # Log the Request
        logger = logging.getLogger(self.__class__.__name__)
        logger.debug("Received incoming HTTP GET")
        logger.debug("  Path: " + self.path)

        # Respond with a 404 Error (shouldn't process GET)
        self.server.stop_serving()
        self.send_error(404, "CWMP File Not Found: %s" % self.path)


    def do_POST(self):
        """Handle the HTTP POST Messages containing CWMP Messages"""
        content = ""
        content_length = 0
        logger = logging.getLogger(self.__class__.__name__)
        cwmp_server = self.server.get_cwmp_server()

        # Process the Request
        # TODO: Should we do chunked encoding? - Might have to, or might have to front it with nginx
        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            content = self.rfile.read(content_length)

            # Log the Request
            logger.info("Received incoming HTTP POST")
            logger.debug("  Path: " + self.path)
            logger.info("  Content-Length: " + str(content_length))
            logger.info("  Content-Type: " + self.headers["Content-Type"])

            if content_length == 0:
                # Validate that this is the Empty HTTP POST that is sent after the Inform
                #  - Make sure that we have a Device ID from an Inform
                #  - Make sure that we don't have any pending GPN or GPV
                if (cwmp_server.get_requested_gpn() is None and 
                        cwmp_server.get_requested_gpv() is None and
                        cwmp_server.is_device_id_present()):
                    logger.info("Processing incoming EMPTY HTTP POST as a CWMP Message")
                    self._write_incoming_cwmp_message("<EMPTY>")

                    # Start with the Root Data Model Object
                    a_data_model_obj = DataModelObject()
                    a_data_model_obj.set_name(cwmp_server.get_root_data_model())
                    a_data_model_obj.set_access("readOnly")

                    cwmp_server.set_requested_gpn(a_data_model_obj)

                    # TODO: send a GPN for the Root Data Model
#                    self._get_parameter_names(a_data_model_obj)

                    # TODO: Remove after the _get_parameter_names method is complete
                    self._terminate_cwmp_session()
                else:
                    # Invalid input - return a fault
                    logger.warning("Invalid Empty POST Received")
                    self.send_error(500, "Invalid Empty POST Received")
            elif "xml" in self.headers["Content-Type"]:
                logger.info("Processing incoming HTTP POST as a CWMP Message")

                # Trace the CWMP Conversation
                self._write_incoming_cwmp_message(content)

                # Convert content from XML to Dictionary
                content_dict = self._convert_content_to_dict(content)

                # Process the CWMP Message (Inform, Empty, GPNResp, GPVResp)
                self._process_cwmp_message(content_dict["soap-env:Envelope"])
            else:
                # Invalid input - return a fault
                logger.warning(
                    "Invalid Content Type Received {} - Sending an HTTP 500"
                    .format(self.headers["Content-Type"]))
                self.send_error(500, "Invalid Content-Type: %s" % self.headers["Content-Type"])



    def _write_incoming_cwmp_message(self, message):
        """Write Incoming CWMP Trace Messages to a separate log file"""
        trace_logger = logging.getLogger("TRACE_LOGGING")
        message_type = "Incoming HTTP POST from [{}]".format(self.address_string())

        trace_logger.debug(message_type)
        trace_logger.debug(message)



    def _write_outgoing_cwmp_message(self, message):
        """Write Outgoing CWMP Trace Messages to a separate log file"""
        trace_logger = logging.getLogger("TRACE_LOGGING")
        message_type = "Outgoing HTTP Response to [{}]".format(self.address_string())

        trace_logger.debug(message_type)
        trace_logger.debug(message)



    def _convert_content_to_dict(self, content_str):
        """Convert the XML Content into a Dictionary"""
        content_dict = {}

        # Use these standard namespaces
        namespaces = {
            "urn:dslforum-org:cwmp-1-0": "cwmp",
            "urn:dslforum-org:cwmp-1-1": "cwmp",
            "urn:dslforum-org:cwmp-1-2": "cwmp",
            "http://www.w3.org/2001/XMLSchema": "xsd",
            "http://www.w3.org/2001/XMLSchema-instance": "xsi",
            "http://schemas.xmlsoap.org/soap/envelope/": "soap-env",
            "http://schemas.xmlsoap.org/soap/encoding/": "soap-enc"
        }

        content_dict = xmltodict.parse(content_str, process_namespaces=True, namespaces=namespaces)

        return content_dict



    def _process_cwmp_message(self, soap_envelope):
        """Process the Incoming CWMP Message, which could be one of:
             Inform, GetParameterNamesResponse, GetParameterValuesResponse"""
        soap_body = soap_envelope["soap-env:Body"]
        soap_header = soap_envelope["soap-env:Header"]
        logger = logging.getLogger(self.__class__.__name__)

        if "cwmp:Inform" in soap_body:
            logger.info("Incoming HTTP POST is a CWMP Inform RPC")
            self._process_inform(soap_header, soap_body)
        elif "cwmp:GetParameterNamesResponse" in soap_body:
            logger.info("Incoming HTTP POST is a Response to a CWMP GetParameterNames RPC")
            self._process_gpn_response(soap_body)
        elif "cwmp:GetParameterValuesResponse" in soap_body:
            logger.info("Incoming HTTP POST is a Response to a CWMP GetParameterValues RPC")
            self._process_gpv_response(soap_body)
        else:
            logger.warning("Unsupported CWMP RPC encountered - Sending an HTTP 500")
            self.send_error(500, "Unsupported CWMP RPC encountered")



    def _process_inform(self, soap_header, soap_body):
        """Process the incoming CWMP Inform RPC"""
        cwmp_server = self.server.get_cwmp_server()
        logger = logging.getLogger(self.__class__.__name__)

        # Are we already in a CWMP Session with another device?
        if cwmp_server.is_device_id_present():
            # YES; Response with a fault
            logger.warning(
                "Already Processing Device {} - Sending an HTTP 500"
                .format(cwmp_server.get_device_id()))
            self.send_error(500, "Already Processing Device: %s" % cwmp_server.get_device_id())
        else:
            # NO; Save the OUI-SN as the Found Device and send the InformResponse
            cwmp_device_id = soap_body["cwmp:Inform"]["DeviceId"]
            device_id = cwmp_device_id["OUI"] + "-" + cwmp_device_id["SerialNumber"]

            param_list = soap_body["cwmp:Inform"]["ParameterList"]
            for param_val_struct_item in param_list["ParameterValueStruct"]:
                if "SoftwareVersion" in param_val_struct_item["Name"]:
                    cwmp_server.set_root_data_model(param_val_struct_item["Name"].split(".")[0])

            cwmp_server.set_device_id(device_id)
            self._send_inform_response(soap_header)



    def _process_gpn_response(self, soap_body):
        pass
        # TODO: _process_get_parameter_names_response(soap_body)
        # requested_data_model_obj = server.get_requested_gpn()
        # loop through returned parameter list
        #   if item ends in a "."
        #     create a DataModelObject
        #     add the new DataModelObject to the sub_object_list
        #   else
        #     create a new DataModelParameter if it doesn't end in a "."
        #     add the new DataModelParameter to the requested_data_model_obj
        #     add the new DataModelParameter to a gpv_param_list
        # if gpv_param_list is not empty
        #   set_requested_gpv(requested_data_model_obj)
        #   appendd_list_to_pending_gpn_list(sub_object_list)
        #   _get_parameter_values(gpv_param_list)
        # elif sub_object_list is not empty:
        #   a_data_model_obj = sub_object_list.pop()
        #   set_requested_gpn(a_data_model_obj)
        #   appendd_list_to_pending_gpn_list(sub_object_list)
        #   _get_parameter_names(a_data_model_obj)
        # elif not server.is_pending_gpn_list_empty()
        #   next_gpn_obj = server.get_pending_gpn_list().pop()
        #   server.set_requested_gpn(next_gpn_obj)
        #   _get_parameter_names(next_gpn_obj)
        # else:
        #   _terminate_cwmp_session()



    def _process_gpv_response(self, soap_body):
        pass
        # TODO: _process_get_parameter_values_response(soap_body)
        # requested_data_model_obj = server.get_requested_gpv()
        # loop through returned parameter list
        #   get DataModelParameter from requested_data_model_obj
        #   set the value
        # if not server.is_pending_gpn_list_empty():
        #   next_gpn_obj = server.get_pending_gpn_list().pop()
        #   server.set_requested_gpn(next_gpn_obj)
        #   _get_parameter_names(next_gpn_obj)
        # else:
        #   _terminate_cwmp_session()



    def _get_parameter_names(self, a_data_model_obj):
        pass
        # TODO: _get_parameter_names(DataModelObject)
        # send a GPN with the name of the passed in Data Model Object and a True for NextLevel



    def _get_parameter_values(self, param_list):
        pass
        # TODO: _get_parameter_values(List of DataModelParameters)
        # send a GPV with the names of the passed in Data Model Parameters



    def _send_inform_response(self, soap_header):
        """Send an InformResponse back"""
        cwmp_id = None
        out_buffer = cStringIO.StringIO()

        if "cwmp:ID" in soap_header:
            cwmp_id = soap_header["cwmp:ID"]["#text"]

        # Build Response
        out_buffer.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        out_buffer.write("<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">\n")
        out_buffer.write("                  xmlns:cwmp=\"urn:dslforum-org:cwmp-1-0\">\n")
        out_buffer.write(" <soapenv:Header>\n")

        # Include the CWMP ID if it was in the Inform
        if cwmp_id is not None:
            out_buffer.write(
                "  <cwmp:ID soapenv:mustUnderstand=\"1\">{}</cwmp:ID>\n".format(cwmp_id))

        # Finish building the Response
        out_buffer.write(" </soapenv:Header>\n")
        out_buffer.write(" <soapenv:Body>\n")
        out_buffer.write("  <cwmp:InformResponse>\n")
        out_buffer.write("   <MaxEnvelopes>1</MaxEnvelopes>\n")
        out_buffer.write("  </cwmp:InformResponse>\n")
        out_buffer.write(" </soapenv:Body>\n")
        out_buffer.write("</soapenv:Envelope>\n")

        # Send Response
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(out_buffer.getvalue())
        self._write_outgoing_cwmp_message(out_buffer.getvalue())

        out_buffer.close()



    def _terminate_cwmp_session(self):
        """Terminate the CWMP Session by sending an HTTP 204 response"""
        logger = logging.getLogger(self.__class__.__name__)

        # Tell the Server to stop responding to HTTP Requests
        self.server.stop_serving()

        # Send an HTTP 204 Response to terminate the CWMP Session
        self.send_response(204)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("")

        logger.info("Terminating the CWMP Session with an HTTP 204")
        self._write_outgoing_cwmp_message("<EMPTY>")



class DataModelObject(object):
    """Represents an implemented Data Model Object"""
    def __init__(self):
        """Initialize the Data Model Object"""
        self.name = None
        self.access = None
        # TODO: Do we want/need to keep object heirarchy? - I don't think so
#        self.sub_objects = []
        self.parameters = []


    def get_name(self):
        """Retrieve the Data Model Parameter's name"""
        return self.name

    def set_name(self, value):
        """Set the name of the Data Model Parameter"""
        self.name = value


    def get_access(self):
        """Retrieve the Data Model Parameter's access"""
        return self.access

    def set_access(self, value):
        """Set the access of the Data Model Parameter"""
        self.access = value


    def add_parameter(self, item):
        """Add a Data Model Parameter to this Data Model Object"""
        self.parameters.append(item)

    def get_parameters(self):
        """Retrieve the list of Data Model Parameters"""
        return self.parameters



class DataModelParameter(object):
    """Represents an implemented Data Model Parameter"""
    def __init__(self):
        """Initialize the Data Model Parameter"""
        self.name = None
        self.access = None
        self.value = None


    def get_name(self):
        """Retrieve the Data Model Parameter's name"""
        return self.name

    def set_name(self, value):
        """Set the name of the Data Model Parameter"""
        self.name = value


    def get_access(self):
        """Retrieve the Data Model Parameter's access"""
        return self.access

    def set_access(self, value):
        """Set the access of the Data Model Parameter"""
        self.access = value


    def get_value(self):
        """Retrieve the Data Model Parameter's value"""
        return self.value

    def set_value(self, value):
        """Set the value of the Data Model Parameter"""
        self.value = value



if __name__ == "__main__":
    logging.basicConfig(filename="logs/cwmp-testing.log",
                        format='%(asctime)-15s %(name)s %(levelname)-8s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    tester = DataModelSanityTester()
    tester.start_server()
    tester.test()
