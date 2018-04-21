#информация из группы https://vk.com/dubki
#много постов , но мало комментариев 
#поэтому выгружается 200 постов и все комментарии

import codecs
import numpy
import datetime 
import urllib.request  
import json
import matplotlib.pyplot as plt
req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-16757548&count=100&v=5.74&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8') 
response = urllib.request.urlopen(req) 
result = response.read().decode('utf-8')
req1 = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-16757548&count=100&offset=100&v=5.74&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8') 
response = urllib.request.urlopen(req1) 
result1 = response.read().decode('utf-8')
data1 = json.loads(result)
data2 = json.loads(result1)
data=dict()
data.update(data1)
data['response']['items']=data1['response']['items']+data2['response']['items']


def make_file(text, idpost): #функция для создания файла .txt и дикертории к нему
    path = 'txts/' + str(idpost) 
    f = codecs.open(path + '.txt', 'w', 'utf-8')#открываем файл для записи в кодировке utf-8 ()
    f.write(text)
    f.close()

def age(st): #расчет возраста из даты в вк
    if len(st) > 4:
        st = st.split('.')
        now = datetime.datetime.now()
        then = datetime.datetime(int(st[2]), int(st[1]), int(st[0]))
        delta = now - then
        return delta.days // 365
    else:
        return -1
        
posts=[]#Длина каждого поста 
for i in range(200):
    te=data['response']['items'][i]['text']
    make_file(te,data['response']['items'][i]['id'])
    s = te.split()
    l = len(s)
    posts.append(l)
print('Длина каждого поста:\n', posts)


id1=[]#id постов для выгрузки комментариев 
for i in range(200):
    te=data['response']['items'][i]['id']
    id1.append(te)




com=[]#длина каждого комментария
comid=[]#id комментатора
for i in id1:
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-16757548&post_id='+str(i)+'&count=100&v=5.74&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8') 
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    req1 = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-16757548&post_id='+str(i)+'&count=20&offset=100&v=5.74&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8') 
    response = urllib.request.urlopen(req1) 
    result1 = response.read().decode('utf-8')
    comment1 = json.loads(result)
    comment2= json.loads(result1)
    comment=dict()
    comment.update(comment1)
    comment['response']['items']=comment1['response']['items']+comment2['response']['items']
    j=len(comment['response']['items'])
    lc=0
 
    for p in range(j):
        ss=0
        ll=0
        comm=comment['response']['items'][p]['text']
        chto=comment['response']['items'][p]['from_id']
        ss = comm.split()
        ll = ll+len(ss)
        com.append(ll)
        comid.append(chto)

print('Длина каждого комментария', com)


i=0 #удаление комментариев от групп (комментарии могу быть написаны группой)
while i<len(com):
    if comid[i]<0:
        del comid[i]
        del com[i]
    i+=1

comentators = [] #информация со страниц комментирующих
for i in comid:
    if i>0:
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=city,bdate&v=5.23&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8'.format(str(i)))
        response = urllib.request.urlopen(req) 
        result3 = response.read().decode('utf-8')
        data5 = json.loads(result3)
        comentators.append(data5['response'][0])
        
users=[] #пользователи, написавшие посты id
for i in range(200):
    users.append(data['response']['items'][i]['from_id'])



i=0 #пост может быть написан группой, поэтому удаляем комментарии группы 
while i<len(users):
    if users[i]<0:
        del users[i]
        del posts[i]
    i+=1 
    
    
userc = list()#пользователи, написавшие посты информация
for i in users:
    if i>0:
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=city,bdate&v=5.23&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8'.format(str(i)))
        response = urllib.request.urlopen(req) 
        result3 = response.read().decode('utf-8')
        data1 = json.loads(result3)
        userc.append(data1['response'][0])
        
        
        
#графики

age_dict = {} #средняя длина поста -возраст
for i in range(len(posts)):    
    try:
        a = age(userc[i]['bdate'])
        if a > -1:
            if a in age_dict:
                age_dict[a] = age_dict[a] + [posts[i]]
            else:
                age_dict[a] = [posts[i]]
    except: pass         
for i in age_dict:
    age_dict[i] = numpy.mean(age_dict[i])
plt.ylabel('Средняя длина поста')
plt.xlabel('Возраст')
plt.scatter(list(age_dict.keys()), list(age_dict.values()))
plt.show()



city_dict = {} #средняя длина поста - город
for i in range(len(posts)):    
    try:
        c = userc[i]['city']['title']
        if c in city_dict:
            city_dict[c] = city_dict[c] + [posts[i]]
        else:
            city_dict[c] = [posts[i]]
    except: pass    
for i in city_dict:
    city_dict[i] = numpy.mean(city_dict[i])
plt.bar(range(len(city_dict.keys())), city_dict.values())
plt.ylabel('Средняя длина поста')
plt.xlabel('Город')
plt.xticks(range(len(city_dict.keys())), city_dict.keys(), rotation=90)
plt.legend()
plt.show()



city_dict_com = {} #средняя длина комментария - город
for i in range(len(com)):    
    try:
        c = comentators[i]['city']['title']
        if c in city_dict_com:
            city_dict_com[c] = city_dict_com[c] + [com[i]]
        else:
            city_dict_com[c] = [com[i]]
    except: pass    
for i in city_dict_com:
    city_dict_com[i] = numpy.mean(city_dict_com[i])
plt.bar(range(len(city_dict_com.keys())), city_dict_com.values())
plt.ylabel('Средняя длина комментария')
plt.xlabel('Город')
plt.xticks(range(len(city_dict_com.keys())), city_dict_com.keys(), rotation=90)
plt.legend()
plt.show()



age_dict_com = {} #средняя длина комментария -возраст
for i in range(len(posts)):    
    try:
        a = age(comentators[i]['bdate'])
        if a > -1:
            if a in age_dict_com:
                age_dict_com[a] = age_dict_com[a] + [com[i]]
            else:
                age_dict_com[a] = [com[i]]
    except: pass
for i in age_dict_com:
    age_dict_com[i] = numpy.mean(age_dict_com[i])
plt.ylabel('Средняя длина комментария')
plt.xlabel('Возраст')
plt.scatter(list(age_dict_com.keys()), list(age_dict_com.values()))
plt.show()




