# Created and edited by Yunhan Huang
# yunhanh@bu.edu

#import xlrd
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import jieba

from gensim import corpora
df = pd.read_excel ("/Users/huangyunhan/Desktop/ccms.xlsx", sheetname = 'Sheet1')
df2 = pd.read_excel("/Users/huangyunhan/Desktop/douban.xlsx", sheetname = "Sheet1")

df['director'] = df['director'].fillna("")
df['actor'] = df['actor'].fillna("")
df['douban_link'] = df['douban_link'].fillna("")
df2['director'] = df2['director'].fillna("")
df2['actor'] = df2['actor'].fillna("")
df2['year'] = df2['year'].fillna("")
df['year'] = df['year'].fillna("")
df['writer'] = df['writer'].fillna("")
df2['writer'] = df2['writer'].fillna("")


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



#Use jieba to cut the title for future comparison
def cut(d):
    new_dict = {}
    for x in d:
        new_dict[x]= jieba.lcut(d[x])
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
    iD_name = iD + "|" + name
    ccms_title[iD] = name

douban_title = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD + "|" + name
    douban_title[iD] = name
#print(cut(ccms_title))
# compare titles from two sources and generates a new dictionary with similar pairs
def search_title(d1, d2):
    new_dict = {}
    score_id = {}
    for x in d1:
        new_set = set()
        for i in range(len(d1[x])-1):
            for y in d2:
                for j in range(len(d2[y]) - 1):
                    if d1[x][i] == d2[y][j] and d1[x][i+1] == d2[y][j+1]:
                            new_set.add(y)
        new_dict[x] = new_set
    #print(len(new_dict.keys()))

    return new_dict

#print(cut(ccms_title))
title_similar = search_title(cut(ccms_title), cut(douban_title))
#print(len(title_similar.keys()))

def search_person(d1, d2):

    new_dict= {}
    #new_set = set()
    for x in d1:
        id_score = {}
        for y in d2:
            count = 0
            if d1[x] == "":
                new_dict[x] = {}
            if d1[x] != "" and d2[y] !="":
                for elem in d1[x]:
                    if elem in d2[y]:
                        count+=1
                if count !=0:
                    id_score[count] = y

        new_dict[x] = id_score
    #print(new_dict)
    for product in list(new_dict):
        #print("!")
        if new_dict[product] == {}:
            new_dict.pop(product, None)
    return new_dict

director = open("director.txt", "w+")
#director.write(str(director_score))

#print(search_person(writer1, writer2))
#print(search_person(actor1, actor2))
writer_score = search_person(writer1, writer2)

actor_score = search_person(actor1, actor2)
director_score = search_person(director1, director2)

#print(writer_score)
def main_function():
    dictitle = {}
    dictitle_writer = {}
    dictitle_actor = {}
    dictitle_actor_writer = {}
    dictitle_director = {}
    dictitle_director_writer = {}
    dictitle_director_actor= {}
    dictitle_director_actor_writer = {}
    dicdouban = {}
    title = 0
    title_writer = 0
    title_actor = 0
    title_actor_writer = 0
    title_director = 0
    title_director_writer = 0
    title_director_actor= 0
    title_director_actor_writer = 0

    f1 = open("title.txt", "w+")
    f2 = open("title_writer.txt", "w+")
    f3 = open("title_actor.txt", "w+")
    f4 = open("title_actor_writer.txt", "w+")
    f5 = open("title_director.txt", "w+")
    f6 = open("title_director_writer.txt", "w+")
    f7 = open("title_director_actor.txt", "w+")
    f8 = open("title_director_actor_writer.txt", "w+")
    f9 = open("douban.txt", "w+")

    for name_id in title_similar: # 每一个id在题目相似度里

        if name_id in same_douban: # 查看是否豆瓣链接相同
            #print(same_douban)
            dicdouban = same_douban

        else:   #豆瓣链接不相同
            if name_id not in director_score: #如果没有在导演相似里
                if name_id not in actor_score: #如果没有在演员相似里
                    if name_id not in writer_score: #如果没有在编剧相似里

                        dictitle = title_similar #字典就是题目相似
                        title +=1

                    else: #如果在编剧相似里
                        #for name_id in writer_score:
                        dictitle_writer[name_id] = writer_score[name_id]
                        title_writer +=1

                else: #如果在演员相似里
                    if name_id not in writer_score: #如果不在编剧相似里
                        #if actor_score[title_similar[name_id]] in actor_score[name_id]:
                         #   dicttitle_actor[name_id]= actor_score[name_id]
                          #  print(dicttitle_actor)
                        dictitle_actor[name_id] = actor_score[name_id]
                        title_actor+=1
                    else: #如果在编剧相似里，找演员和编剧的交集
                        same_actor_writer = {x: actor_score[x].items() & writer_score[x].items() for x in actor_score if x in writer_score and writer_score[x].items() != {} and actor_score[x].items()!= {}}
                        if same_actor_writer[name_id] != set():
                            dictitle_actor_writer[name_id] = same_actor_writer[name_id]
                        title_actor_writer+=1

                        #for x in actor_score:
                         #   if x in writer_score:
                          #      #print(actor_score[x].items())
                           #     print(actor_score[x])
                            #    print(writer_score[x].items())
                             #   print(actor_score[x].items() & writer_score[x].items())

            else: #如果在导演相似里
                if name_id not in actor_score: #如果不在演员相似里
                    if name_id not in writer_score: #如果不在编剧相似里
                        #for name_id in director_score:
                        dictitle_director[name_id] = director_score[name_id]
                        title_director+=1

                    else: #如果在编剧相似里
                        same_director_writer = {x: director_score[x].items()& writer_score[x].items() for x in director_score if x in writer_score}

                        if same_director_writer[name_id] != set():
                            dictitle_director_writer[name_id] = same_director_writer[name_id]

                        #dic[name_id] = title_similar[name_id]
                        title_director_writer+=1

                else: #如果在演员相似里
                    if name_id not in writer_score: #如果不在编剧相似里
                        same_director_actor = {x: director_score[x].items() & actor_score[x].items() for x in director_score if x in actor_score}
                        if same_director_actor[name_id] != set():

                            dictitle_director_actor[name_id] = same_director_actor[name_id]
                        title_director_actor+=1

                    else: #如果在编剧相似里
                        same_director_actor = {x: director_score[x].items() & actor_score[x].items() for x in director_score if x in actor_score}
                        director_actor_writer = {x: same_director_actor[x].intersection(writer_score[x]) for x in same_director_actor if x in writer_score}
                        if director_actor_writer[name_id]!= set():
                            dictitle_director_actor_writer[name_id] = director_actor_writer[name_id]
                        title_director_actor_writer+=1

    f1.write(str(dictitle))
    f2.write(str(dictitle_writer))
    f3.write(str(dictitle_actor))
    f4.write(str(dictitle_actor_writer))
    f5.write(str(dictitle_director))
    f6.write(str(dictitle_director_writer))
    f7.write(str(dictitle_director_actor))
    f8.write(str(dictitle_director_actor_writer))
    f9.write(str(dicdouban))
    print(title)
    print(title_writer)
    print(title_actor)
    print(title_actor_writer)
    print(title_director )
    print(title_director_writer )
    print(title_director_actor)
    print(title_director_actor_writer)
    print(len(dictitle.keys()))
    print(len(dictitle_writer.keys()))
    print(len(dictitle_actor.keys()))
    print(len(dictitle_actor_writer.keys()))
    print(len(dictitle_director.keys()))
    print(len(dictitle_director_writer.keys()))
    print(len(dictitle_director_actor.keys()))
    print(len(dictitle_director_actor_writer.keys()))
    #print(len(dic.keys()))
    return None

print(main_function())


#print(filter_tree(ccms_title, douban_title))

#def title_director():
 #   result = {}
  #  count = 0
   # for x in title_similar:
    #    i = df[df.assets_id == int(x)].index[0]
     #   j = df2[df2.assets_id == int(title_similar[x])].index[0]
      #  if df.loc[i, "director"] != "" and df2.loc[j, "director"]!= "":
       #     if df.loc[i, "director"] == df2.loc[j, "director"] :
        #        result[x] = title_similar[x]
         #       count+=1
        #else:
         #   if df.loc[i, "year"]!= None and df2.loc[j, "year"]!= None:
          #      if df.loc[i, "year"] in range(df2.loc[j,"year"] -1, df2.loc[j,"year"]+2):
           #         result[x] = title_similar[x]
            #        count+=1
   # print(count)
   # return result

#print(title_director())

#print(director1)
def title_person(d1, d2):
    result = {}
    count = 0
    for x in title_similar:
        if d1[x] != "" and d2[title_similar[x]]!= "":
            for elem1 in d1[x]:
                if elem1 in d2[title_similar[x]]:
                    print(elem1)
                    result[x] = title_similar[x]
                    count+=1

    print(count)
    return result



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
