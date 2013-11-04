#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
                               ('/crons/getmatches', crons.GetMatchesHandler),
                               ('/crons/updatemaps', crons.UpdateMapStatsHandler),
                               ('/crons/updateservers', crons.UpdateServerStatsHandler),
                               ('/crons/updateocn', crons.UpdateOCNStatsHandler),
                               ('/crons/updategm', crons.UpdateGameModeHandler)
                               ], debug=True)

