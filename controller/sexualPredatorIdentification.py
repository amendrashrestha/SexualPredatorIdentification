__author__ = 'amendrashrestha'

import utilities.XMLParser as util
import utilities.IOProperties as prop
import utilities.IOReadWrite as IO
import model.dbScript as script

class sexualPredatorIdentification():
    def __init__(self):
        self.identifier()

    def identifier(self):
        script.loadPredatorFile(prop.training_predator_filepath)
        # util.parseXML(prop.test_xml_filepath)
        # script.get_users()

