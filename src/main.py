"""
Set all the url handlers to the corresponding urls
"""

import webapp2

from controllers import pages, crons
from maintenance import manual_update

app = webapp2.WSGIApplication([('/', pages.MainPage), 
                               (r'/map/(.*)', pages.MapPage),
                               (r'/server/(.*)', pages.ServerPage),
                               ('/maps', pages.MapsPage),
                               ('/servers', pages.ServersPage),
                               (r'/mapmaker/(.*)',pages.MapMakerPage),
                               ('/mapmakers',pages.MapMakersPage),
                               (r'/data/(.*)',pages.JsonNamePage),
                               ('/crons/getmatches', crons.GetMatchesHandler),
                               ('/crons/updatemaps', crons.UpdateMapStatsHandler),
                               ('/crons/updateservers', crons.UpdateServerStatsHandler),
                               ('/crons/updateocn', crons.UpdateOCNStatsHandler),
                               ('/crons/updategm', crons.UpdateGameModeHandler),
                               ('/crons/updatemapmakers', crons.UpdateMapMakersHandler),
                               ('/manual_update',  manual_update.ManualUpdateHandler)
                               ], debug=True)

