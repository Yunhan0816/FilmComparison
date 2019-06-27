# Created and edited by Yunhan Huang
# yunhanh@bu.edu

# Created and edited by Yunhan Huang
# yunhanh@bu.edu

#import xlrd
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import jieba

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
    ccms.update({iD_name: df['douban_link'][i]})

douban = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD + "|" + name
    douban.update({iD_name: df2['douban_link'][i]})

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

# compare titles from two sources and generates a new dictionary with similar pairs
def search_title(d1, d2):
    new_dict = {}
    score_id = {}
    for x in d1:
        new_set = set()
        for y in d2:
            for i in range(len(d1[x])-2):
                for j in range(len(d2[y])-2):
                    if d1[x][i] == d2[y][j]:
                        #print(d1[x][i])
                        #print(d2[y][j])
                        new_set.add(y)
                        #count+=1
            new_dict[x] = new_set
    print(len(new_dict.keys()))

    return new_dict

#print(cut(ccms_title))
title_similar = search_title(cut(ccms_title), cut(douban_title))
#print(title_similar)

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

#print(search_person(director1, director2))
#print(search_person(writer1, writer2))
#print(search_person(actor1, actor2))
writer_score = search_person(writer1, writer2)
actor_score = search_person(actor1, actor2)
director_score = search_person(director1, director2)


def main_function():
    dic = {}
    for name_id in title_similar:
        if name_id not in director_score:
            if name_id not in actor_score:
                if name_id not in writer_score:
                    dic = title_similar
                else:
                    dic[name_id] = writer_score[name_id]
            else:
                if name_id not in writer_score:
                    dic[name_id] = actor_score[name_id]
                else:
                    same_actor_writer = {x: actor_score[x] for x in actor_score if x in writer_score}
                    dic = same_actor_writer
        else:
            same_director_actor = {x: director_score[x] for x in director_score if x in actor_score}
            director_actor_writer = {x: same_director_actor[x] for x in same_director_actor if x in writer_score}
            dic = director_actor_writer
    print(len(dic.keys()))
    return dic

print(main_function())


#print(filter_tree(ccms_title, douban_title))

def title_director():
    result = {}
    count = 0
    for x in title_similar:
        i = df[df.assets_id == int(x)].index[0]
        j = df2[df2.assets_id == int(title_similar[x])].index[0]
        if df.loc[i, "director"] != "" and df2.loc[j, "director"]!= "":
            if df.loc[i, "director"] == df2.loc[j, "director"] :
                result[x] = title_similar[x]
                count+=1
        else:
            if df.loc[i, "year"]!= None and df2.loc[j, "year"]!= None:
                if df.loc[i, "year"] in range(df2.loc[j,"year"] -1, df2.loc[j,"year"]+2):
                    result[x] = title_similar[x]
                    count+=1
    print(count)
    return result

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

 
