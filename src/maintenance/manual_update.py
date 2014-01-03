import webapp2
import logging
from models.models import Match, Map, Server, OCN, MapMaker


class ManualUpdateHandler(webapp2.RequestHandler):

    def get(self):
        logging.info("Beginning manual update")

        # put entites to update manually here.

        self.update_entity(Map, "Cairo Blitz", objective="Eliminate the other team before 10 minutes is up", authors=["koipen"])

        #

        logging.info("Manual update complete")
        logging.info("Updating mapmakers")
        self.update_mapmakers()
        logging.info("Mapmakers updated")
        self.redirect("/")

    def update_entity(self, cls, name, **kwargs):
        """ Updates all attributes in kwargs for entity
            named 'name' of type 'cls'.
        """

        entity = cls.query(cls.name == name).get()
        logging.info('Updating ' + name)
        
        if entity:
            for attr, value in kwargs.iteritems():
                if hasattr(entity, attr):
                    setattr(entity, attr, value)

            entity.put()


    def update_mapmakers(self):
        """ Mapmakers who are added to maps manually aren't added to the datastore.
            This function fixes that.
        """

        for m in Map.query().fetch():
            if m.authors:
                for map_maker in m.authors:
                    mm = MapMaker.get_or_insert(map_maker)
                    mm.name = map_maker
                    if m.name not in mm.maps:
                        mm.maps.append(m.name)
                    
                    mm.put()

