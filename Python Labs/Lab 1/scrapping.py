
# coding: utf-8

# In[1]:


url = 'https://fr.wikipedia.org/wiki/Discographie_de_Charles_Aznavour'


# In[21]:


import requests   # http://docs.python-requests.org/en/master/
from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from matplotlib.pyplot import plot # https://matplotlib.org/index.html
from collections import Counter # https://docs.python.org/2/library/collections.html


# In[8]:

# Transformer la réponse HTML reçue depuis requests.get en objet parcourable
soup = BeautifulSoup(requests.get(url).content,"html.parser") 


# In[10]:

# Acceder à la table qui contient la discographie d'Aznavour
table = soup.find(class_="wikitable")


# In[16]:

# Prendre de chaque ligne de la table la date de parutioin de l'album
years = []
for tr in table.findAll('tr')[1:]:
	try:
    	years.append(int(tr.find('td').getText()))
    except ValueError:
    	pass


# In[19]:


ryears = range(min(years),max(years)+1)


# In[23]:

# Créer le dictionnaire: {année:nombre_de_disques_produit}
production_charles_aznavour = {}
for year in ryears:
    if year in years:
        production_charles_aznavour[year] = Counter(years)[year]
    else:
        production_charles_aznavour[year] = 0


# In[28]:

# Dessiner la courbe nombre_de_disques_produit = f(année)
get_ipython().magic(u'matplotlib inline')
plot(ryears,[production_charles_aznavour[year] for year in ryears],'b')

