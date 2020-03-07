

import requests
from bs4 import BeautifulSoup
import re
from database_manager import DatabaseManager
import time

class WebsiteScrapper:

  # Dummy Header
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  rbhe_url = "http://periodicos.uem.br/ojs/index.php/rbhe/issue/archive"

  def scrapRbhe(self):
    print("Starting to scrap RBHE")

    databaseManager = DatabaseManager()

    # Get Main Page
    main_page = requests.get(self.rbhe_url, headers=self.headers)
    if(main_page.status_code == 200):
      
      print("Connection to main site was ok")
      
      # Parse main page
      main_soup = BeautifulSoup(main_page.content, 'html.parser')

      # Get all issues
      list_of_issues = main_soup.findAll("ul", {"class": "issues_archive"})

      print("Found " + str(len(list_of_issues)) + " issues")

      for issue in list_of_issues:

        # Get issue url
        issue_url = issue.find("a", {"class": "title"})['href']

        # Get the issue page
        issue_page = requests.get(issue_url, headers = self.headers)

        if(issue_page.status_code == 200):

          # Parse issue page
          issue_soup = BeautifulSoup(issue_page.content, 'html.parser')

          # Get all articles
          list_of_articles =  issue_soup.findAll("ul", {"class": "cmp_article_list articles"})[0].findAll("a")
          
          for article in list_of_articles:

            article_url = article["href"]

            # Get article page
            article_page = requests.get(article_url, headers = self.headers)

            if(article_page.status_code == 200):

              article_soup = BeautifulSoup(article_page.content, 'html.parser')

              # Article Title
              title = article_soup.find("h1", {"class": "page_title"}).text.strip()
              
              print("Getting article: " + title)

              # Authors
              list_of_authors = article_soup.findAll("span", {"class": "name"})
              all_authors = []
              for author in list_of_authors:
                all_authors.append(author.text.strip())

              # Summary
              summary = article_soup.find("p").text

              # Key words
              temp_string = article_soup.find("div", {"class": "item keywords"}).find("span",{"class": "value"}).text.strip().split(",")
              key_words = []
              for w in temp_string:
                w = re.sub('\s+', '', w)
                key_words.append(w)
                
              databaseManager.addToRbheFile(title, all_authors, summary, key_words)

              time.sleep(1)
            else:
              print("Wasn't able to access " + str(article_url) )
        else:
          print("Wasn't able to access the issue page " + str(issue_url) )
    else:
      print("Coudn't connect to the main website")
      print("Status code: " + str(page.status_code))
      
    
