from controller.sexualPredatorIdentification import sexualPredatorIdentification
from controller.featureCreator import StyloFeatures

__author__ = 'amendrashrestha'

import utilities.IOProperties as prop

def run():
    print(" >>> Running ...... \n")

    feature_vector_filepath = prop.feature_vector_test_filepath
    predator = 1
    tbl_name = "tbl_test_predator"
    tbl_message = "tbl_test_message_conversation"

    StyloFeatures(feature_vector_filepath, tbl_name, tbl_message, predator)
    # sexualPredatorIdentification()


if __name__ == "__main__":
    run()
