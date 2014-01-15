import webapp2
import logging
from models.models import Match, Map, Server, OCN, MapMaker


class ManualUpdateHandler(webapp2.RequestHandler):

    def get(self):
        logging.info("Beginning manual update")

        # put entites to update manually here.
        

        #self.update_entity(Map, "Cairo Blitz", objective="Eliminate the other team before 10 minutes is up", authors=["koipen"])

        #

        maps = [
                ("BipBetaMC" ,"https://maps.oc.tc/BipBetaMC%20TDM/map.xml"),
                ("Cake Wars 3", "https://maps.oc.tc/Blitz/Cake%20Wars%203/map.xml"),
                ("101 Pumpkins", "https://maps.oc.tc/Blitz/101%20Pumpkins/map.xml"),
                ("A Watery Grave", "https://maps.oc.tc/Watery%20Grave/map.xml"),
                ("Arid Crossroads", "https://maps.oc.tc/Blitz/Arid%20Crossroads/map.xml"),
                ("BalloonsDTM: Halloween", "https://maps.oc.tc/Halloween/BalloonsDTM%20Halloween/map.xml"),
                ("Bessemer's Process", "https://maps.oc.tc/Bessemer/map.xml"),
                ("Bliss", "https://maps.oc.tc/Blitz/Bliss/map.xml"),
                ("Blitzkrieg", "https://maps.oc.tc/Blitz/Blitzkrieg/map.xml"),
                ("Cairo Blitz", "https://maps.oc.tc/Blitz/Cairo%20Blitz/map.xml"),
                ("CotBot", "https://maps.oc.tc/Blitz/CotBot/map.xml"),
                ("Dead Heat", "https://maps.oc.tc/Blitz/Dead%20Heat/map.xml"),
                ("Dry Wound", "https://maps.oc.tc/Blitz/Dry%20Wound/map.xml"),
                ("Fairy Tales 2: A Tale or Two", "https://maps.oc.tc/Fairy%20Tales%202/map.xml"),
                ("Fallen Courtyard", "https://maps.oc.tc/Blitz/Fallen%20Courtyard/map.xml"),
                ("GS: Classic Flame", "https://maps.oc.tc/GS/Classic%20Flame/map.xml"),
                ("GS: Frozen Palace", "https://maps.oc.tc/GS/Frozen%20Palace/map.xml"),
                ("GS: Quartz Mine", "https://maps.oc.tc/GS/Quartz%20Mine/map.xml"),
                ("Glacial Impact 2", "https://maps.oc.tc/GI2/map.xml"),
                ("Golden Drought II", "https://maps.oc.tc/GD2/map.xml"),
                ("Golden Drought III", "https://maps.oc.tc/GD3/map.xml"),
                ("Hallowed Harb", "https://maps.oc.tc/Halloween/Hallowed%20Harb/map.xml"),
                ("Halloween Train", "https://maps.oc.tc/Halloween/Halloween%20Train/map.xml"),
                ("Harb Blitz", "https://maps.oc.tc/Blitz/Harb%20Blitz/map.xml"),
                ("Haunted Blocks", "https://maps.oc.tc/Halloween/Haunted%20Blocks/map.xml"),
                ("Haunted Rings", "https://maps.oc.tc/Halloween/Haunted%20Rings/map.xml"),
                ("Hot Dam: Mini", "https://maps.oc.tc/Hot%20Dam%20Mini/map.xml"),
                ("Industrial Citadel", "https://maps.oc.tc/Blitz/Industry/map.xml"),
                ("Into The Jungle", "https://maps.oc.tc/Blitz/Into%20The%20Jungle/map.xml"),
                ("Kytriak (TE)", "https://maps.oc.tc/Kytriak/map.xml"),
                ("Nuclear Halloween", "https://maps.oc.tc/Halloween/Nuclear%20Halloween/map.xml"),
                ("Plus Side", "https://maps.oc.tc/Blitz/Plus%20Side/map.xml"),
                ("Proelium", "https://maps.oc.tc/Blitz/Proelium/map.xml"),
                ("Race for Victory 2", "https://maps.oc.tc/RFV2/map.xml"),
                ("Race for Victory 3", "https://maps.oc.tc/RFV3/map.xml"),
                ("Rage Quit", "https://maps.oc.tc/Blitz/Rage%20Quit/map.xml"),
                ("Scorched Grove", "https://maps.oc.tc/The%20Scorched%20Grove/map.xml"),
                ("Sky Traffic", "https://maps.oc.tc/SkyTraffic/map.xml"),
                ("Snowy Wars Halloween", "https://maps.oc.tc/Halloween/Snowy%20Wars%20Halloween/map.xml"),
                ("Soviet Chills", "https://maps.oc.tc/Halloween/Soviet%20Chills/map.xml"),
                ("Swarthmoor", "https://maps.oc.tc/Blitz/Swarthmoor/map.xml"),
                ("The 6th Law", "https://maps.oc.tc/Blitz/The%206th%20Law/map.xml"),
                ("The Arena Blitz", "https://maps.oc.tc/Blitz/The%20Arena%20Blitz/map.xml"),
                ("The Complex", "https://maps.oc.tc/Blitz/The%20Arena%20Blitz/map.xml"),
                ("Viridun Blitz", "https://maps.oc.tc/Blitz/Viridun%20Blitz/map.xml") 
               ]

        for m in maps:
            self.update_map_xml_directly(m[0],m[1])

        logging.info("Manual update complete")
        logging.info("Updating mapmakers")
        self.update_mapmakers()
        logging.info("Mapmakers updated")
        self.redirect("/")


#    def update_entity(self, cls, name, **kwargs):
#        """ Updates all attributes in kwargs for entity
#            named 'name' of type 'cls'.
#        """
#
#        entity = cls.query(cls.name == name).get()
#        logging.info('Updating ' + name)
#        
#        if entity:
#            for attr, value in kwargs.iteritems():
#                if hasattr(entity, attr):
#                    setattr(entity, attr, value)
#
#            entity.put()
    

    def update_map_xml_directly(self, name, url):
        """ Updates map xml by calling specified url """

        m = Map.query(Map.name == name).get()
        if m:
            m.get_map_xml_data(url=url)
            m.put()
    
    

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

