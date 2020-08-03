import requests,json
from lxml import etree

urls = ['''
        https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?os=ios&for_mobile=1&start=0&count=18
      ''']
# for i in range(1,11):
#     urls.append('https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?os=ios&for_mobile=1&start={}&count=18&loc_id=108288&_=1554105184140'.format(18*i))
# print(urls)
headers = {
    'Host': 'm.douban.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://m.douban.com/movie/nowintheater?loc_id=108288',
    'Accept': '*/*'
}
movie_list = []
movie_dict = {}
for url in urls:
    res = requests.get(url,headers=headers)
    json_str = res.content.decode()
    json_dic = json.loads(json_str)
    movies = json_dic['subject_collection_items']
    for each in movies:
        movie_dict['info'] = each['card_subtitle']
        movie_dict['year'] = each['year']
        movie_list.append(movie_dict.copy())
for each in movie_list:
    print(each)
