""" Cron jobs that are run as specified in cron.yaml
"""

import numpy as np
import webapp2

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch, urlfetch_errors

import scraper
from models.models import Match, Map, Server, OCN, MapMaker

class GetMatchesHandler(webapp2.RequestHandler):
    """ Gets matches from oc.tc/matches and store in ndb """

    def get(self):
        print "getting matches"
        scraper.scrape_matches(150)



class UpdateMapStatsHandler(webapp2.RequestHandler):
    """ Updates map stats from matches """

    def get(self):
        print "updating stats"
        maps = Map.query()
        
        maps = list(maps)

        # get total number of map instances on servers
        total_maps = 0
        for m in maps:
            total_maps += len(m.servers)
        
        for m in maps:
            lengths = []
            kills = []
            deaths = []
            participants = []
            servers = []
            is_on_EU = False
            is_on_US = False

            map_name = m.name
            matches = Match.query(Match.map_name == map_name)
    
            matches = list(matches)            
           
            for match in matches:
                lengths.append(match.length)
                kills.append(match.kills)
                deaths.append(match.deaths)
                participants.append(match.participants)

                is_on_EU = "(EU)" in match.server
                is_on_US = "(US)" in match.server

                if not match.server in servers:
                    servers.append(match.server)
     
            lengths = np.array(lengths)
            kills = np.array(kills)
            deaths = np.array(deaths)
            participants = np.array(participants)

            n_matches = len(matches)
            m.n_matches = n_matches

            if n_matches > 1:
                m.avg_length = np.mean(lengths)
                m.med_length = np.median(lengths)
                m.std_length = np.std(lengths)
                m.min_length = np.amin(lengths)
                m.max_length = np.amax(lengths)

                m.avg_kills = np.mean(kills)
                m.med_kills = np.median(kills)
                m.std_kills = np.std(kills)
                m.min_kills = np.amin(kills)
                m.max_kills = np.amax(kills)
                
                m.avg_deaths = np.mean(deaths)
                m.med_deaths = np.median(deaths)
                m.std_deaths = np.std(deaths)
                m.min_deaths = np.amin(deaths)
                m.max_deaths = np.amax(deaths)
                    
                m.avg_participants = np.mean(participants)
                m.med_participants = np.median(participants)
                m.std_participants = np.std(participants)
                m.min_participants = np.amin(participants)
                m.max_participants = np.amax(participants)
            
            m.is_on_EU = is_on_EU
            m.is_on_US = is_on_US
            m.servers = servers

            if total_maps != 0:
                m.percent_maps = len(servers) / float(total_maps)

            if not m.authors:
                d = self.get_map_xml_data(m)
                m.authors = d['authors']
                m.objective = d['objective']
                m.team_size = d['team_size']

            if m.authors:
                for map_maker in m.authors:
                    mm = MapMaker.get_or_insert(map_maker.lower())
                    mm.maps.append(m.name)
                    mm.name = map_maker
                    mm.put()
                    
            m.put()


    def get_map_xml_data(self, mapp):
        """ Get more map information from map XML page """

        BASE_URL = "https://maps.oc.tc/"
        URL_SUFFIX = "/map.xml"

        page_get = True

        # check if Ghost Squadron map
        if mapp.name[:3].lower() == "gs:":
            url = BASE_URL + "/GS/" + mapp.name[4:] + URL_SUFFIX
        else:
            url = BASE_URL + mapp.name + URL_SUFFIX    
        
        try:
            page = urlfetch.fetch(url,validate_certificate=False,
                                    headers = {'User-Agent': 'Mozilla/5.0'})
        except Exception:    
            print "url error for map " + mapp.name       
            page_get = False    

        if page_get and page.status_code == 200:
            xml = page.content
            soup =  BeautifulSoup(xml)

            objective = soup.find("objective").contents[0]

            authors = []
            for author in soup.find_all("author"):
                authors.append(author.contents[0])

            authors = authors

            team_size = int(soup.find_all("team")[0]['max'])

        else:
            objective = None
            authors = []
            team_size = None

        return {'objective':objective,'authors':authors,'team_size':team_size}


class UpdateServerStatsHandler(webapp2.RequestHandler):
    """ Updates server stats from maps """

    def get(self):
        print "updating servers"

        servers = Server.query()
        servers = list(servers)

        maps = Map.query()
        maps = list(maps)

        for s in servers:
            lengths = []
            kills = []
            deaths = []
            participants = []
            servers = []

            for m in maps:
                if s.name in m.servers:
                    if not m.name in s.maps:
                        s.maps.append(m.name)
                
                    if m.avg_length != None:
                        lengths.append(m.avg_length)
                        kills.append(m.avg_kills)
                        deaths.append(m.avg_deaths)
                        participants.append(m.avg_participants)

            lengths = np.array(lengths)
            kills = np.array(kills)
            deaths = np.array(deaths)
            participants = np.array(participants)


            if len(lengths) > 1:
                s.avg_length = np.mean(lengths)
                s.med_length = np.median(lengths)
                s.std_length = np.std(lengths)

                s.avg_kills = np.mean(kills)
                s.med_kills = np.median(kills)
                s.std_kills = np.std(kills)
                
                s.avg_deaths = np.mean(deaths)
                s.med_deaths = np.median(deaths)
                s.std_deaths = np.std(deaths)
                    
                s.avg_participants = np.mean(participants)
                s.med_participants = np.median(participants)
                s.std_participants = np.std(participants)

            # calculate average rotation length
            avg_rotation_length = 0
            for map_name in s.maps:
                m = Map.get_by_id(map_name.lower())
                
                if m.avg_length != None:
                    avg_rotation_length += m.avg_length

            s.avg_rotation_length = avg_rotation_length
            
            s.put()
        

class UpdateMapMakersHandler(webapp2.RequestHandler):
    """ Updates map maker stats """

    def get(self):
        print "updating map maker"

        map_makers = MapMaker.query()
        map_makers = list(map_makers)

        maps = Map.query()
        maps = list(maps)

        for mm in map_makers:
            lengths = []
            kills = []
            deaths = []
            participants = []
            servers = []
            maps = []

            for mapp in maps:
                if mm.name in mapp.authors:
                    if not mapp.name in mm.maps:
                        mm.maps.append(mapp.name)
                
                    if mapp.avg_length != None:
                        lengths.append(mapp.avg_length)
                        kills.append(mapp.avg_kills)
                        deaths.append(mapp.avg_deaths)
                        participants.append(mapp.avg_participants)

            lengths = np.array(lengths)
            kills = np.array(kills)
            deaths = np.array(deaths)
            participants = np.array(participants)


            if len(lengths) > 1:
                mm.avg_length = np.mean(lengths)
                mm.med_length = np.median(lengths)
                mm.std_length = np.std(lengths)

                mm.avg_kills = np.mean(kills)
                mm.med_kills = np.median(kills)
                mm.std_kills = np.std(kills)
                
                mm.avg_deaths = np.mean(deaths)
                mm.med_deaths = np.median(deaths)
                mm.std_deaths = np.std(deaths)
                    
                mm.avg_participants = np.mean(participants)
                mm.med_participants = np.median(participants)
                mm.std_participants = np.std(participants)
            
            mm.put()


class UpdateOCNStatsHandler(webapp2.RequestHandler):
    """ Updates OCN stats from servers """

    def get(self):
        # TODO
        pass

class UpdateGameModeHandler(webapp2.RequestHandler):
    """ Updates OCN stats from servers """

    def get(self):
        # TODO
        pass
            
