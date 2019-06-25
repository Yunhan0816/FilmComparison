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
#print(ccms_title)


douban_title = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD + "|" + name
    douban_title[iD] = name

#print(douban_title)


#Use jieba to cut the title for future comparison
def cut(d):
    new_dict = {}
    for x in d:
        new_dict[x]= jieba.lcut(d[x])
    return new_dict

# compare titles from two sources and generates a new dictionary with similar pairs
def search_title(d1, d2):
    new_dict = {}
    count = 0
    for x in d1:
        for i in range(len(d1[x])-2):
            for y in d2:
                for j in range(len(d2[y])-2):
                    if d1[x][i] == d2[y][j] and d1[x][i+1] == d2[y][j+1] and d1[x][i+2] == d2[y][j+2]:
                        new_dict[x] = y
                        count +=1
    print(count)
    return new_dict

title_similar = search_title(cut(ccms_title), cut(douban_title))


#clean the data that has "," and put them in a set for easier checking
def devide(d):
    new_dict = {}
    for x in d:
        if d[x] != None:
            #print(d[x])
            name_list = (d[x]).split(",")
            #print(name_list)
            new_dict[x] = set(name_list)
    return new_dict


# actor
actor1 = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD + "|" + name
    actor1[iD] = df['actor'][i]
actor2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD + "|" + name
    actor2[iD] = df2['actor'][i]
#DIRECTOR
director1 = {}
for i in range(len(df['assets_id'])):
    name = df['assets_name'][i]
    iD = str(df['assets_id'][i])
    iD_name = iD + "|" + name
    director1.update({iD: df['director'][i]})

director2 = {}
for i in range(len(df2['assets_id'])):
    name = df2['assets_name'][i]
    iD = str(df2['assets_id'][i])
    iD_name = iD+"|"+ name
    director2.update({iD: df2['director'][i]})

#clean the data
actor1 = devide(actor1)
actor2 = devide(actor2)
director1 = devide(director1)
director2 = devide(director2)


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
def title_director_actor():
    result = {}
    count = 0
    for x in title_similar:
        if director1[x] != "" and director2[title_similar[x]]!= "":
            for elem1 in director1[x]:
                if elem1 in director2[title_similar[x]]:
                    result[x] = title_similar[x]
                    count+=1
                    #print("题目相似+相同导演！")
        elif actor1[x] != "" and actor2[title_similar[x]]!= "":
            for elem1 in actor1[x]:
                if elem1 in actor2[title_similar[x]]:
                    result[x] = title_similar[x]
                    count +=1
                    #print("题目相似+相同演员！")

    print(count)

    return result

print(title_director_actor())


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
