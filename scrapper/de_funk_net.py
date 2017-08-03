print("Loaded Funk")
def test():
    return "Test"

def setup(app):
    print("register")
    app.register_scrapper('de_funk_net', test)
