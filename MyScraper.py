import urllib.request, urllib.parse, urllib.error
import re
from selenium import webdriver
import random
import time

'''spider requires the argument 'page', which is the url of a kickstarter discover page, then look for inner url links to
individual projects, and return a list of url to the projects' comment section'''
class mycrawl:

    def __init__(self):
        self.page_number = 1

    def rand_header(self, headless_url):
        user_agent_list = [
           #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            #Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        for i in range(1,6):
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            request = urllib.request.Request(headless_url,headers={'User-Agent': user_agent})
            return request


    def pager(self):

        ''' kickstarter page template
        https://www.kickstarter.com/discover/advanced?category_id=16&woe_id=Earth&sort=magic&seed=2578776&page=1
        and the 'page=1' increments and seems to be there are only 200 pages at the moment
        '''

        url_template = 'https://www.kickstarter.com/discover/advanced?category_id=16&woe_id=Earth&sort=magic&seed=2578776&page='
        flag = False

        try:
            next_page = url_template + str(self.page_number)
            if urllib.request.urlopen(self.rand_header(next_page)): flag = True
        except:
            print("Reached the end of the results!")


        if flag:
            print("Page " + str(self.page_number) + "\'s links have been collected.")
            self.page_number += 1
            return next_page
        else: return False
        '''
        a list of all the urls in the kickstarter discovery screen of technology category made
        '''


    def spider(self, page):
        '''
        driver = webdriver.Safari()
        driver.get(page)
        data = driver.page_source
        tmp = re.findall(r'\"rewards\"\:\"https\:\/\/www\.kickstarter\.com\/projects\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+', data)
        '''
        if not page:
            print('No More Kickstarter Pages!')
            return False

        data = urllib.request.urlopen(self.rand_header(page)).read().decode()
        tmp = re.findall(r'\"rewards\"\:\"https\:\/\/www\.kickstarter\.com\/projects\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+', data)

        project_urls = list()
        for url in tmp:
            print(url + ' comment page has been recorded!')
            project_urls.append(url[11:]+'/comments')
        return project_urls

        '''
        Link Template "rewards":"https://www.kickstarter.com/projects/primotoys/pigzbe/rewards"
        Return a list of urls in the form of '"rewards":"https://www.kickstarter.com/projects/company_name/project_name' (str)
        '''

    def scrape(self, project_urls, webdriver):

        if not project_urls:
            print('No More Comment Pages.')
            return False

        load_more_xpath = '//*[@id="react-project-comments"]/div/button'
        f = open('email_harvest.txt', 'a+')

        driver = webdriver

        for url in project_urls:

            driver.get(url)

            while True:
                driver.implicitly_wait(10)

                try:
                    driver.find_element_by_xpath(load_more_xpath).click()
                    time.sleep(random.choice([second for second in range(10,25)]))
                except: break

            page_source = driver.page_source
            emails = re.findall(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', page_source)
            for email in emails:
                f.write(email + '\n')

        f.close()

        '''
        Scrape requires a list of the urls of Kickstarter comment sections
        using selenium, it is able to unravel as many comments as the comment page hasself.
        Automatically, it writes all the emails harvested in the link in the local file, email_harvest.txt
        '''

#proxy example
'''
 myProxy = "http://149.215.113.110:70"

        proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy':''})

        self.driver = webdriver.Firefox(proxy=proxy)
'''

hyuck_crawl = mycrawl()
kickstarter_url_list = list()

random_box = range(2, 10)
random_box1 = range(5, 25)


while True:
    tmp = hyuck_crawl.pager()
    if tmp:
        kickstarter_url_list.append(tmp)
        print(tmp + ' page has been parsed!')
        time.sleep(random.choice(random_box))
    else: break

driver = webdriver.Safari()

for url in kickstarter_url_list:
    time.sleep(random.choice(random_box))
    kickstarter_comment_page_links = hyuck_crawl.spider(url)
    time.sleep(random.choice(random_box1))
    hyuck_crawl.scrape(kickstarter_comment_page_links, driver)

driver.close()

'''
URL header changer, in case I need it.
import random
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
for i in range(1,6):
    #Pick a random user agent
    user_agent = random.choice(user_agent_list)
    #Set the headers
    headers = {'User-Agent': user_agent}
    #Make the request
    request = urllib.request.Request(url,headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(request)
    html = response.read()
'''
