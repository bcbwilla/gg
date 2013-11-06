""" Generate the site pages """

import webapp2
import jinja2
import os

from models.models import Map, Server, MapMaker

# Set environment to use jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')))


class MainPage(webapp2.RequestHandler):
    """ Main page.
        Just redirects to /maps for now.
    """
    
    def get(self):
        self.redirect('/maps')        


class MapPage(webapp2.RequestHandler):
    """ Map page."""
    
    def get(self):
        # query arguments
        map_name = self.request.get('n')
        json_rep = self.request.get('json')

        if map_name: 
            mapp = Map.get_by_id(map_name.lower())

            if json_rep == "true":
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.write(mapp.to_json())
            else:
                self.render_page(mapp)

        else:
            self.redirect('/maps')
        
    def render_page(self, mapp, json_rep=False):
        """ Renders map page 

        Positional arguments:
        mapp -- Map object 

        Keyword arguments:
        json_rep -- if to display page as json string
        
        """

        template_values = {
            'page_title': "Map: " + mapp.name,
            'mapp': mapp
        }
        template = JINJA_ENVIRONMENT.get_template('map.html')
        self.response.write(template.render(template_values))


class ServerPage(webapp2.RequestHandler):
    """ renders a map page """
    
    def get(self):
        server_name = self.request.get('n')  
        json_rep = self.request.get('json')

        if server_name:
            server = Server.get_by_id(server_name.lower())

            if json_rep == "true":
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.write(server.to_json())
            else:
                self.render_page(server)

        else:
            self.redirect('/servers')
        

    def render_page(self, server):
        """ Renders server page 

        Positional arguments:
        server -- Server object 
        
        """

        template_values = {
            'page_title': "Server: " + server.name,
            'server': server
        }
        template = JINJA_ENVIRONMENT.get_template('server.html')
        self.response.write(template.render(template_values))


class MapMakerPage(webapp2.RequestHandler):
    """ Map page."""
    
    def get(self):
        # query arguments
        name = self.request.get('n')

        if name: 
            mm = MapMaker.get_by_id(name.lower())
            self.render_page(mm)

        else:
            self.redirect('/')
        
    def render_page(self, mm):
        """ Renders map page 

        Positional arguments:
        mapp -- Map object 
        
        """

        template_values = {
            'page_title': "Map Maker: " + mm.name,
            'mm': mm
        }
        template = JINJA_ENVIRONMENT.get_template('mapmaker.html')
        self.response.write(template.render(template_values))


class MapsPage(webapp2.RequestHandler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(Map, sort, page)

        self.render_page(objs['objs'], objs['page'], objs['count'], objs['sort'])     
    
    def render_page(self, maps, page, count, sort):
        """ Renders maps page 

        Positional arguments:
        maps -- list of Map objects 
        page -- page of maps
        count -- total number of map objects in datastore
        sort -- query parameter to sort by
        
        """

        template_values = {
            'nav': 'maps',
            'page_title': "Maps",
            'maps': maps,
            'sort': sort,
            'page': page,
            'count': count,
            'base_url': "/maps"
        }
        template = JINJA_ENVIRONMENT.get_template('maps.html')
        self.response.write(template.render(template_values))


class MapMakersPage(webapp2.RequestHandler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(MapMaker, sort, page)

        self.render_page(objs['objs'], objs['page'], objs['count'], objs['sort'])     
    
    def render_page(self, mms, page, count, sort):
        """ Renders maps page 

        Positional arguments:
        mms -- list of MapMaker objects 
        page -- page of maps
        count -- total number of map objects in datastore
        sort -- query parameter to sort by
        
        """

        template_values = {
            'nav': 'mapmakers',
            'page_title': "Map Authors",
            'mms': mms,
            'sort': sort,
            'page': page,
            'count': count,
            'base_url': "/mapmakers"
        }
        template = JINJA_ENVIRONMENT.get_template('mapmakers.html')
        self.response.write(template.render(template_values))


class ServersPage(webapp2.RequestHandler):

    def get(self):

        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(Server, sort, page)

        self.render_page(objs['objs'], objs['page'], objs['count'], objs['sort'])   
    
    def render_page(self, servers, page, count, sort):
        """ Renders servers page 

        Positional arguments:
        servers -- list of Server objects 
        page -- page of maps
        count -- total number of map objects in datastore
        sort -- query parameter to sort by
        
        """

        template_values = {
            'nav': 'servers',
            'page_title': "Servers",
            'servers' : servers,
            'sort': sort,
            'page': page,
            'count': count
        }
        template = JINJA_ENVIRONMENT.get_template('servers.html')
        self.response.write(template.render(template_values))


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

