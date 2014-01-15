""" Generate the site pages """

import webapp2
import jinja2
import os
import json
import cgi
import logging
import random

from google.appengine.datastore.datastore_query import Cursor

from models.models import Map, Server, MapMaker

# Set environment to use jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')))

class Handler(webapp2.RequestHandler):

    def render(self, template, **kwargs):
        """ Renders page  

            template -- .html jinja2 template to render
            **kwargs -- keyword arguments to pass to template
        """

        template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(template.render(**kwargs))

    def post(self, *args):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        logging.info(search)

        if mt == "map":
            self.redirect("/map/" + search)
        elif mt == "server":
            self.redirect("/server/" + search)
        elif mt == "mapmaker":
            self.redirect("/mapmaker/" + search)
        else:
            self.redirect("/")


class MainPage(Handler):
    """ Main page.
        Just redirects to /maps for now.
    """
    
    def get(self):
        #self.redirect('/maps')

        # prepare data for display
        # longest and shortest maps
        longest_maps = Map.top("avg_length", ascending=False, limit=10)
        shortest_maps = Map.top("avg_length", ascending=True, limit=10)
        longest_maps_data = [[str(m.name), round(m.avg_length / 60.0, 2)] for m in longest_maps]      
        shortest_maps_data = [[str(m.name), round(m.avg_length / 60.0, 2)] for m in shortest_maps]  

        longest_maps_data = [['Map', 'Average Length']] + longest_maps_data
        shortest_maps_data = [['Map', 'Average Length']] + shortest_maps_data


        # most deadly maps
        deadliest_maps = Map.top("kill_density", ascending=False, limit=10)
        deadliest_maps_data = [[str(m.name), round(m.kill_density*60, 2)] for m in deadliest_maps]
        deadliest_maps_data = [['Map', 'Average Kills/Minute']] + deadliest_maps_data  

        peaceful_maps = Map.top("kill_density", ascending=True, limit=10)
        peaceful_maps_data = [[str(m.name), round(m.kill_density*60, 2)] for m in peaceful_maps]
        peaceful_maps_data = [['Map', 'Average Kills/Minute']] + peaceful_maps_data




        # biggest variation
        #std_dev_maps = Map.top("std_length", ascending=False, limit=10)
        #std_dev_maps_data = [[str(m.name), round(m.std_length / 60.0, 2)] for m in std_dev_maps]
        #std_dev_maps_data = [['Map', 'Standard Deviation of Length (minutes)']] + std_dev_maps_data  

        
        # colors for graphs
        # css colors = success: "18bc9c", primary: "2c3e50", warning: f39c12", info: "3498DB", danger: "e74c3c"
        colors = ['#18bc9c', '#f39c12', '#3498db', '#e74c3c']
        random.shuffle(colors)


        self.render("main.html", page_title="Stats", longest_maps_data=longest_maps_data,
                    shortest_maps_data=shortest_maps_data, deadliest_maps_data=deadliest_maps_data,
                    peaceful_maps_data=peaceful_maps_data, colors=colors)        


class MapPage(Handler):
    """ Map page."""
    
    def get(self, map_name):
        # query arguments
        json_rep = self.request.get('json')

        if map_name: 
            mapp = Map.get_by_id(map_name)

            if json_rep == "true":
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(mapp.to_json())
            else:
                self.render('map.html', mapp=mapp, page_title=mapp.name)

        else:
            self.redirect('/maps')


class ServerPage(Handler):
    """ renders a map page """
    
    def get(self, server_name):  
        json_rep = self.request.get('json')

        if server_name:
            server = Server.get_by_id(server_name)

            if json_rep == "true":
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(server.to_json())
            else:
                self.render('server.html', page_title=server.name, server=server)

        else:
            self.redirect('/servers')


class MapMakerPage(Handler):
    """ Map page."""
    
    def get(self, name):

        if name: 
            mm = MapMaker.get_by_id(name)
            self.render('mapmaker.html', mm=mm, page_title=mm.name)

        else:
            self.redirect('/')


class MapsPage(Handler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(Map, sort, page)

        self.render('maps.html', maps=objs['objs'], page=objs['page'], count=objs['count'], 
                    sort=objs['sort'], base_url='/maps', page_title='Maps', nav='maps') 


class MapMakersPage(Handler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(MapMaker, sort, page)

        self.render('mapmakers.html', mms=objs['objs'], page=objs['page'], count=objs['count'], 
                    sort=objs['sort'], nav='mapmakers', page_title='Map Authors', base_url='/mapmakers')    


class ServersPage(Handler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(Server, sort, page)

        self.render('servers.html', servers=objs['objs'], page=objs['page'], count=objs['count'], 
                         sort=objs['sort'], nav='servers', page_title='Servers')
    

class JsonNamePage(Handler):
    """ Returns .json page with list of names of all datastore entites.
        For use with typeahead.js search function
    """

    def get(self, entity):
        if entity.lower() == "maps":
            names = Map.names()
        elif entity.lower() == "servers":
            names = Server.names()
        elif entity.lower() == "mapmakers":
            names = MapMaker.names()
        else:
            self.redirect("/")

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(names))


def get_data_for_table(ModelObject, sort, page):
    """ Queries ndb for PER_PAGE instances
        of ModelObject, sorted by sort.
        For use with /maps and /servers, etc.
    
        Returns dictionary for appending to
        template_values.
    """

    PER_PAGE = 15 # number of table entries per page

    if not page or page < 1:
        page = 1
    page = int(page)
    offset = (page-1)*PER_PAGE

    if sort and sort != 'name':
        try:
            qry = ModelObject.query().order(-getattr(ModelObject, sort))
        except AttributeError:
            qry = ModelObject.query().order(ModelObject.name)

    else:
        sort = 'name'
        qry = ModelObject.query().order(ModelObject.name)

    count = qry.count() // PER_PAGE + 1 # page count
    objs = qry.fetch(PER_PAGE, offset=offset)

    return {'objs': objs, 'count': count, 'page': page, 'sort': sort} 

def model_type(name):
    if name in Map.names():
        return "map"
    elif name in Server.names():
        return "server"
    elif name in MapMaker.names():
        return "mapmaker"
