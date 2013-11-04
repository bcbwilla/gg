#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import webapp2

import scraper
from models.models import Match, Map, Server, OCN

class GetMatchesHandler(webapp2.RequestHandler):
    """ Gets matches from oc.tc/matches and store in ndb """

    def get(self):
        print "getting matches"
        # scraper.scrape_matches(150)
        scraper.scrape_matches(4)



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

            m.put()


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
