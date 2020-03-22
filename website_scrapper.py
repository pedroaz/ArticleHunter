

import requests
from bs4 import BeautifulSoup
import re
from database_manager import DatabaseManager
import time
import os

class WebsiteScrapper:

  # Dummy Header
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  rbhe_url = "http://periodicos.uem.br/ojs/index.php/rbhe/issue/archive"
  databaseManager = DatabaseManager()

  def scrapRbhe(self):

    print("Starting to scrap RBHE")

    os.remove("database/rbhe_file.txt")

    f = open("database/rbhe_file.txt", "w")
    f.close()
    

    # Get Main Page
    main_page = requests.get(self.rbhe_url, headers=self.headers)
    if(main_page.status_code == 200):
      
      print("Connection to main site was ok")
      
      # Parse main page
      main_soup = BeautifulSoup(main_page.content, 'html.parser')

      # Get all issues
      list_of_issues = main_soup.find("ul", {"class": "issues_archive"}).findAll("a", {"class": "title"})

      print("Found " + str(len(list_of_issues)) + " issues")

      for issue in list_of_issues:

        # Get issue url
        issue_url = issue['href']

        # Get the issue page
        issue_page = requests.get(issue_url, headers = self.headers)

        if(issue_page.status_code == 200):

          # Parse issue page
          issue_soup = BeautifulSoup(issue_page.content, 'html.parser')

          # Get all articles
          list_of_articles =  issue_soup.findAll("div", {"class": "title"})

          for article in list_of_articles:
            
            article_url = article.find("a")["href"]
            print("Article url: " + str(article_url))

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
              keywords_div = article_soup.find("div", {"class": "item keywords"})
              key_words = []

              if(keywords_div is not None):
                temp_string = keywords_div.find("span",{"class": "value"}).text.strip().split(",")
                for w in temp_string:
                  w = re.sub('\s+', '', w)
                  key_words.append(w)
                
              self.databaseManager.addToRbheFile(title, all_authors, summary, key_words)

              # time.sleep(1)
            else:
              print("Wasn't able to access " + str(article_url) )
        else:
          print("Wasn't able to access the issue page " + str(issue_url) )
    else:
      print("Coudn't connect to the main website")
      print("Status code: " + str(page.status_code))
      
    
