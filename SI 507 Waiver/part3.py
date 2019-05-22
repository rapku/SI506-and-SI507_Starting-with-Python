import requests
from bs4 import BeautifulSoup

page = 'https://www.michigandaily.com/'
reqpage = requests.get(page)
a = reqpage.text[922:]
soup = BeautifulSoup(a, 'html.parser')

b = soup.aside.find_all('li')

print("Michigan Daily -- MOST READ")
for x in range(len(b)):
	print(b[x].string)
	nexturl = page + (b[x].a.get('href'))
	respurl = requests.get(nexturl).text
	iteratingsoup = BeautifulSoup(respurl, 'html.parser')
	print(" Author:",iteratingsoup.find('div', attrs = {'class':'link'}).contents[0].string)


# [
# <li class="first"><a href="/section/campus-life/update-university-confirms-richard-spencer-has-requested-speak-u">UPDATE: University confirms Richard Spencer has requested to speak at 'U'</a></li>, 
# <li><a href="/section/arts/darkness-and-occult-brief-history-doom">Darkness and the Occult: A brief history of doom metal</a></li>, 
# <li><a href="/section/crime/landmark-student">University student reports property damage by roommate after coming out as gay</a></li>, 
# <li><a href="/section/mic/white-rice-was-excellent-followed-directions-bag-perfectly-way-go">"The white rice was excellent. Followed the directions on the bag perfectly. Way to go."</a></li>, 
# <li class="last"><a href="/section/black-voices/classified-yet-obvious-room-sale-dm-details">Classified yet obvious: room for sale, dm for details </a></li>
# ]
