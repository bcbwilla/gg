import webapp2, jinja2, os
from models.models import Map, Server

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')))

class MainPage(webapp2.RequestHandler):
    """Main page.
       Nothing interesting yet.
    """
    
    def get(self):
        self.redirect('/maps')        

class MapPage(webapp2.RequestHandler):
    """ Map page."""
    
    def get(self):
        map_name = self.request.get('n')
        json_rep = self.request.get('json') 

        if map_name: 
            mapp = Map.get_by_id(map_name.lower())
        else:
            self.redirect('/')

        if json_rep == "true":
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(mapp.to_json())
        else:
            self.render_page(mapp)

    def to_json(self, m):
        m_attributes = (name for name in dir(m) if not name.startswith('_'))
       
        md = {} # dictionary rep. of map

        print md
        
        # need to convert update date to string
        md['updated_date'] = m.updated_date.isoformat()
        
        # frequency is behaving strangly?
        #md['frequency'] = m.frequency

        #return json.dumps(md)
        
    
    def render_page(self, mapp, json_rep=False):
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
        else:
            self.redirect('/')
        
        if json_rep == "true":
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(server.to_json())
        else:
            self.render_page(server)
    
    def render_page(self, server):
        template_values = {
            'page_title': "Server: " + server.name,
            'server': server
        }
        template = JINJA_ENVIRONMENT.get_template('server.html')
        self.response.write(template.render(template_values))

class MapsPage(webapp2.RequestHandler):

    def get(self):
        sort = self.request.get('sort')

        if sort:
            try:
                maps = Map.query().order(-getattr(Map, sort))
            except AttributeError:
                maps = Map.query().order(Map.name)

        else:
            maps = Map.query().order(Map.name)
        maps = list(maps) 
        self.render_page(maps)     
    
    def render_page(self, maps):
        template_values = {
            'nav': 'maps',
            'page_title': "Maps",
            'maps' : maps
        }
        template = JINJA_ENVIRONMENT.get_template('maps.html')
        self.response.write(template.render(template_values))

class ServersPage(webapp2.RequestHandler):

    def get(self):
        sort = self.request.get('sort')

        if sort == "name":
            servers = Server.query().order(Server.name)
        elif sort:
            try:
                servers = Server.query().order(-getattr(Server, sort))
            except AttributeError:
                servers = Server.query().order(Server.name)
        else:
            servers = Server.query().order(Server.name)
        servers = list(servers) 
        self.render_page(servers)     
    
    def render_page(self, servers):
        template_values = {
            'nav': 'servers',
            'page_title': "Servers",
            'servers' : servers
        }
        template = JINJA_ENVIRONMENT.get_template('servers.html')
        self.response.write(template.render(template_values))

