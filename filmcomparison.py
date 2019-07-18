# Created and edited by Yunhan Huang
# yunhanh@bu.edu

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import jieba
from gensim import corpora, models, similarities

df = pd.read_excel ("/Users/huangyunhan/Desktop/ccms.xlsx", sheetname = 'Sheet1', skipinitialspace = True)
df2 = pd.read_excel("/Users/huangyunhan/Desktop/douban.xlsx", sheetname = "Sheet1", skipinitialspace = True)

# 处理不完整信息 avoid nan error
df['director'] = df['director'].fillna("")
df['actor'] = df['actor'].fillna("")
df['douban_link'] = df['douban_link'].fillna("")
df2['director'] = df2['director'].fillna("")
df2['actor'] = df2['actor'].fillna("")
df2['year'] = df2['year'].fillna("")
df['year'] = df['year'].fillna("")
df['writer'] = df['writer'].fillna("")
df2['writer'] = df2['writer'].fillna("")
df['summary'] = df['summary'].fillna("")
df2['summary'] = df2['summary'].fillna("")

#clean the data that has "," and put them in a set for easier checking
def divide_comma(d):
    new_dict = {}
    for x in d:
        if d[x] != None:
            #print(d[x])
            name_list = (d[x]).split(",")
            #print(name_list)
            new_dict[x] = set(name_list)
    return new_dict

def divide_slash(d):
    new_dict = {}
    for x in d:
        if d[x] != None:
            name_list = (d[x]).split("/")
            new_dict[x] = set(name_list)
    return new_dict
# actor
actor1 = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD + "|" + name
    #if df['actor'][i] == Nan:
    actor1[iD] = df['actor'][i]
actor1 = divide_comma(actor1)

actor2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD + "|" + name
    actor2[iD] = df2['actor'][i]
actor2 = divide_slash(actor2)

#DIRECTOR
director1 = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD + "|" + name
    director1[iD] = df['director'][i]
director1 = divide_comma(director1)

director2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD+"|"+ name
    director2[iD] = df2['director'][i]
director2 = divide_slash(director2)


#WRITER
writer1 = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD + "|" + name
    writer1[iD] = df['writer'][i]

writer2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD+"|"+ name
    writer2[iD] = df2['writer'][i]

writer1 = divide_comma(writer1)
writer2 = divide_slash(writer2)

#print(actor1)
persons1 = {}
for i in range(len(df['assets_id'])):
    iD = str(df['assets_id'][i])
    persons = (director1[iD].union(actor1[iD]) ).union(writer1[iD])
    persons1[iD] = persons
#persons2 = {}
#print(persons1)

persons2 = {}
for i in range(len(df2['assets_id'])):
    iD = str(df2['assets_id'][i])
    persons = (director2[iD].union(actor2[iD]) ).union(writer2[iD])
    persons2[iD] = persons

#Use jieba to cut the title for future comparison
def cut(d):
    new_dict = {}
    for x in d:
        new_dict[x]= lcut(d[x])
    return new_dict

#Doubanlink
ccms = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD+ "|"+name
    ccms.update({iD: df['douban_link'][i]})

douban = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD + "|" + name
    douban.update({iD: df2['douban_link'][i]})

def compare_doubanlink(dict1, dict2):
    result = {}
    for x in dict1:
        for y in dict2:
            if dict1[x] == dict2[y]:
                result[x]= y
            #result[x] = 0
    return result

same_douban = compare_doubanlink(ccms, douban)
#print(same_douban)

ccms_title = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    ccms_title[iD] = name

douban_title = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    douban_title[iD] = name
#print(cut(ccms_title))
# compare titles from two sources and generates a new dictionary with similar pairs

#print([jieba.lcut(douban_title[x]) for x in douban_title ])


df['summary'] = df['summary'].str.replace(u'\u3000', u'')
df2['summary'] = df2['summary'].str.replace(u'\u3000', u'')

ccms_summary = {}
for i in range(len(df['assets_id'])):
    name = df['summary'][i]
    iD = str(df['assets_id'][i])
    ccms_summary[iD] = name

douban_summary = {}
for i in range(len(df2['assets_id'])):
    name = df2['summary'][i]
    iD = str(df2['assets_id'][i])
    douban_summary[iD] = name
#print(ccms_summary)
#print(douban_summary)


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding = 'utf-8').readlines()]
    return stopwords

def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('./Desktop/stopwords.txt')  # 这里加载停用词的路径
    outstr = []
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                if word != " ":
                    outstr.append(word)

    return outstr

# use GENSIM to calculate the similarity score between titles
def gensimcalculation(d1, d2):

    # train the model
    new_dict = {}
    texts = [seg_sentence(d2[y]) for y in d2]
    dictionary = corpora.Dictionary(texts)
    feature_cnt = len(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    result = {}
    #calculate similarity
    for x in d1:
    #    print("!")
        text1 = d1[x]
        id_score = {}
        iDs = [y for y in d2]
        new_vec = dictionary.doc2bow(seg_sentence(text1))
        indx = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
        sim = indx[tfidf[new_vec]] # list of similarity scores
        #pairId = ""
        #maxSim = max(sim)
        for i in range(len(iDs)):
            if sim[i] >=0.05:
                id_score[iDs[i]] = sim[i]
        #count = 0
        #for i in range(len(sim)):
         #   if sim[i] == maxSim:
          #      count = i
        new_dict[x] = id_score
        #iD = iDs[count]
        #new_dict[x] = {iD: maxSim}

    return new_dict

#print(title_similar)

title_similar = gensimcalculation(ccms_title, douban_title)
print(title_similar)
summary_similar = gensimcalculation(ccms_summary, douban_summary)
print(summary_similar)
def search_person(d1, d2):
    new_dict= {}
    #new_set = set()
    for x in d1:
        id_score = {}
        for y in d2:
            count = 0
            if d1[x] == "":
                new_dict[x] = {}
            elif d1[x] != "" and d2[y] !="":
                for elem in d1[x]:
                    if elem in d2[y] and elem != "":
                        count+=1
                        #print(elem)
                        #print(d2[y])
                        #print("same person! ")
                if count != 0:
                    count = count/(len(d1[x])) # calculate similarity percentage
                    #id_score[count] = y
                    id_score[y] = count
                    #print(id_score)

        new_dict[x] = id_score
    #print(new_dict)
    for product in list(new_dict):
        #print("!")
        if new_dict[product] == {}:
            new_dict.pop(product, None)
    return new_dict

persons_similar = search_person(persons1, persons2)
file1 = open("similar_person.txt", "w+")
file1.write(str((persons_similar)))

#print(summary_similar)
#print(len(persons_similar.keys()))
def douban_function():
    dictdouban = {}
    for name_id in title_similar:
        if name_id in same_douban:
            dictdouban[name_id] = same_douban[name_id]
    return dictdouban

def main_function():
    f1 = open("remain.txt", "w+")
    f2 = open("persons.txt", "w+")
    f3 = open("summary.txt", "w+")
    f4 = open("persons_summary.txt", "w+")
    f5 = open("title.txt", "w+")
    f6 = open("title_persons", "w+")
    f7 = open("title_summary", "w+")
    f8 = open("title_persons_summary", "w+")
    dictremain = set()
    dictpersons = {}
    dictsummary = {}
    dictpersons_summary = {}
    dictitle = {}
    dictitle_persons = {}
    dictitle_summary = {}
    dictitle_persons_summary = {}
    for name_id in title_similar:
        if title_similar[name_id] =={}: #没有与此底库资产题目相似的资产
            if summary_similar[name_id] == {}: #没有与此底库资产简介相似的资产
                if name_id not in persons_similar: #没有人物相似
                    dictremain.add(name_id)
                else: #有人物相似
                    dictpersons[name_id] = persons_similar[name_id]
                    #for x in list(dictpersons[name_id]):
                     #   if dictpersons[name_id][x]<=0.5:
                      #      dictpersons[name_id].pop(x, None)
            else: #有与此底库资产简介相似的资产
                if name_id not in persons_similar: #没有人物相似
                    dictsummary[name_id] = summary_similar[name_id]
                   # for x in list(dictsummary):
                    #    if dictsummary[x] == {}:
                     #       dictsummary.pop(x, None)
                else: # 有人物相似
                    same_ids = set(summary_similar[name_id].keys()) & set(persons_similar[name_id].keys())
                    intersection = {}
                    for elem in same_ids:
                        intersection[elem] = 0.6 * persons_similar[name_id][elem] + 0.4 * summary_similar[name_id][elem]
                   # for x in list(intersection):
                    #    if intersection[x] <=0.05:
                     #       intersection.pop(x,None)
                    dictpersons_summary[name_id] =  intersection
        else: #有题目相似
            if summary_similar[name_id] == {}: #没有简介相似
                if name_id not in persons_similar: #没有人物相似
                    dictitle[name_id] = title_similar[name_id]
                   # for x in list(dictitle[name_id]):
                    #    if dictitle[name_id][x] <= 0.05:
                     #       dictitle[name_id].pop(x,None)
                else:
                    same_ids = set(title_similar[name_id].keys()) & set(persons_similar[name_id].keys())
                    intersection = {}
                    for elem in same_ids:
                        intersection[elem] = 0.3 * title_similar[name_id][elem] + 0.7 * persons_similar[name_id][elem]
                    #for x in list(intersection):
                     #   if intersection[x] <=0.05:
                      #      intersection.pop(x, None)
                    dictitle_persons[name_id] =  intersection
            else: #有简介相似
                if name_id not in persons_similar:
                    same_ids = set(title_similar[name_id].keys()) & set(summary_similar[name_id].keys())
                    intersection = {}
                    for elem in same_ids:
                        intersection[elem] = 0.6 * title_similar[name_id][elem] + 0.4 * summary_similar[name_id][elem]
                    #for x in list(intersection):
                     #   if intersection[x] <=0.05:
                      #      intersection.pop(x,None)
                    dictitle_summary[name_id] = intersection
                else:
                    same_ids = (set(title_similar[name_id].keys()) & set(summary_similar[name_id].keys()) ) & (set(persons_similar[name_id].keys()))
                    intersection = {}
                    for elem in same_ids:
                        intersection[elem] = 0.3 * title_similar[name_id][elem] + 0.4 * persons_similar[name_id][elem] + 0.3 * summary_similar[name_id][elem]
                    #for x in list(intersection):
                     #   if intersection[x] <=0.01:
                      #      intersection.pop(x,None)
                    dictitle_persons_summary[name_id] = intersection
    for x in list(dictpersons[name_id]):
        if dictpersons[name_id][x]<=0.5:
            dictpersons[name_id].pop(x, None)
    for x in list(dictsummary):
        if dictsummary[x] == {}:
            dictsummary.pop(x, None)
    for x in list(dictpersons_summary):
        if dictpersons_summary[x] == {}:
            dictpersons_summary.pop(x, None)
    for x in list(dictitle):
        if dictitle[x] == {}:
            dictitle_summary.pop(x, None)
    for x in list(dictitle_persons):
        if dictitle_persons[x] == {}:
            dictitle_persons.pop(x, None)
    for x in list(dictitle_summary):
        if dictitle_summary[x] == {}:
            dictitle_summary.pop(x, None)
    for x in list(dictitle_persons_summary):
        if dictitle_persons_summary[x] == {}:
            dictitle_persons_summary.pop(x, None)

    print("没有匹配的ID：")
    print(dictremain)
    print("只有人物相似的ID匹配")
    print(dictpersons)
    print("只有简介相似的ID匹配")
    print(dictsummary)
    print("人物和简介相似的ID匹配交集")
    print(dictpersons_summary)
    print("标题相似的ID匹配")
    print(dictitle)
    print("标题和人物相似的ID匹配交集")
    print(dictitle_persons )
    print("标题和简介相似的ID匹配交集")
    print(dictitle_summary )
    print("标题、人物和简介相似的ID匹配交集")
    print(dictitle_persons_summary)
print(main_function())
