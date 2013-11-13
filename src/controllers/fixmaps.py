from models.models import Map, Server, MapMaker
import logging
import webapp2

class FixMapsHandler(webapp2.RequestHandler):
    """ Gets matches from oc.tc/matches and store in ndb """

    def get(self):

        maps = Map.query().fetch()
        for m in maps:
            new_key = m.name
            d = m.to_dict(exclude=["frequency","avg_length_s","med_length_s", "std_length_s", "min_length_s", "max_length_s"])
            m_new = Map(id=m.name)
            m_new.populate(**d)
            m_new.put()

           
        servers = Server.query().fetch()
        for s in servers:
            new_key = s.name
            d = s.to_dict(exclude=["n_maps","avg_length_s","med_length_s", "std_length_s", "avg_rotation_length_s"])
            s_new = Server(id=s.name)
            s_new.populate(**d)
            s_new.put()

           
        mms = MapMaker.query().fetch()
        for mm in mms:
            new_key = mm.name
            d = mm.to_dict(exclude=["n_maps","avg_length_s","med_length_s", "std_length_s"])
            mm_new = MapMaker(id=mm.name)
            mm_new.populate(**d)
            mm_new.put()
           

