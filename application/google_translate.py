#!/usr/bin/env python
# coding=utf-8

from googletrans import Translator
translator = Translator(service_urls=['translate.google.com'])
f1 = open("C:\\Users\\Administrator\\Downloads\\word1.csv", 'a')
with open("C:\\Users\\Administrator\\Downloads\\word.csv", 'r') as file:
    data_lines = file.readlines()
for line in data_lines:
    line = line.strip('\n')
    text = translator.translate(line, src='en', dest='zh-cn').text
    f1.write(line + "," + text + '\n')


file.close()
f1.close()

