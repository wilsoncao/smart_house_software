#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import tree
import jieba
from snownlp import SnowNLP
import spider
import zmq
import sys
import time

#customized tokenizer    
def my_tokenizer(s):
    return s.split()

#这个函数初始化分词库，避免每次都需要初始化
def fenci_initalize():
	jieba.initialize()

#以下两个函数为一样的分词函数，只是返回值一个是list，一个是string
def fenci_all(sentence):
	seg_list = jieba.cut(sentence,cut_all = True)
	word_list = ' '.join(seg_list)
	return [word_list]


def fenci_all2(sentence):
	seg_list = jieba.cut(sentence,cut_all = None)
	word_list = ' '.join(seg_list)
	return word_list


#这个函数对corpus.txt里面的每一个句子进行分词
def fenci_corpus(sentences):
	corpus = []
	for sentence in sentences:
                #print sentence
		corpus.append(fenci_all2(sentence))
	return corpus


#这个函数读取语义训练库corpus.txt
def load_corpus():
   lines = list(open('corpus.txt','r'))
   Y = []
   corpus = []
   for line in lines:
      temp = line.split(' ')
      Y.append(int(temp[0]))
      corpus.append(fenci_all2(temp[1].replace('\n','')))
   return Y,corpus

#这个函数处理讯飞开放语义的内容
def jsonFunc():
    f = file('test.json')
    source = f.read()
    result = json.loads(source)

    if not result.has_key('answer'):
      return u'对不起我找不到呢'.encode('utf-8')
    elif len(result['answer']['text'].encode('utf-8')) <= 100:
      return result['answer']['text'].encode('utf-8')
    elif len(result['answer']['text'].encode('utf-8')) > 100:
      original = result['answer']['text'].encode('utf-8').replace('。','\n')
      text = SnowNLP(original)
      summary_text = ''
      for line in text.summary(3):
        summary_text = summary_text + line + u'。'.encode('utf-8')
      print summary_text
      return summary_text

#这个函数返回知乎抓取的文字内容
def jsonzhihu():
    f = file('test.json')
    source = f.read()
    result = json.loads(source)
    #print result['text']
    #print len(result['answer']['text'].encode('utf-8'))
    text = result['text']
    text  = text.encode('utf-8')
    text = str(text)
    print type(text)
    print text
    zhihu_text = spider.Spider_zhihu(text)
    print type(zhihu_text)
    return zhihu_text



#这个函数通过读取其它json以及调用决策树函数来决定选择什么功能。

def makeDecision():
        context = zmq.Context()
        print "Connecting to server..."
        socket = context.socket(zmq.REQ)
        socket.connect ("tcp://127.0.0.1:10002")
	f = file('test.json')
	source = f.read()
	result = json.loads(source)
	text = result['text']
	#
	#text = '开灯吧'
	choice = wordVectorizer_2(text)
        print choice
        if choice == 10:
                return u"0".encode('utf-8')
        elif choice == -4:
                return u"1".encode('utf-8')
        elif choice == -5:
                return u"2".encode('utf-8')
        elif choice == -6:
                return u"3".encode('utf-8')
        elif choice == -7:
                return u"-1".encode('utf-8')
        elif choice == 3:
                answer = spider.Spider_world_cup()
                print answer
                print type(answer)
                return answer
        elif choice == 4:
                return u"8 7月9日 16:50".encode('utf-8')
        elif choice == -8:
                return u"-2".encode('utf-8')
        elif choice == -9:
                return u"-3".encode('utf-8')
        elif choice == 5:
                return u"开空调".encode('utf-8')
        elif choice == 6:
                return u"关空调".encode('utf-8')
        elif choice == 7:
                return u"开窗帘".encode('utf-8')
        elif choice == 8:
                return u"关窗帘".encode('utf-8')
        elif choice == 0:
                return u"关灯".encode('utf-8')
        elif choice == 1:
                return u"开灯".encode('utf-8')
        if  result.has_key('answer'):
                return jsonFunc()
        if result.has_key('data'):
                return spider.Spider_meal()
	if choice == 0:
                socket.send('2')
                meg_in = socket.recv()
		return  u"关灯了".encode('utf-8')
	elif choice == 1:

                time.sleep(1)
                socket.send('1')
                time.sleep(1)
                #meg_in = socket.recv()
                #print meg_in
                print "ok"
		return  u"开灯了".encode('utf-8')
	elif choice == -1:
		return jsonFunc()
        elif choice == -2:
                return spider.Spider_news()
        elif choice == -3:
                print "it should work!"
                return jsonzhihu()
        elif choice == -4:
                return "1"
        elif choice == -5:
                return "2"
        elif choice == -6:
                return "3"
        elif choice == -7:
                return "-1"
        elif choice == -8:
                return "-2"
        elif choice == -9:
                return "-3"
        elif choice == 3:
                return spide.Spider_world_cup()
        elif choice == 2:
                return spider.Spider_news_context(text)
	return 0


#决策树函数
def wordVectorizer_2(s):
    s = fenci_all(s)
    Y,corpus = load_corpus()
    print type(corpus)
    vectorizer = CountVectorizer( tokenizer = my_tokenizer, min_df = 1)
    X = vectorizer.fit_transform(corpus)
    vector = vectorizer.transform(s).toarray()
    example = X.toarray()
    Y, corpus = load_corpus()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(example,Y)
    print clf.predict(vector)
    return clf.predict(vector)



def main():
    #wordVectorizer_2("开灯")
    #jsonFunc()
    #jsonzhihu()
    #spider.Spider_zhihu('怎么抓住一只狂奔的鸡')
    #wordVectorizer_2('开灯吧')
    makeDecision()


if __name__ == '__main__':
	main()
