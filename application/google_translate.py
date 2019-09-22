#!/usr/bin/env python
# coding=utf-8

# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client.from_service_account_json('C:\\Users\\zan.wang\\'
                                                              'Downloads\\transsion-tecno-ef0340407413.json')

# The target language
target = 'zh-cn'

f1 = open("C:\\Users\\zan.wang\\Downloads\\word1.txt", 'a')
with open("C:\\Users\\zan.wang\\Downloads\\word.txt", 'r') as file:
    data_lines = file.readlines()

for text in data_lines:
    text = text.strip('\n')
    translation = translate_client.translate(text, target_language=target)
    print(text + "," + translation['translatedText'] + '\n')
    f1.write(text + "," + translation['translatedText'] + '\n')

file.close()
f1.close()


