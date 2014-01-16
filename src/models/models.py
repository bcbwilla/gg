""" Datastore model objects
"""

import json
from datetime import datetime, timedelta
import logging

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch, urlfetch_errors
from google.appengine.ext import ndb

class GGModelBase(object):
    """ Base class for all datastore models """

    @classmethod
    def names(cls):
        """ Returns a list of all of the names
            of entity instances.  For use with
            typeahead.js searchbox.
    
            Using class must have attribute "name" defined.
        """
        
        if hasattr(cls, "name"):
            objs = cls().query().fetch(projection=[cls.name])
            names = [obj.name for obj in objs]
            
            return names

        else:
            return []

        
    @classmethod
    def top(cls, attr, ascending=True, limit=5, projections=[]):
        if hasattr(cls, attr):
            logging.info("has attribute " + attr)
            if ascending:
                qry = cls().query(getattr(cls,attr) != None).order(getattr(cls,attr))
            else:
                qry = cls().query(getattr(cls,attr) != None).order(-getattr(cls,attr))
            
            p = projections + [getattr(cls,attr), cls.name]
            objs = qry.fetch(limit, projection=p)
            logging.info(objs)
            return objs

        else:
            return []

    

class Map(ndb.Model,GGModelBase):
    """ Represents a map """

    name = ndb.StringProperty()
    servers = ndb.StringProperty(repeated=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)
    n_matches = ndb.IntegerProperty()
    gamemode = ndb.StringProperty(choices=["CTW","DTC","DTM","Blitz","Rage","GS","TDM","Mixed","Gear","KOTH"])
    authors = ndb.StringProperty(repeated=True)
    objective = ndb.StringProperty()
    team_size = ndb.IntegerProperty()
    
    # Number of times map appears on all servers
    frequency = ndb.ComputedProperty(lambda self: len(self.servers))
    # Percentage of all maps that are map
    percent_maps = ndb.FloatProperty()
    
    is_on_US = ndb.BooleanProperty()
    is_on_EU = ndb.BooleanProperty()
    is_in_rots = ndb.BooleanProperty()

    avg_length = ndb.FloatProperty()
    med_length = ndb.FloatProperty()
    std_length = ndb.FloatProperty()
    min_length = ndb.IntegerProperty()
    max_length = ndb.IntegerProperty()

    # times in hh:mm:ss string format for displaying on pages    
    avg_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.avg_length))) if self.avg_length != None else None)

    med_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.med_length))) if self.med_length != None else None)

    std_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.std_length))) if self.std_length != None else None)

    min_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.min_length))) if self.min_length != None else None)

    max_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.max_length))) if self.max_length != None else None)

    avg_kills = ndb.FloatProperty()
    med_kills = ndb.FloatProperty()
    std_kills = ndb.FloatProperty()
    min_kills = ndb.IntegerProperty()
    max_kills = ndb.IntegerProperty()

    avg_deaths = ndb.FloatProperty()
    med_deaths = ndb.FloatProperty()
    std_deaths = ndb.FloatProperty()
    min_deaths = ndb.IntegerProperty()
    max_deaths = ndb.IntegerProperty()

    avg_participants = ndb.FloatProperty()
    med_participants = ndb.FloatProperty()
    std_participants = ndb.FloatProperty()
    min_participants = ndb.IntegerProperty()
    max_participants = ndb.IntegerProperty()

    kill_density = ndb.ComputedProperty(lambda self: (self.avg_kills / self.avg_participants) / self.avg_length 
                                        if self.avg_kills != None and self.avg_length != None and self.avg_participants != None else None)

    def get_map_xml_data(self, url=None):
        """ Get more map information from map XML page 
            
            Keyword Arguments:
            url -- specifies complete url to map xml page.
        
        """

        m = self

        if not url:
            BASE_URL = "https://maps.oc.tc/"
            URL_SUFFIX = "/map.xml"

            page_get = True
            
            m_name = m.name.replace(" ", "%20") # replace spaces in URL with %20

            # check if Ghost Squadron map
            if m.name[:3].lower() == "gs:":
                url = BASE_URL + "GS/" + m.name[4:] + URL_SUFFIX
            else:
                url = BASE_URL + m_name + URL_SUFFIX   


        try:
            page = urlfetch.fetch(url,validate_certificate=False,
                                  headers = {'User-Agent': 'Mozilla/5.0'})
            
            if page.status_code != 200:
                url = BASE_URL + "KOTH/" + m_name + URL_SUFFIX
                page = urlfetch.fetch(url,validate_certificate=False,
                                      headers = {'User-Agent': 'Mozilla/5.0'})
            xml = page.content
            
        except Exception:
            
            try:
                page = urlfetch.fetch(url,validate_certificate=False,
                                      headers = {'User-Agent': 'Mozilla/5.0'})
                xml = page.content         
            except Exception, (err_msg):
                logging.warning("Can't find xml for " + m.name + ': ' + str(err_msg))
                return m
      
        soup =  BeautifulSoup(xml) 

        try:
            m.objective = soup.find("objective").contents[0]

            m.authors = []
            authors = []
            for author in soup.find_all("author"):
                if not author.contents[0] in m.authors:
                    m.authors.append(author.contents[0])

            m.team_size = int(soup.find_all("team")[0]['max'])

        except Exception, (err_msg):
            m.objective = None
            m.authors = []
            m.team_size = None
            logging.warning('XML scraping exception for ' + m.name + ': ' + str(err_msg))

        return m

    def to_json(self):
        """ Constructs json rep. of map.
            There MUST be a better way to do this.
            I tried, but I suck.  json does not
            like if I try to use __dict__ method.
            # TODO
        """

        d = {}    
        d['name'] = self.name
        d['servers'] = self.servers
        d['updated_date'] = self.updated_date.isoformat()
        d['n_matches'] = self.n_matches
        d['gamemode'] = self.gamemode

        d['frequency'] = self.frequency
        d['percent_maps'] = self.percent_maps
        
        d['is_on_US'] = self.is_on_US
        d['is_on_EU'] = self.is_on_EU
        d['is_in_rots'] = self.is_in_rots

        d['avg_length'] = self.avg_length
        d['med_length'] = self.med_length
        d['std_length'] = self.std_length
        d['min_length'] = self.min_length
        d['max_length'] = self.max_length

        d['avg_kills'] = self.avg_kills
        d['med_kills'] = self.med_kills
        d['std_kills'] = self.std_kills
        d['min_kills'] = self.min_kills
        d['max_kills'] = self.max_kills

        d['avg_deaths'] = self.avg_deaths
        d['med_deaths'] = self.med_deaths
        d['std_deaths'] = self.std_deaths
        d['min_deaths'] = self.min_deaths
        d['max_deaths'] = self.max_deaths

        d['avg_participants'] = self.avg_participants
        d['med_participants'] = self.med_participants
        d['std_participants'] = self.std_participants
        d['min_participants'] = self.min_participants
        d['max_participants'] = self.max_participants
        
        return json.dumps(d)

class Match(ndb.Model):
    """ Represents a match """

    date = ndb.DateTimeProperty(auto_now_add=True)
    map_name = ndb.StringProperty()
    server = ndb.StringProperty()
    deaths = ndb.IntegerProperty()
    kills = ndb.IntegerProperty()
    participants = ndb.IntegerProperty()
    length = ndb.IntegerProperty() # In seconds
    # When match took place relative to date, in minutes ago
    when = ndb.IntegerProperty() 


class OCN(ndb.Model):
    """ Represents the whole network """

    updated_date = ndb.DateTimeProperty(auto_now=True)
    servers = ndb.StringProperty(repeated=True)
    n_servers = ndb.ComputedProperty(lambda self: len(self.servers))
    deaths = ndb.IntegerProperty()
    kills = ndb.IntegerProperty()
    participants = ndb.IntegerProperty()
    time_played = ndb.IntegerProperty() # in seconds

class Server(ndb.Model,GGModelBase):
    """ Represents a server """
    
    name = ndb.StringProperty()    
    updated_date = ndb.DateTimeProperty(auto_now=True)
    maps = ndb.StringProperty(repeated=True)
    n_maps = ndb.ComputedProperty(lambda self: len(self.maps))

    avg_length = ndb.FloatProperty()
    med_length = ndb.FloatProperty()
    std_length = ndb.FloatProperty()

    # times in hh:mm:ss string format for displaying on pages    
    avg_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.avg_length))) if self.avg_length != None else None)

    med_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.med_length))) if self.med_length != None else None)

    std_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.std_length))) if self.std_length != None else None)

    avg_rotation_length = ndb.FloatProperty()

    avg_rotation_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.avg_rotation_length))) if self.avg_rotation_length != None else None)

    avg_kills = ndb.FloatProperty()
    med_kills = ndb.FloatProperty()
    std_kills = ndb.FloatProperty()

    avg_deaths = ndb.FloatProperty()
    med_deaths = ndb.FloatProperty()
    std_deaths = ndb.FloatProperty()

    avg_participants = ndb.FloatProperty()
    med_participants = ndb.FloatProperty()
    std_participants = ndb.FloatProperty()
    
    def to_json(self):
        """ Constructs json rep. of map.
            There MUST be a better way to do this.
            I tried, but I suck.  json does not
            like if I try to use __dict__ method.
            # TODO
        """

        d = {}    
        d['name'] = self.name
        d['updated_date'] = self.updated_date.isoformat()
        d['maps'] = self.maps
        d['n_maps'] = self.n_maps

        d['avg_rotation_length'] = self.avg_rotation_length

        d['avg_length'] = self.avg_length
        d['med_length'] = self.med_length
        d['std_length'] = self.std_length

        d['avg_kills'] = self.avg_kills
        d['med_kills'] = self.med_kills
        d['std_kills'] = self.std_kills

        d['avg_deaths'] = self.avg_deaths
        d['med_deaths'] = self.med_deaths
        d['std_deaths'] = self.std_deaths

        d['avg_participants'] = self.avg_participants
        d['med_participants'] = self.med_participants
        d['std_participants'] = self.std_participants

        return json.dumps(d)


class GameMode(ndb.Model):
    """ Represents a game mode """
    
    name = ndb.StringProperty()    
    updated_date = ndb.DateTimeProperty(auto_now=True)
    maps = ndb.StringProperty(repeated=True)
    n_maps = ndb.ComputedProperty(lambda self: len(self.maps))
    servers = ndb.StringProperty(repeated=True)
    n_servers = ndb.ComputedProperty(lambda self: len(self.servers))

    avg_length = ndb.FloatProperty()
    med_length = ndb.FloatProperty()
    std_length = ndb.FloatProperty()
    min_length = ndb.IntegerProperty()
    max_length = ndb.IntegerProperty()

    # times in hh:mm:ss string format for displaying on pages    
    avg_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.avg_length))) if self.avg_length != None else None)

    med_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.med_length))) if self.med_length != None else None)

    std_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.std_length))) if self.std_length != None else None)

    min_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.min_length))) if self.min_length != None else None)

    max_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.max_length))) if self.max_length != None else None)


    avg_kills = ndb.FloatProperty()
    med_kills = ndb.FloatProperty()
    std_kills = ndb.FloatProperty()
    min_kills = ndb.IntegerProperty()
    max_kills = ndb.IntegerProperty()

    avg_deaths = ndb.FloatProperty()
    med_deaths = ndb.FloatProperty()
    std_deaths = ndb.FloatProperty()
    min_deaths = ndb.IntegerProperty()
    max_deaths = ndb.IntegerProperty()

    avg_participants = ndb.FloatProperty()
    med_participants = ndb.FloatProperty()
    std_participants = ndb.FloatProperty()
    min_participants = ndb.IntegerProperty()
    max_participants = ndb.IntegerProperty()


class MapMaker(ndb.Model,GGModelBase):
    """ Represents a map maker """

    name = ndb.StringProperty()
    maps = ndb.StringProperty(repeated=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)
    n_maps = ndb.ComputedProperty(lambda self: len(self.maps))

    avg_length = ndb.FloatProperty()
    med_length = ndb.FloatProperty()
    std_length = ndb.FloatProperty()

    # times in hh:mm:ss string format for displaying on pages    
    avg_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.avg_length))) if self.avg_length != None else None)

    med_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.med_length))) if self.med_length != None else None)

    std_length_s = ndb.ComputedProperty(lambda self: 
                                        str(timedelta(seconds=int(self.std_length))) if self.std_length != None else None)

    avg_kills = ndb.FloatProperty()
    med_kills = ndb.FloatProperty()
    std_kills = ndb.FloatProperty()

    avg_deaths = ndb.FloatProperty()
    med_deaths = ndb.FloatProperty()
    std_deaths = ndb.FloatProperty()

    avg_participants = ndb.FloatProperty()
    med_participants = ndb.FloatProperty()
    std_participants = ndb.FloatProperty()
    

class Chart(ndb.Model):
    """ Represents a basic chart """

    name = ndb.StringProperty()

class ColumnChart(Chart):
    """ Represents a colum chart """
    
    x = ndb.StringProperty(repeated=True)
    y = ndb.FloatProperty(repeated=True)
    x_header = ndb.StringProperty(default='Map')
    y_header = ndb.StringProperty(default='')

    def get_data_array(self):
        """ prepares data for use in google chart 
            returns 2d array of [x,y] with headers"""
        x_strings = [str(i) for i in self.x]
        return [[str(self.x_header), str(self.y_header)]] + [list(i) for i in zip(x_strings, self.y)]
