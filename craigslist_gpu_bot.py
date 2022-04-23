import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def craigslist_search_encoder(s):
	return s.replace(" ", "+")


searches = ['bmw 330ci'] #searching sfbay craigslist for sale with this search key
prices = []
titles = []
links = []

for search in searches:

	response = requests.get('https://sfbay.craigslist.org/d/for-sale/search/sss?query=' + craigslist_search_encoder(search) + '&sort=rel')

	html_soup = BeautifulSoup(response.text, 'html.parser')

	posts = html_soup.find_all('li', class_= 'result-row')
	
	results_num = html_soup.find('div', class_= 'search-legend')
	results_total = int(results_num.find('span', class_='totalcount').text) #pulled the total count of posts as the upper bound of the pages array

	pages = np.arange(0, results_total+1, 120)

	for page in pages:

		for i in range(len(posts)):

			post_price = posts[i].a.text.strip()[1:].replace(",", "") #grabs the text for price, strips whitespaces, removes dollar sign, then removes commas to convert to int
			if post_price == '':
				post_price = 0
			prices.append(int(post_price))

			post_title = posts[i].find('a', class_='result-title hdrlnk')
			titles.append(post_title.text)

			post_link = post_title['href']
			links.append(post_link)

dict = {
	'Title' : titles,
	'Price' : prices,
	'Link'	: links
}

df = pd.DataFrame(dict)
df.sort_values(by="Price").to_csv('cls_gpu_search.csv') #saves data in csv file with title of search key
print(df.sort_values(by="Price"))
