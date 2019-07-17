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


#texts = [(seg_sentence(douban_summary[x])) for x in douban_summary]
#print(texts)
#for x in douban_summary:
 #   print(seg_sentence(douban_summary[x]))

# use GENSIM to calculate the similarity score between titles
def gensimcalculation(d1, d2):

    # train the model first
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
        iDs = [y for y in d2]
        new_vec = dictionary.doc2bow(seg_sentence(text1))
        indx = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
        sim = indx[tfidf[new_vec]] # list of similarity scores

        #pairId = ""
        maxSim = max(sim)

        count = 0
        for i in range(len(sim)):
            if sim[i] == maxSim:
                count = i

        iD = iDs[count]
        new_dict[x] = {iD: maxSim}

    print(new_dict)

    return new_dict

#print(title_similar)

#title_similar = gensimcalculation(ccms_title, douban_title)
#print(title_similar)
#summary_similar = gensimcalculation(ccms_summary, douban_summary)
#print(summary_similar)
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

similar_person = search_person(persons1, persons2)
file1 = open("similar_person.txt", "w+")
file1.write(str((similar_person)))

#print("This is the writer similarity score: ")
#writer_score = search_person(writer1, writer2)
#print(writer_score)
#print("This is the actor similarity score: ")
#actor_score = search_person(actor1, actor2)
#print(actor_score)
#print("This is the director similarity score: ")
#director_score = search_person(director1, director2)
#print(director_score)



def main_function():
    for name_id in title_similar:

def main_function():
    dictitle = {}
    dictitle_summary = {}
    dictitle_writer = {}
    dictitle_writer_summary = {}

    dictitle_actor = {}
    dictitle_actor_summary = {}
    dictitle_actor_writer = {}
    dictitle_actor_writer_summary = {}

    dictitle_director = {}
    dictitle_director_summary = {}
    dictitle_director_writer = {}
    dictitle_director_writer_summary = {}

    dictitle_director_actor= {}
    dictitle_director_actor_summary = {}
    dictitle_director_actor_writer = {}
    dictitle_director_actor_writer_summary = {}

    dictdouban = {}

    f1 = open("title.txt", "w+")
    f2 = open("title_summary.txt","w+")
    f3 = open("title_writer.txt", "w+")
    f4 = open("title_writer_summary.txt", "w+")
    f5 = open("title_actor.txt", "w+")
    f6 = open("title_actor_summary.txt", "w+")
    f7 = open("title_actor_writer.txt", "w+")
    f8 = open("title_actor_writer_summary.txt", "w+")
    f9 = open("title_director.txt", "w+")
    f10 = open("title_director_summary.txt", "w+")
    f11 = open("title_director_writer.txt", "w+")
    f12 = open("title_director_writer_summary.txt", "w+")
    f13 = open("title_director_actor.txt", "w+")
    f14 = open("title_director_actor_summary.txt", "w+")
    f15 = open("titile_director_actor_writer.txt" , "w+")
    f16 = open("title_director_actor_writer_summary.txt", "w+")
    f17 = open("douban.txt", "w+")

    for name_id in title_similar: # 每一个id在题目相似度里
        if name_id in same_douban: # 查看是否豆瓣链接相同
            #print(same_douban)
            dictdouban = same_douban
        else:   #豆瓣链接不相同
            if name_id not in director_score: #如果没有在导演相似里
                if name_id not in actor_score: #如果没有在演员相似里
                    if name_id not in writer_score: #如果没有在编剧相似里
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: # 如果没有在简介相似里
                            dictitle = title_similar #字典就是题目相似
                        else: #如果在简介相似里，标题和简介交集
                            if title_similar[name_id].keys() == summary_similar[name_id].keys():
                                same_ids = set(title_similar[name_id].keys()) & set(summary_similar[name_id].keys())
                                intersection = {}

                                for elem in same_ids:
                                    intersection[elem] = 0.5 * title_similar[name_id][elem] + 0.5 * summary_similar[name_id][elem]
                                dictitle_summary = {name_id: intersection}
                    else: #如果在编剧相相似
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: #如果不在简介相似里
                            if list(title_similar[name_id].keys())[0] in writer_score[name_id].keys():
                                same_ids = set(title_similar[name_id].keys()) & set(writer_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.6 * writer_score[name_id][elem] + 0.4* title_similar[name_id][elem]
                                dictitle_writer = {name_id: intersection}
                        else:#如果在简介相似里
                            if list(title_similar[name_id].keys())[0] in writer_score[name_id].keys() and set(title_similar[name_id].keys() )== set(summary_similar[name_id].keys()):
                                same_ids = (set(title_similar[name_id].keys()) & set(writer_score[name_id].keys())) & set(summary_similar[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.3 * title_similar[name_id][elem] + 0.4 * writer_score[name_id][elem] + 0.3 * summary_similar[name_id][elem]
                                dictitle_writer_summary = {name_id: intersection}

                else: #如果在演员相似里
                    if name_id not in writer_score: #如果不在编剧相似里
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: # 如果不在简介相似
                            if list(title_similar[name_id].keys())[0] in actor_score[name_id].keys():
                                same_ids = set(title_similar[name_id].keys()) & set(actor_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.3 * title_similar[name_id][elem] + 0.7 * actor_score[name_id][elem]
                                dictitle_actor = {name_id: intersection}
                        else: #如果在简介相似
                            if list(title_similar[name_id].keys())[0] in actor_score[name_id].keys() and set(title_similar[name_id].keys() ) == set(summary_similar[name_id].keys()):
                                same_ids = (set(title_similar[name_id].keys()) & set(actor_score[name_id].keys())) & set(summary_similar[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.2 * title_similar[name_id][elem] + 0.5 * actor_score[name_id][elem] + 0.3 * summary_similar[name_id][elem]
                                dictitle_actor_summary = {name_id: intersection}

                    else: #在演员相似&在编剧相似
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: # 如果不在简介相似
                            if list(title_similar[name_id].keys())[0] in actor_score[name_id].keys() and list(title_similar[name_id].keys())[0] in writer_score[name_id].keys():
                                same_ids = (set(title_similar[name_id].keys()) & set(actor_score[name_id].keys()) )&  set(writer_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.2 * title_similar[name_id][elem] + 0.5 * actor_score[name_id][elem] + 0.3 * writer_score[name_id][elem]
                                dictitle_actor_writer = {name_id: intersection}
                        else: # 如果在简介相似: 演员相似& 编剧相似& 简介相似
                            if list(title_similar[name_id].keys())[0] in actor_score[name_id].keys() and list(title_similar[name_id].keys())[0] in writer_score[name_id].keys() and list(title_similar[name_id].keys())[0] == list(summary_similar[name_id].keys())[0]:
                                same_ids =( set(title_similar[name_id].keys()) & set(actor_score[name_id].keys()))  & ( set(writer_score[name_id].keys()) & summary_similar[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.3 * actor_score[name_id][elem] + 0.2 * title_similar[name_id][elem] + 0.3* writer_score[name_id][elem] + 0.2 * summary_similar[name_id][elem]
                                dictitle_actor_writer_summary = {name_id: intersection}
            else: #如果在导演相似
                if name_id not in actor_score: #不在演员相似
                    if name_id not in writer_score: # 不在编剧相似
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: # 不在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys():
                                same_ids = set(title_similar[name_id].keys()) & set(director_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.6* director_score[name_id][elem] + 0.4 * title_similar[name_id][elem]
                                dictitle_director = {name_id: intersection}
                        else: # 在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and title_similar[name_id].keys()== summary_similar[name_id].keys():
                                same_ids = (set(title_similar[name_id].keys()) & set(director_score[name_id].keys())) & set(summary_similar[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.3* title_similar[name_id][elem] + 0.3 * summary_similar[name_id][elem] + 0.4 * director_score[name_id][elem]
                                dictitle_director_summary = {name_id: intersection}
                    else: # 不在演员，在编剧相似
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: # 不在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and list(title_similar[name_id].keys())[0] in writer_score[name_id].keys():
                                same_ids = (set(title_similar[name_id].keys()) & set(director_score[name_id].keys())) & set(writer_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    print(elem)
                                    intersection[elem] = 0.2 * title_similar[name_id][elem] + 0.4 * writer_score[name_id][elem] + 0.4 * director_score[name_id][elem]
                                dictitle_director_writer = {name_id: intersection}

                        else: # 在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and list(title_similar[name_id].keys())[0] in writer_score[name_id].keys() and title_similar[name_id].keys() == summary_similar[name_id].keys():
                                same_ids = (set(title_similar[name_id].keys()) & set(director_score[name_id].keys())) & ( set(writer_score[name_id].keys()) & set(summary_similar[name_id].keys()))
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.4 * director_score[name_id][elem] + 0.3 * writer_score[name_id][elem] + 0.2 * title_similar[name_id][elem] + 0.1 * summary_similar[name_id][elem]
                                dictitle_director_writer_summary = {name_id: intersection}

                else: #在演员相似
                    if name_id not in writer_score: # 不在编剧相似
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: #不在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and list(title_similar[name_id].keys())[0] in actor_score[name_id].keys():
                                same_ids = ( set(title_simimlar[name_id].keys()) & set(director_score[name_id].keys()) ) & set(actor_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.2 * title_similar[name_id][elem] + 0.4*writer_score[name_id][elem] + 0.4*director_score[name_id][elem]
                                dictitle_director_actor = {name_id: intersection}
                        else: #在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and list(title_similar[name_id].keys())[0] in actor_score[name_id].keys() and title_similar[name_id].keys() == summary_similar[name_id].keys():
                                same_ids = (set(title_similar[name_id].keys()) & set(director_score[name_id].keys())) & ( set(actor_score[name_id].keys()) & set(summary_similar[name_id].keys()))
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.3 * director_score[name_id][elem] + 0.3 * actor_score[name_id][elem] + 0.2 * title_similar[name_id][elem] + 0.2 * summary_similar[name_id][elem]
                                dictitle_director_actor_summary = {name_id: intersection}
                    else: # 在编剧相似
                        if summary_similar[name_id].get(list(summary_similar.keys())[0]) == 0.0: #不在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and list(title_similar[name_id].keys())[0] in writer_score[name_id].keys() and list(title_similar[name_id].keys())[0] in actor_score[name_id].keys():
                                same_ids =( set(title_similar[name_id].keys()) & set(director_score[name_id].keys()) ) &  ( set(actor_score[name_id].keys()) & writer_score[name_id].keys())
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.1 * title_similar[name_id][elem] + 0.3 * director_score[name_id][elem] + 0.3 * actor_score[name_id][elem] + 0.3 * writer_score[name_id][elem]
                                dictitle_director_actor_writer = {name_id: intersection}

                        else: #在简介相似
                            if list(title_similar[name_id].keys())[0] in director_score[name_id].keys() and list(title_similar[name_id].keys())[0] in writer_score[name_id].keys() and list(title_similar[name_id].keys())[0] in actor_score[name_id].keys() and title_similar[name_id].keys() == title_similar[name_id].keys():
                                same_ids = (( set(title_similar[name_id].keys()) & set(director_score[name_id].keys()) ) &  ( set(actor_score[name_id].keys()) & writer_score[name_id].keys()) ) & summary_similar[name_id].keys()
                                intersection = {}
                                for elem in same_ids:
                                    intersection[elem] = 0.1 * title_similar[name_id][elem] + 0.1* summary_similar[name_id][elem] + 0.2 * director_score[name_id][elem] + 0.3 * actor_score[name_id][elem] + 0.1 * writer_score[name_id][elem]
                                dictitle_director_actor_writer_summary = {name_id: intersection}

    f1.write(str(dictitle))
    f2.write(str(dictitle_summary))
    f3.write(str(dictitle_writer))
    f4.write(str(dictitle_writer_summary))
    f5.write(str(dictitle_actor))
    f6.write(str(dictitle_actor_summary))
    f7.write(str(dictitle_actor_writer))
    f8.write(str(dictitle_actor_writer_summary))
    f9.write(str(dictitle_director))
    f10.write(str(dictitle_director_summary))
    f11.write(str(dictitle_director_writer))
    f12.write(str(dictitle_director_writer_summary))
    f13.write(str(dictitle_director_actor))
    f14.write(str(dictitle_director_actor_summary))
    f15.write(str(dictitle_director_actor_writer))
    f16.write(str(dictitle_director_actor_writer_summary))
    f17.write(str(dictdouban))

    print(len(dictdouban.keys()))
    print(len(dictitle.keys()))
    print(len(dictitle_summary.keys()))
    print(len(dictitle_writer.keys()))
    print(len(dictitle_writer_summary.keys()))
    print(len(dictitle_actor.keys()))
    print(len(dictitle_actor_summary.keys()))
    print(len(dictitle_actor_writer.keys()))
    print(len(dictitle_actor_writer_summary.keys()))
    print(len(dictitle_director_writer.keys()))
    print(len(dictitle_director_writer_summary.keys()))
    print(len(dictitle_director_actor.keys()))
    print(len(dictitle_director_actor_summary.keys()))
    print(len(dictitle_director_actor_writer.keys()))
    print(len(dictitle_director_actor_writer_summary.keys()))

    #print(len(dic.keys()))
    return None

#print(main_function())


# TYPE:
same_type = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD+ "|"+name
    same_type.update({iD: df['show_type'][i]})

same_type2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD + "|" + name
    same_type2.update({iD: df2['show_type'][i]})

#REGION
same_region = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD+ "|"+name
    same_region.update({iD_name: df['region'][i]})


same_region2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD+"|"+ name
    same_region2.update({iD_name: df2['region'][i]})

def compare_region1(dict1, dict2):
    score = {}
    for x in dict1:
        for y in dict2:
            if dict1[x] == dict2[y]:
                score[x] = y
                break
            score[x] = 0
    return score


#def total_score(dict1, dict2):
