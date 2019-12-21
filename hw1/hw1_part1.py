import requests
from bs4 import BeautifulSoup
import re
import time

basic_url = 'https://www.kinopoisk.ru/top/lists/1/filtr/all/sort/order/perpage/200/page/'
text1 = 'C:\\Users\\Анастасия\\Desktop\\Учеба\\Программирование\\new_text1.html'
user_agent = {'User-agent': 'Mozilla/5.0'}

def getting_pages():
    i = 1
    response = ''
    while i < 4:
        new_url = basic_url + str(i)
        new_response = requests.get (new_url, headers = user_agent)
        i += 1
        time.sleep(20)
        response = response + new_response.text
    return response

def find_all_movies(response):
    re_movie_info = re.compile('<tr (.*?)</tr>', re.DOTALL)
    movie_info_list = re.findall(re_movie_info, response)
    return movie_info_list

def find_all_info(movie_info):
    re_movie_name = re.compile('data-film-title="(.*?)"')
    re_kp_rating = re.compile('data-film-rating="(.*?)"')
    re_imdb_rating = re.compile('IMDb: (.*?)<small')
    re_year = re.compile('\((\d+)\) <nobr')
    re_part_url = re.compile('data-kp-film-id="(.*?)"')
    movie_name = re.findall(re_movie_name, movie_info)
    kp_rating = re.findall(re_kp_rating, movie_info)
    imdb_rating = re.findall(re_imdb_rating, movie_info)
    year = re.findall(re_year, movie_info)
    part_url = re.findall(re_part_url, movie_info)
    full_url = 'https://www.kinopoisk.ru/film/' + str(part_url[0]) + '/'
    dict_movie = {'name':movie_name[0],
                  'kp_rating':float(kp_rating[0]),
                  'imdb_rating':float(imdb_rating[0]),
                  'year':int(year[0]),
                  'url':full_url}
    print(dict_movie)
    return dict_movie

response = getting_pages()
movie_info_list = find_all_movies(response)
output_list = []
for movie in movie_info_list:
    output_list.append(find_all_info(movie))
print (len(output_list), '\n', output_list)
