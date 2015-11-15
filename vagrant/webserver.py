from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import *
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>Hello!'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>&iexcl;Hola! <a href="/hello">Back to Hello</a>'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<a href="/restaurants/new">Create new restaurant</a>'

                for restaurant in session.query(Restaurant).all():
                    output += '<h3>%s</h3>' % restaurant.name
                    output += '<p><a href="/restaurants/%s/edit">Edit</a></p>' % restaurant.id
                    output += '<p><a href="/restaurants/%s/delete">Delete</a></p>' % restaurant.id

                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/new"><h2>What is the name of the new restaurant? <input name="name" type="text" /><input type="submit" value="Submit" /></h2></form>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = int(self.path.split('/')[-2])
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/edit"><h2>What is the new name of the restaurant <strong>%s</strong>? <input name="name" type="text" /><input type="submit" value="Submit" /></h2></form>' % (restaurant_id, restaurant.name)
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = int(self.path.split('/')[-2])
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/delete"><h2>Are you sure you want to delete <strong>%s</strong>? <input name="restaurant_id" type="hidden" value="%s" /><input type="submit" value="Submit" /></h2></form>' % (restaurant_id, restaurant.name, restaurant_id)
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                print 'in new'
                self.send_response(200)
                self.end_headers()
                print 'in new after headers'
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    print 'ctype is multipart'
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    print 'creating new restaurant'
                    new_restaurant = Restaurant(name=messagecontent[0])
                    session.add(new_restaurant)
                    session.commit()
                    print 'added new restaurant'

                output = ''
                output += '<html><body>'
                output += '<h2>Restaurant created:<h2>'
                output += '<h1> %s </h1>' % new_restaurant.name

                output += '<a href="/restaurants">Go back to Restaurants</a>'
                output += '</body></html>'
                print 'sending output'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    restaurant_id = int(self.path.split('/')[-2])
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
                    restaurant.name = messagecontent[0]
                    session.add(restaurant)
                    session.commit()

                output = ''
                output += '<html><body>'
                output += '<h2>Restaurant modified:<h2>'
                output += '<h1> %s </h1>' % restaurant.name

                output += '<a href="/restaurants">Go back to Restaurants</a>'
                output += '</body></html>'
                print 'sending output'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_id')
                    restaurant_id = int(self.path.split('/')[-2])
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
                    if int(messagecontent[0]) == restaurant_id:
                        session.delete(restaurant)
                        session.commit()

                output = ''
                output += '<html><body>'
                output += '<h2>Restaurant deleted:<h2>'
                output += '<h1> %s </h1>' % restaurant.name

                output += '<a href="/restaurants">Go back to Restaurants</a>'
                output += '</body></html>'
                print 'sending output'
                self.wfile.write(output)
                print output
                return

            else:
                self.send_response(200)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ''
                output += '<html><body>'
                output += '<h2> Okay, how about this: <h2>'
                output += '<h1> %s </h1>' % messagecontent[0]

                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print 'Web server running on port %s' % port
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C entered, stopping web server...'
        server.socket.close()

if __name__ == '__main__':
    main()