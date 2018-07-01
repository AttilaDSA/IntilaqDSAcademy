"""
    This python file contains the definition of GithubSearchSpider class, a scrapy spider, that searches
    repositories on github for a given keyword(s) and downloads specific files from each repository.

    @python-version: 3.6.5

    @packages-versions:

        colorama : 0.3.9
        requests : 2.18.4
        scrapy : 1.5.0
        pyyaml : 3.12

    @args:
        KEYWORD : keyword to pass to github search 

    @output:
        - Send query for https://github.com/search?q={keyword}&type=Repositories
        - Download specific files from each repository (conserving the original folders
        hierarchy).
        - The specific files are the ones whom their url (file_url) verifies:
            IS_ACCEPTED_FILE(file_url) returns True

    @configs:
        REWRITE: Overwrites old files with the newly downloaded
        file, if they both have same path. (True/False)
        REVISIT: Set to true to crawl any repository even when it has been already
        checked, passes already-visited repositories otherwise. (True/False)
        HUMAN_BEHAVIOUR_SIMULATION: Github has a tough protection against scrapping.
        Setting this parameter to True will simulate a human behaviour while crawling
        the repositories. 
        BASE_SAVING_DIRECTORY: The path of the directory where all downloads will be 
        saved into. NB: Choosing a not empty directory and activating the REWRITE option
        can lead to the loss of personnal files.

"""

import colorama   # Python-Package used to print in colors on the command prompt
import requests   # Python-Package used to send http(s) queries
import random     # Python-Package used to generate random values
import scrapy     # Python-Package that offers multiple tools to scrap web pages and crawl web domains
import yaml       # Python-Package used to read or write .yml files
import time       # Python-Package defining multiple time operations (get time, sleep,...)
import os         # Python-Package designed to interact with the operating system (make directories,...)


from bs4 import BeautifulSoup   # Python-Package used to objectify HTML files
from pathlib import Path # Python-Package used manipulate file paths without compatibility problems (windows / mac/ linux)

try:
    import urllib.parse     # Python-Package cotaining generic url operations (quote, unquote, parse,...)
    unquoting_function = urllib.parse.unquote
except ImportError:
    print('**************** URLLIB NOT FOUND ********************')
    print('Downloaded files and directories will be url quoted')
    unquoting_function = lambda x:x




#*****************************
#          Configs           *
#*****************************

KEYWORD = 'games'

REWRITE = 0
REVISIT = 0

HUMAN_BEHAVIOUR_SIMULATION = True
MEAN_REQUESTS__TIME_WAIT = 3
MIN_REQUESTS__TIME_WAIT = 3
VAR_REQUESTS__TIME_WAIT = 2

BASE_SAVING_DIRECTORY = r'C:\Users\asus\Documents\Jobs\IntilaQ\Projects\Scrapping\gitscrap\Scrapped_Repositories'


def IS_ACCEPTED_FILE(url):
    """
        This function is used to validate a github file given its url.
        Only the valide files will be downloaded by the spider.

        @params:
            url : the url of the file to verify
        @returns:
            True if valid, False otherwise.
    """
    return url.endswith('.py')


#******************************










colorama.init()  # init colorama package to print in colors.

SEARCH_URL = 'https://github.com/search?p={page_num}&q={keyword}&type=Repositories'

ERROR = 0
WARNING = 1
VALIDE = 2

LAST_REQUEST_TIMER = time.time()  



#******************************


# GLOBAL FUNCTIONS

def log(msg,state=3):
    '''
        prints msg to command prompt using color depending on the msg state
        (ERROR, VALIDE or WARNING)

        @params: msg, state
    '''
    if state == ERROR:
        code = '\033[31m'
    elif state == WARNING:
        code = '\033[33m'
    elif state == VALIDE:
        code = '\033[32m'
    else:
        print(msg)
        return None

    print(code+msg+'\033[0m')



def FORMAT_KEYWORD(kw):
    return kw.replace(' ','+')


#******************************



if BASE_SAVING_DIRECTORY == '':
    log('BASE_SAVING_DIRECTORY has not been specified.',ERROR)
    exit(1)
elif not os.path.isdir(BASE_SAVING_DIRECTORY):
    log('BASE_SAVING_DIRECTORY is not a valid directory path.',ERROR)
    exit(1)
else:
    BASE_SAVING_DIRECTORY = Path(BASE_SAVING_DIRECTORY)




class GithubSearchSpider(scrapy.Spider):

    name = "gitcrawler"



    def __init__(self):
        super(GithubSearchSpider,self).__init__()
        self.current_repos_explored_urls = []




    def start_requests(self):
        """
            Function that yields starting web urls. 
        """
        urls = [
            SEARCH_URL.format(page_num=1,keyword=FORMAT_KEYWORD(KEYWORD)),
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)




    def parse(self, response):
        """
            Scraps a github search page, extracts all repositories url in order
            to explore them then yields the url for the next serach page. 
        """

        # Extract current serach page number
        try:
            indx = str(response.url).find('p=')
            page_num = int(response.url[indx+2:indx+response.url[indx:].find('&q')])
        except Exception as exc:
            page_num=None
            log('Page num not found.',ERROR)
            log(str(exc),ERROR)


        # Collect possible repositories urls from current page
        repositories = []
        for repository in response.xpath('//a[contains(@class,"v-align-middle")]'):
            repositories.append(repository.css('a::attr(href)').get())
            break


        # Yields found repositories' urls
        for repository in repositories:
            self.current_repos_explored_urls = []
            yield scrapy.Request('https://github.com'+repository, callback=self.extract_from_repos)


        # Go to Next page
        if page_num:
            next_page = SEARCH_URL.format(page_num=page_num+1,keyword=FORMAT_KEYWORD(KEYWORD))
            yield scrapy.Request(next_page, callback=self.parse)





    def extract_from_repos(self,response):
        """
            Function that:
                - verifies if the given reponse contains a valid github repostory
                (by searching for the button [CLONE or DOWNLOAD] in the webpage).
                - verifies if the repository has already been visited or not.
                - Launches the repository's exploring
                - Marks the repository as explored.

            @return:
                downloaded: sum of all downloaded files' sizes from the repository (in bytes)
        """
        try:
            with open(os.path.join(BASE_SAVING_DIRECTORY,r'visited_repos.yml'),'r') as fl:
                content = yaml.load(fl.read())
        except FileNotFoundError:
            content = {}
            log('Visted repos file not found. The file will be created.',WARNING)

        # Verify if repository in visited_repos.yml
        if response.url in content:
            log(response.url+' has already been visited',WARNING)
            if not REVISIT:
                return 0

        # Verifiy if the url is a github repository url by searching for the button "Clone or Download"
        if not response.xpath('//summary[contains(@class,"btn btn-sm btn-primary")]'):
            # Quit this url if it doesn't have the clone button 
            log(response.url+' is not a github repository',state=WARNING)
            return None

        log(response.url+' is a github repository',state=VALIDE)

        # Explore the repository
        downloaded = self.explore_directory(url=response.url)

        # Add repository to visited_repos.yml
        content[response.url] = downloaded
        with open(os.path.join(BASE_SAVING_DIRECTORY,r'visited_repos.yml'),'w') as fl:
            fl.write(yaml.dump(content,default_flow_style=False))





    def explore_directory(self,url):
        """
            Given a github repos directory url, this function will explores it recursively.

            @params: url
            @returns: downloaded
        """


        # Create the directory where python files will be stored (recreate the exact hirarchy of the project)
        path = self.from_gitpath_to_localpath(url)
        if not os.path.isdir(path):
            os.makedirs(path)
        log('Creating directory: '+str(path),VALIDE)

        # Get all items listed in the directory
        req = self.get_request(url)
        downloaded = 0

        if req:

            soup = BeautifulSoup(req.content,'html.parser')
            for item in soup.findAll(class_="js-navigation-open"):

                try:
                    href = item['href']
                except:
                    href = None

                if href:

                    if '/blob' in href.lower():
                        downloaded += self.download_file('https://github.com'+href)
                        log('File at '+href,state=VALIDE)
                    elif '/tree' in href.lower():
                        downloaded += self.explore_directory('https://github.com'+href)
                        log('Directory at '+href,state=VALIDE)
                    else:
                        log('Unknown object at '+href,state=ERROR)

        return downloaded


    def download_file(self,url):
        """
            Given a github repos file url, this function will verify if this file is accepted
            then downloads it if True (or not if the filehas already been downloaded and the 
            REWRITE option is not activated)

            @params: url
            @returns: bytes_written
        """

        # Download the file or not ? 
        if not IS_ACCEPTED_FILE(url):
            return 0

        # Create the path where to store the downloaded file
        path = self.from_gitpath_to_localpath(url)
        if os.path.isfile(path):
            log('file already downloaded !',state=WARNING)
            if not REWRITE:
                return 0

        raw_url = url.replace('github','raw.githubusercontent').replace('/blob','')
        req = self.get_request(raw_url)
        soup = BeautifulSoup(req.content,'html.parser')
        bytes_written = 0
        with open(path,'w') as pyfile:
            log('Downloading file {} into {}'.format(url,path),VALIDE)
            bytes_written += pyfile.write(soup.getText())

        return bytes_written





    def get_request(self,url):
        """
            Send a get request to a given url while avoiding making the same requests
            and simulating a human beheviour by introducing random waiting time between
            requests.
            In case of a 429 'RATE LIMIT' response code, waits 10 seconds then repeats
            the request until it passes.
            In case of other non 2xx response codes, repeats the request at most 3 times
            then returns None if it didn't succeed.

            @params: url
            @returns: response
        """

        global LAST_REQUEST_TIMER,HUMAN_BEHAVIOUR_SIMULATION
        global MEAN_REQUESTS__TIME_WAIT,VAR_REQUESTS__TIME_WAIT,MIN_REQUESTS__TIME_WAIT

        if HUMAN_BEHAVIOUR_SIMULATION:
            time_before_next_request = min(
                random.normalvariate(MEAN_REQUESTS__TIME_WAIT,VAR_REQUESTS__TIME_WAIT)
                ,MIN_REQUESTS__TIME_WAIT
            )
            time.sleep(max(LAST_REQUEST_TIMER+time_before_next_request-time.time(),0))


        req = None
        done = False

        waiting_time_429_error = 10
        waiting_time_std_error = 0.5
        waiting_time_error = 0

        error_limit = 3
        errors = 0

        if url in self.current_repos_explored_urls:
            return req

        self.current_repos_explored_urls.append(url)

        while not done and errors < error_limit:

            waiting_time_error = waiting_time_std_error

            try:

                req = requests.get(url)
                LAST_REQUEST_TIMER = time.time()

                if req.status_code//100 == 2:
                    return req
                elif req.status_code == 429:
                    waiting_time_error = waiting_time_429_error
                    errors -= 1
                    raise Exception('Status Code 429')
                else:
                    raise Exception('Status Code '+str(req.status_code))

            except Exception as exc:
                log('Exception at requests: '+str(exc),ERROR)

            log('Waiting '+str(waiting_time_error)+'s',WARNING)
            time.sleep(waiting_time_error)        
            errors += 1

        return req





    def from_gitpath_to_localpath(self,url):
        """

            Transforms a github url into a local path.
            @params:
                url: the github url
            @returns:
                path: a valid local path
            @example:
                
                in: https://github.com/AttilaDSA/IntilaqDSAcademy/tree/master/Tests
                out: /AttilaDSA/IntilaqDSAcademy/master/Tests 

                in: https://github.com/AttilaDSA/IntilaqDSAcademy/blob/master/Tests
                out: /AttilaDSA/IntilaqDSAcademy/master/Tests 

        """
        path = unquoting_function(url.split('github.com/')[1])

        if '/blob' in path:
            path = Path(path.replace('/blob',''))
        elif '/tree' in path:
            path = Path(path.replace('/tree',''))

        return os.path.join(BASE_SAVING_DIRECTORY,path)
