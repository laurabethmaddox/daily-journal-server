from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_entries, get_single_entry, delete_entry, update_entry, get_entries_by_search, create_entry
from views import get_all_moods
from views import get_all_tags
from views import get_all_entrytags

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the 
        # path is "/entries/1", the resulting list will
        # have "" at index 0, "entries" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # Example: /customers?email=jenna@solis.com

            param = resource.split("?")[1] # email=jenna@solis.com
            resource = resource.split("?")[0] # 'customers'
            pair = param.split("=") # [ 'email', 'jenna@solis.com' ]
            key = pair[0] # 'email'
            value = pair[1] # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            # Try to get the item at index 2
            try:
                # Convert the string "2" to the integer 2
                id = int(path_params[2])
            except IndexError:
                pass # No route parameter exists: /entries
            except ValueError:
                pass # Request had trailing slash: /entries/

            return (resource, id) # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)
        response = {} # Default response

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/entries` or `/entries/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            # It's an if..else statement
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"

            if resource == "moods":
                response = f"{get_all_moods()}"

            if resource == "tags":
                response = f"{get_all_tags()}"

            if resource == "entrytags":
                response = f"{get_all_entrytags()}"

        # Response from parse_url is a tuple with 3
        # items in it, which means the request was for 
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `entries` and was there a 
            # query parameter that specified the entry
            # as a filtering value?
            if key == "q" and resource == "entries":
                response = f"{get_entries_by_search(value)}"

        # This weird code sends a response back to the client
        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry
        new_entry = None

        # Add a new entry to the list
        if resource == "entries":
            new_entry = create_entry(post_body)

            # Encode the new entry and send in response
            self.wfile.write(f"{new_entry}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single entry from the list
        if resource == "entries":
            success = update_entry(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new entry and send in response
        self.wfile.write("".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any DELETE request.
    def do_DELETE(self):
        """Handles DELETE requests to the server
        """
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single entry from the list
        if resource == "entries":
            delete_entry(id)

            # Encode the new entry and send in response
            self.wfile.write(f"{delete_entry}".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
