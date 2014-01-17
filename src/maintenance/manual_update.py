import webapp2
import logging
from models.models import Match, Map, Server, OCN, MapMaker


class ManualUpdateHandler(webapp2.RequestHandler):

    def get(self):
        logging.info("Beginning manual update")

        # put entites to update manually here.
        

        maps = [
               "AstroGEN",
               "The Arena Blitz",
               "Battle of Lyndanisse Blitz",
               "Bliss",
               "Blitzkrieg",
               "Cairo Blitz",
               "CatalystMC Blitz",
               "The Complex",
               "CotBot",
               "Harb Blitz",
               "Industrial Citadel",
               "Metallicus",
               "No Return",
               "Overgrown Blitz",
               "Ozone Blitz",
               "Permeac",
               "Proelium",
               "Twilight Zone: Blitz",
               "Venice Blitz",
               "Viridun Blitz",
               "Cake Wars 3",
               "Dead Heat",
               "Undead Heat",
               "War Wars"]

        for m in maps:
            self.update_entity(Map, m, gamemode="Blitz")

        logging.info("Blitz")

        maps = [
                "Arcane Realms",
                "Grand Hall",
                "Parallax",
                "Banana Split",
                "Blocks CTW",
                "Broken Unity",
                "Buried Down",
                "Cargo",
                "Circus CTW",
                "Cloud Nine",
                "Deepwind Jungle",
                "Dynamo",
                "Empire",
                "Fairy Tales 2: A Tale or Two",
                "Golden Drought",
                "Golden Drought II",
                "Golden Drought III",
                "Hadron",
                "Haunted Rings",
                "Hydrolock",
                "Hydrolock II",
                "Jungle Beat",
                "Kytriak (TE)",
                "Mushroom Gorge",
                "Placid Spring",
                "Race For Victory",
                "Race For Victory 2",
                "Race For Victory 3",
                "Race Through the Forest",
                "Ring Race",
                "Selenius",
                "Tenebrous",
                "Turf Wars",
                "Twisted",
                "Two Castles",
                "Two Tier",
                "Utopia",
                "Welcome To Wool Square"]

        for m in maps:
            self.update_entity(Map, m, gamemode="CTW")

        logging.info("CTW")


        maps = [
                "Suburban Complex",
                "Avalon Funland",
                "Airship Battle",
                "Avalanche",
                "Battle of Tenjin",
                "Battle of Tenjin 2",
                "Bessemer's Process",
                "Black Gold",
                "Blocks DTC",
                "Bridge Over Troubled Water",
                "Cake Wars",
                "Fallencrests",
                "Fallencrests 2",
                "Fortress Battles",
                "Full Salvo",
                "Haunted Blocks",
                "Holiday Blocks",
                "Hot Dam",
                "Hot Dam: Mini",
                "Inheritance",
                "Interitus",
                "Ion",
                "Mayan Apocalypse",
                "Medieval Warfare",
                "Nuclear Halloween",
                "Nuclear Winter",
                "Runes of Ruin",
                "Shroom Trip",
                "Sky Traffic",
                "Sky Traffic 2",
                "Solitude",
                "SolitudeMC",
                "Temple Run",
                "Temple Valley",
                "Total War",
                "Tower Sight",
                "Tree of Life",
                "Winterhold"
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="DTC")

        logging.info("DTC")


        maps = [
                "Train Wars",
                "The 4th Law",
                "Spaceship Battles II",
                "Spaceship Battles",
                "SSB Halloween",
                "Synergy"
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="Mixed")

        logging.info("Mixed")



        maps = [
                'A Watery Grave 2',
                'Aerobellum',
                'Anathema',
                'Antiquis',
                'Atromix',
                'Balloon Archipelago',
                'BalloonsDTM',
                'BalloonsDTM: Halloween',
                'Baroque Gardens',
                'Blizzard',
                'Boom',
                'Callorbus',
                'Cathedral',
                'Corrupted Kingdoms',
                'Desert Cataract',
                'Escensio',
                'The Fenland',
                'Fort Wars',
                'Galactic War',
                'Ghostwind Mountain',
                'Glacial Impact 2',
                'Halloween Train',
                'Merry Drought',
                'Midnight Train',
                'Molendinis',
                'The Nile',
                'Scorched Grove',
                'Snowy Wars',
                'Snowy Wars Christmas',
                'Snowy Wars Halloween',
                'Soviet Chills',
                'Soviet Mills',
                'Sunrise over Paradise',
                'Warlock',
                'A Watery Grave'
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="DTM")

        logging.info("DTM")



        maps = [
                'Icescar',
                'Rift',
                'Tempest',
                'Lunar Coliseum',
                "Pharaoh's Catacombs",
                'Necro'
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="Gear")

        logging.info("Gear")



        maps = [
                'GS: Classic Flame',
                'GS: Deserted',
                'GS: Desolated',
                'GS: Eldritch',
                'GS: Frozen Palace',
                'GS: Grassy Knoll',
                'GS: Molten Crevasse',
                'GS: Nostalgia',
                'GS: Prototype',
                'GS: Quartz Mine',
                'GS: Royal Garden',
                'GS: Splinter',
                'GS: Twisted',
                'GS: Vengeance'
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="GS")

        logging.info("GS")


        maps = [ 
                "Ascension",
                "Cabin Fever",
                "Cat's Cradle",
                "Diablo",
                "Equinox",
                "The Hill",
                "Storm",
                "Urban Jungle",
                "Villa Estus"
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="KOTH")

        logging.info("KOTH")


        maps = [
                '100 Rooms',
                '101 Pumpkins',
                '101 Rooms',
                'The 6th Law',
                'Arid Crossroads',
                'BipBeta Halloween',
                'BipBetaMC',
                'Dry Wound',
                'Fallen Courtyard',
                'Grimsnes',
                'Hallow Side',
                'Into The Jackolantern',
                'Into The Jungle',
                'Plus Side',
                'Quavilla',
                'Rage Quit',
                'Swarthmoor',
                'Zero Gravity'
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="Rage")

        logging.info("Rage")


        maps = [
                'Babylon',
                'BipBetaMC: TDM',
                'Zoo',
                'Abandoned Zoo',
                'Arcane Sanctuary',
                'The Archives',
                'The Arena',
                'Aurimar Rift',
                'Battle of Lyndanisse',
                'Cairo TDM',
                'Chemical Reaction',
                'Festive Venice',
                'Funerea',
                'Hallowed Harb',
                'Harb',
                'Icebliss',
                'Modern Cityscape',
                'Mortal Jungle',
                'Northern Mounts',
                'Ozone',
                'Pipe Factory',
                'Sand Wars',
                'SuperPRISM',
                'Trench Warfare 2',
                'Twilight Zone',
                'Venice TDM',
                'Viridun',
                'Wildwood Crevice',
                'Wooly Woods',
                'Yule TDM'
                ]

        for m in maps:
            self.update_entity(Map, m, gamemode="TDM")


        logging.info("TDM")


        #

        """
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
        """

        

        logging.info("Manual update complete")
        #logging.info("Updating mapmakers")
        #self.update_mapmakers()
        #logging.info("Mapmakers updated")
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

