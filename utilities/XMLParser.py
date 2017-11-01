__author__ = 'amendrashrestha'

import xml.dom.minidom
import html
import utilities.IOProperties as prop
import utilities.IOReadWrite as IO
import traceback

import model.connect as conn

def parseXML(filename):
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement

    # Get all the messages in the collection
    conversations = collection.getElementsByTagName("message")

    for conversation in conversations:
        try:
            conv_author = conversation.getElementsByTagName('author')[0]
            conv_author = conv_author.childNodes[0].data

            conv_time = conversation.getElementsByTagName('time')[0]
            conv_time = conv_time.childNodes[0].data

            conv_text = conversation.getElementsByTagName('text')[0]
            text = IO.cleanText(html.unescape(conv_text.childNodes[0].data))

            post_info = [conv_author, conv_time, text]

            with open(prop.test_training_messages_filepath, "a", encoding='utf-8') as text_file:
                for item in post_info:
                    text_file.write("%s\t" % item)
                text_file.write("\n")
            # try:
            #     connect = conn.conn_db()
            #     sql = "insert into tbl_test_message_conversation VALUES('%s', '%s', '%s')" % (conv_author.strip(), conv_time.strip(), text)
            #     connect.execute(sql)
            # finally:
            #     connect.close()

        except Exception:
            traceback.print_exc()
            pass


