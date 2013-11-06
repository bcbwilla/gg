""" Datastore model objects
"""

import json
from datetime import datetime

from google.appengine.ext import ndb

class Map(ndb.Model):
    """ Represents a map """

    name = ndb.StringProperty()
    servers = ndb.StringProperty(repeated=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)
    n_matches = ndb.IntegerProperty()
    gamemode = ndb.StringProperty()
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

class Server(ndb.Model):
    """ Represents a server """
    
    name = ndb.StringProperty()    
    updated_date = ndb.DateTimeProperty(auto_now=True)
    maps = ndb.StringProperty(repeated=True)
    n_maps = ndb.ComputedProperty(lambda self: len(self.maps))

    avg_length = ndb.FloatProperty()
    med_length = ndb.FloatProperty()
    std_length = ndb.FloatProperty()

    avg_rotation_length = ndb.FloatProperty()

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


class MapMaker(ndb.Model):
    """ Represents a map maker """

    name = ndb.StringProperty()
    maps = ndb.StringProperty(repeated=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)
    n_maps = ndb.ComputedProperty(lambda self: len(self.maps))

    avg_length = ndb.FloatProperty()
    med_length = ndb.FloatProperty()
    std_length = ndb.FloatProperty()

    avg_kills = ndb.FloatProperty()
    med_kills = ndb.FloatProperty()
    std_kills = ndb.FloatProperty()

    avg_deaths = ndb.FloatProperty()
    med_deaths = ndb.FloatProperty()
    std_deaths = ndb.FloatProperty()

    avg_participants = ndb.FloatProperty()
    med_participants = ndb.FloatProperty()
    std_participants = ndb.FloatProperty()
    
