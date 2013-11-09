import urllib2
import time
import random
from datetime import timedelta

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch

from models.models import Match, Map, Server


def scrape_matches(pages=2):
    """ gets match statistics from oc.tc/matches pages
    
        last_page - the highest match page to scrape data from. don't go too high!
        out_file - the name of the output data file
        info - if True, it will print stuff every 10 pages to the console as it 
        runs so you know what the script is up to.
        
    
    """
    
    base_url = "https://oc.tc/matches?page="

    first_page = 10 # Lots of matches before page 10 are "in progress"
    last_page = first_page + pages + 1

    for page in range(first_page,last_page):
        url = base_url+str(page)

        page = urlfetch.fetch(url,validate_certificate=False,
                                    headers = {'User-Agent': 'Mozilla/5.0'})
        html = page.content
        soup =  BeautifulSoup(html, "html.parser") 
        table = soup.findAll('table', {'class':'table table-bordered table-striped'})
        table = table[0].contents[3].findAll('tr')
        

        # Short GS matches clog the database.  Only add them sometimes.
        if random.randint(1,10) < 3:
            do_gs = True
        else:
            do_gs = False


        for row in table:
            match = Match()
            when = row.contents[1].a.contents[0].strip().lower() # when match took place
            # make sure match ended, and convert time ago to minutes
            if not 'in progress' in when:

                map_name = row.contents[5].contents[0].strip() 
                match.map_name = map_name

               
                server_name = row.contents[7].a.contents[0].strip()
                if server_name[:2].lower() == "gs" and not do_gs:
                    continue
 
                match.server = server_name

                match.kills = int(row.contents[11].contents[0].strip())
                match.deaths = int(row.contents[9].contents[0].strip())
                match.participants = int(row.contents[13].contents[0].strip())
                
                # convert the total match time to seconds
                t = row.contents[3].contents[0].strip()
                t = t.split(':')
                t = timedelta(minutes=int(t[0]),seconds=int(t[1]))
                match.length = t.seconds
            
                match.put()
                
                # create map object if there isn't already one
                mapp = Map.get_or_insert(map_name.lower())
                mapp.name = map_name
                mapp.put()
                
                # create server object if there isn't already one
                server = Server.get_or_insert(server_name.lower())
                server.name = server_name
                server.put()
                

        time.sleep(0.1)


