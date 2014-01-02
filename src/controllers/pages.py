""" Generate the site pages """

import webapp2
import jinja2
import os
import json
import cgi

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


class MainPage(Handler):
    """ Main page.
        Just redirects to /maps for now.
    """
    
    def get(self):
        self.redirect('/maps')


class MapPage(Handler):
    """ Map page."""
    
    def get(self, map_name):
        # query arguments
        json_rep = self.request.get('json')

        if map_name: 
            mapp = Map.get_by_id(map_name)

            if json_rep == "true":
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.write(mapp.to_json())
            else:
                self.render_page(mapp)

        else:
            self.redirect('/maps')

    def post(self):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        if mt == "map":
            self.redirect("../map/" + search)
        elif mt == "server":
            self.redirect("../server/" + search)
        elif mt == "mapmaker":
            self.redirect("../mapmaker/" + search)
        else:
            self.redirect("/")
        
    def render_page(self, mapp):
        """ Renders map page 

        Positional arguments:
        mapp -- Map object 
        
        """

        template_values = {
            'page_title': "Map: " + mapp.name,
            'mapp': mapp
        }
        template = JINJA_ENVIRONMENT.get_template('map.html')
        self.response.write(template.render(template_values))


class ServerPage(Handler):
    """ renders a map page """
    
    def get(self, server_name):  
        json_rep = self.request.get('json')

        if server_name:
            server = Server.get_by_id(server_name)

            if json_rep == "true":
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.write(server.to_json())
            else:
                self.render_page(server)

        else:
            self.redirect('/servers')

    def post(self):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        if mt == "map":
            self.redirect("../map/" + search)
        elif mt == "server":
            self.redirect("../server/" + search)
        elif mt == "mapmaker":
            self.redirect("../mapmaker/" + search)
        else:
            self.redirect("/")
        

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


class MapMakerPage(Handler):
    """ Map page."""
    
    def get(self, name):

        if name: 
            mm = MapMaker.get_by_id(name)
            self.render_page(mm)

        else:
            self.redirect('/')

    def post(self):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        if mt == "map":
            self.redirect("../map/" + search)
        elif mt == "server":
            self.redirect("../server/" + search)
        elif mt == "mapmaker":
            self.redirect("../mapmaker/" + search)
        else:
            self.redirect("/")

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


class MapsPage(Handler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(Map, sort, page)

        self.render_page(objs['objs'], objs['page'], objs['count'], objs['sort']) 

    def post(self):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        if mt == "map":
            self.redirect("../map/" + search)
        elif mt == "server":
            self.redirect("../server/" + search)
        elif mt == "mapmaker":
            self.redirect("../mapmaker/" + search)
        else:
            self.redirect("/")
    
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


class MapMakersPage(Handler):

    def get(self):
        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(MapMaker, sort, page)

        self.render_page(objs['objs'], objs['page'], objs['count'], objs['sort'])    

    def post(self):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        if mt == "map":
            self.redirect("../map/" + search)
        elif mt == "server":
            self.redirect("../server/" + search)
        elif mt == "mapmaker":
            self.redirect("../mapmaker/" + search)
        else:
            self.redirect("/") 
    
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


class ServersPage(Handler):

    def get(self):

        sort = self.request.get('sort')
        page = self.request.get('page')

        objs = get_data_for_table(Server, sort, page)

        self.render_page(objs['objs'], objs['page'], objs['count'], objs['sort'])

    def post(self):
        """ Default post method for nav search bar """
        search = cgi.escape(self.request.get('search')).strip()
        mt = model_type(search)

        if mt == "map":
            self.redirect("../map/" + search)
        elif mt == "server":
            self.redirect("../server/" + search)
        elif mt == "mapmaker":
            self.redirect("../mapmaker/" + search)
        else:
            self.redirect("/")
    
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
