"""
Set all the url handlers to the corresponding urls
"""

import webapp2

from controllers import pages, crons

app = webapp2.WSGIApplication([('/', pages.MainPage), 
                               ('/map', pages.MapPage),
                               ('/server', pages.ServerPage),
                               ('/maps', pages.MapsPage),
                               ('/servers', pages.ServersPage),
                               ('/mapmaker',pages.MapMakerPage),
                               ('/mapmakers',pages.MapMakersPage),
                               ('/crons/getmatches', crons.GetMatchesHandler),
                               ('/crons/updatemaps', crons.UpdateMapStatsHandler),
                               ('/crons/updateservers', crons.UpdateServerStatsHandler),
                               ('/crons/updateocn', crons.UpdateOCNStatsHandler),
                               ('/crons/updategm', crons.UpdateGameModeHandler),
                               ('/crons/updatemapmakers', crons.UpdateMapMakersHandler)
                               ], debug=True)

