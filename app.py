### SETUP ###
import typing
import sanic, sanic.response

# Create the Sanic app
app = sanic.Sanic(__name__)

# This dictionary represents your "static"
# redirects. For example, these values
# could be pulled from a configuration file.
REDIRECTS = {
    '/':'/hello_world',                     # Redirect '/' to '/hello_world'
    '/hello_world':'/hello_world.html'      # Redirect '/hello_world' to 'hello_world.html'
}

# This function will return another function
# that will return the configured value
# regardless of the arguments passed to it.
def get_static_function(value:object) -> typing.Callable[..., object]:
    return lambda *_, **__: value

### ROUTING ###
# Iterate through the redirects
for src, dest in REDIRECTS.items():                            
    # Create the redirect response object         
    response:sanic.HTTPResponse = sanic.response.redirect(dest)

    # Create the handler function. Typically,
    # only a sanic.Request object is passed
    # to the function. This object will be 
    # ignored.
    handler = get_static_function(response)

    # Route the src path to the handler
    app.route(src)(handler)

# Route some file and client resources
app.static('/files/', 'files')
app.static('/', 'client')

### RUN ###
if __name__ == '__main__':
    app.run(
        '127.0.0.1',
        10000
    )