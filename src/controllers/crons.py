""" Cron jobs that are run as specified in cron.yaml
"""

import webapp2
import logging
import numpy as np

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch, urlfetch_errors

import scraper
from models.models import Match, Map, Server, OCN, MapMaker, ColumnChart

class GetMatchesHandler(webapp2.RequestHandler):
    """ Gets matches from oc.tc/matches and store in ndb """

    def get(self):
        logging.info("Getting matches")
        scraper.scrape_matches(20)
        logging.info("Matches gotten")



class UpdateMapStatsHandler(webapp2.RequestHandler):
    """ Updates map stats from matches """

    def get(self):
        logging.info('Updating map stats.')

        maps = Map.query().fetch()

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

            map_name = m.key.id()
            m.name = map_name
            # compute stats from only 50 most recent matches.
            matches = Match.query(Match.map_name == map_name).order(-Match.date).fetch(100)
           
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
                m = m.get_map_xml_data()

            if m.authors:
                for map_maker in m.authors:
                    mm = MapMaker.get_or_insert(map_maker)
                    mm.name = map_maker
                    if m.name not in mm.maps:
                        mm.maps.append(m.name)
                    
                    mm.put()
                    
            m.put()

        logging.info('Map stats updated.')



class UpdateServerStatsHandler(webapp2.RequestHandler):
    """ Updates server stats from maps """

    def get(self):
        logging.info("Updating server stats")

        servers = Server.query().fetch()

        maps = Map.query().fetch()

        for s in servers:
            lengths = []
            kills = []
            deaths = []
            participants = []
            servers = []

            s.name = s.key.id()

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
                m = Map.get_by_id(map_name)
                
                if m.avg_length != None:
                    avg_rotation_length += m.avg_length

            s.avg_rotation_length = avg_rotation_length
            
            s.put()

        logging.info("Server stats updated.")

class UpdateMapMakersHandler(webapp2.RequestHandler):
    """ Updates map maker stats """

    def get(self):
        logging.info("Updating map makers")

        map_makers = MapMaker.query().fetch()

        maps = Map.query().fetch()

        logging.info(len(maps))
        for m in maps:
            logging.info(m.authors)

        for mm in map_makers:
            lengths = []
            kills = []
            deaths = []
            participants = []
            servers = []

            mm.name = mm.key.id()

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


            if len(lengths) >= 1:
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

        logging.info("Map makers updated")

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
            

class UpdateChartsHandler(webapp2.RequestHandler):
    """ Updates map stats from matches """

    def get(self):
        logging.info('Updating charts.')

        # time based stats
        longest_chart = ColumnChart().get_or_insert("longest_avg_length")       
        longest_maps = Map.top("avg_length", ascending=False, limit=30, projections=["gamemode"])
        
        longest_chart.name = "Longest"
        longest_chart.x = [str(m.name) for m in longest_maps if m.gamemode != "TDM"][:10]
        longest_chart.y = [round(m.avg_length / 60.0, 3) for m in longest_maps if m.gamemode != "TDM"][:10]
        longest_chart.put()


        shortest_chart = ColumnChart().get_or_insert("shortest_avg_length")       
        shortest_maps = Map.top("avg_length", ascending=True, limit=10)
        
        shortest_chart.name = "Shortest"
        shortest_chart.x = [str(m.name) for m in shortest_maps]
        shortest_chart.y = [round(m.avg_length, 3) for m in shortest_maps]
        shortest_chart.put()
        

        # most deadly maps
        deadliest_chart = ColumnChart().get_or_insert("deadliest")             
        deadliest_maps = Map.top("kill_density", ascending=False, limit=10)

        deadliest_chart.name = "Deadliest"
        deadliest_chart.x = [str(m.name) for m in deadliest_maps]
        deadliest_chart.y = [round(m.kill_density*60, 3) for m in deadliest_maps]
        deadliest_chart.x_header = "Map"
        deadliest_chart.y_header = "Kills per Player per Minute"
        deadliest_chart.put()

        peaceful_chart = ColumnChart().get_or_insert("peaceful") 
        peaceful_maps = Map.top("kill_density", ascending=True, limit=10)

        peaceful_chart.name = "Most Peaceful"
        peaceful_chart.x = [str(m.name) for m in peaceful_maps]
        peaceful_chart.y = [round(m.kill_density*60, 3) for m in peaceful_maps]
        peaceful_chart.x_header = "Map"
        peaceful_chart.y_header = "Kills per Player per Minute"
        peaceful_chart.put()

        logging.info("Charts updated")
        

        
