__author__ = 'amendrashrestha'
import os

training_xml_filepath = os.path.expanduser('~') + "/Desktop/SexualPredator/training_data.xml"
training_predator_filepath = os.path.expanduser(
    '~') + "/Desktop/SexualPredator/train_predators.txt"
training_messages_filepath = os.path.expanduser('~') + "/Desktop/SexualPredator/sexual_predator_messages.tsv"

test_xml_filepath = os.path.expanduser('~') + "/Desktop/SexualPredator/test_data.xml"
test_predator_filepath = os.path.expanduser(
    '~') + "/Desktop/SexualPredator/test_predators.txt"
test_training_messages_filepath = os.path.expanduser(
    '~') + "/Desktop/SexualPredator/testing_sexual_predator_messages.tsv"

function_word_filepath = os.environ['HOME'] + '/PycharmProjects/SexualPredatorIdentification/dictionaries/Function'
LIWC_filepath = os.environ['HOME'] + '/PycharmProjects/SexualPredatorIdentification/LIWC/'

feature_vector_train_filepath = os.path.expanduser('~') + "/Desktop/SexualPredator/feature_vector_train.csv"
feature_vector_test_filepath = os.path.expanduser('~') + "/Desktop/SexualPredator/feature_vector_test.csv"