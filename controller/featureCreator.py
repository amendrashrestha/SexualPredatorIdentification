__author__ = 'amendrashrestha'

import re
import os
import time
from tqdm import *

import nltk
import numpy as np
from nltk.tokenize import TweetTokenizer

import utilities.IOProperties as prop
import model.dbScript as script
import utilities.IOReadWrite as IO


class TokenizerTransformer():
    def __init__(self, text):
        self.transform(text)

    def transform(self, X):
        tknzr = TweetTokenizer()
        return [tknzr.tokenize(x) for x in X]

class StyloFeatures():
    def __init__(self, filepath, tbl_name, tbl_message, predator):
        self.transform(filepath, tbl_name, tbl_message, predator)

    def transform(self, filepath, tbl_name, tbl_message, predator):
        print("Creating Stylometric features ..... \n")

        userlist = script.get_users(tbl_name)
        row = 0

        user_id = ['User_ID']
        lengths = ['Text_length']
        text_class = ['Class']
        word_lengths = [str(x) for x in list(range(1, 21))]
        digits = [str(x) for x in list(range(0, 10))]
        symbols = list('.?!,;:()"-\'')
        smileys = [':\')', ':-)', ';-)', ':P', ':D', ':X', '<3', ':)', ';)', ':@', ':*', ':j', ':$', '%)']
        functions = IO.get_function_words(prop.function_word_filepath)

        pos_tags = list(nltk.data.load('help/tagsets/upenn_tagset.pickle').keys())
        pos_tags = [ x for x in pos_tags if x.isalpha() ]

        hour_of_day = [str("%.2d" % x) for x in list(range(00, 24))]
        period_of_day = [x for x in list(range(0, 6))]

        # tfidf = utilities.get_wordlist(props.tfidf_filepath)
        # ngram_char = utilities.get_wordlist(props.ngram_char_filepath)

        LIWC_header = sorted(os.listdir(prop.LIWC_filepath))

        word_lengths_header = ["WordLength_"+x for x in word_lengths]

        digits_header = ["Digit_"+x for x in digits]

        symbols_header = ['dot', 'question_mark', 'exclamation', 'comma', 'semi_colon', 'colon', 'left_bracket',
                          'right_bracket', 'double_inverted_comma', 'hypen', 'single_inverted_comma']

        smilies_header = ["Smily_" +str(x) for x in list(range(1, 15))]

        pos_tags_header = ["POS_"+x for x in pos_tags]

        hour_of_day_header = ["Hour_"+x for x in hour_of_day]

        period_of_day_header = ['Period_01_04', 'Period_05_08', 'Period_09_12', 'Period_13_16', 'Period_17_20', 'Period_21_00']

        # ngaram_char_header = utilities.create_ngram_header(ngram_char)

        # header_feature = LIWC_header + lengths + word_lengths + digits_header + symbols_header + smilies_header + \
        # functions + tfidf + ngaram_char_header + user_id

        # features = LIWC_header + lengths + word_lengths + digits + symbols + smileys + functions + tfidf + \
        # ngram_char + user_id

        header_feature = LIWC_header + lengths + word_lengths_header + digits_header + symbols_header + smilies_header + \
                         functions + pos_tags_header + hour_of_day_header + period_of_day_header + user_id + text_class

        # corpus = utilities.return_corpus()

        features = LIWC_header + lengths + word_lengths + digits + symbols + smileys + functions + pos_tags + hour_of_day + period_of_day + user_id + text_class
        # print(len(features))
        vector = np.zeros(shape = (len(userlist), len(features)))

        IO.create_file_with_header(filepath, header_feature)

        for user in tqdm(userlist):
            # print(user)
            user_text = script.get_users_text(user, tbl_message)
            user_time = script.get_users_time(user, tbl_message)

            period_list_tmp = []

            for single_hour in user_time:
                if single_hour == "00":
                    single_hour = "24"
                period_day = IO.get_time_category(int(single_hour))
                period_list_tmp.append(period_day)
            # print("\n" +user_text)

            col = 0

            text_size = len(user_text.split())
            user_post_count = len(user_time)
            # x_wo_stopword = utilities.remove_stopword_from_text(x)
            # text_size_wo_stopword = len(x_wo_stopword.split())

            x_only_words = []
            for t in user_text.split():
                if (len(t) == 1 and t.isalpha()) or \
                        (len(t) > 1 and ("http" not in t and "www" not in t and "@" not in t and "#" not in t)):
                    x_only_words.append(t)
            # print(x_only_words)
            counts = nltk.FreqDist([len(tok) for tok in x_only_words])

            pos = nltk.FreqDist([b for (a, b) in nltk.pos_tag(x_only_words)])

            for feat in features:
                # print(feat)
                if col < len(LIWC_header):
                    LIWC_filepath = prop.LIWC_filepath + feat
                    LIWC_words = IO.get_function_words(LIWC_filepath)
                    count = 0

                    for single_word in LIWC_words:
                        count += sum(1 for i in re.finditer(single_word, user_text))
                    # avg_count = count / text_size
                    # print(avg_count)

                    vector[row][col] = count

                # Count text lengths
                elif col < len(LIWC_header) + len(lengths):
                    vector[row][col] = len(user_text)

                # Count word lengths
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths):
                    if int(feat) in counts.keys():
                        vector[row][col] = counts.get(int(feat)) #/ text_size
                    else:
                        vector[row][col] = 0

                # Count special symbols
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits):
                    vector[row][col] = user_text.count(feat) #/ text_size

                # Count special symbols
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols):
                    vector[row][col] = user_text.count(feat) #/ text_size

                # Count smileys
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys):
                    vector[row][col] = user_text.count(feat) #/ text_size

                # Count functions words
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys) + len(
                        functions):
                    vector[row][col] = sum(1 for i in re.finditer(feat, user_text)) #/ text_size

                # Count POS
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys) + len(functions) + len(pos_tags):

                    if feat in pos.keys():
                        vector[row][col] = pos.get(feat) #/ text_size
                    # print(pos.get(feat))

                    #
                    # # Count tfidf without stop words
                    # elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                    #         smileys) + len(
                    #         functions) + len(tfidf):
                    #     vector[row][col] = sum(1 for i in re.finditer(feat, x_wo_stopword)) / text_size_wo_stopword
                    # # print(feat)
                    # # print(sum(1 for i in re.finditer(feat, x_wo_stopword)))
                    #
                    # # Count ngram_char without stop words
                    # elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                    #         smileys) + len(
                    #         functions) + len(tfidf) + len(ngram_char):
                    # print(feat)
                    # vector[row][col] = sum(1 for i in re.finditer(feat, x_wo_stopword)) / text_size_wo_stopword
                #

                # Hour of a Day Features
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys) + len(functions) + len(pos_tags) + len(hour_of_day):

                        vector[row][col] = user_time.count(feat) #/ user_post_count

                # Period of a Day Features
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys) + len(functions) + len(pos_tags) + len(hour_of_day) + len(period_of_day):

                        vector[row][col] = period_list_tmp.count(feat) #/ user_post_count
                        # print(vector[row][col])

                # # Adding userId
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys) + len(functions) + len(pos_tags) + len(hour_of_day) + len(period_of_day) + len(user_id):

                    # + len(tfidf) + len(ngram_char) \

                    vector[row][col] = (row + 1)

                # # Adding predator class
                elif col < len(LIWC_header) + len(lengths) + len(word_lengths) + len(digits) + len(symbols) + len(
                        smileys) + len(functions) + len(pos_tags) + len(hour_of_day) + len(period_of_day) + len(user_id) + len(text_class):

                    # + len(tfidf) + len(ngram_char) \

                    vector[row][col] = predator

                # print(vector)

                if col == len(features) - 1:
                    col = 0
                    break
                col += 1

            row += 1

        with open(filepath, 'ab') as f_handle:
            np.savetxt(f_handle, vector, delimiter=",")


