#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


def jsonFunc():
    f = file('../bin/test.json')
    source = f.read()
    result = json.loads(source)
    print result['answer']['text'].encode('utf-8')
    return result['answer']['text'].encode('utf-8')


def main():
    #wordVectorizer_2("开灯")
    jsonFunc()


if __name__ == '__main__':
	main()
