from flask import Flask, Response
from flask import request, escape

app = Flask(__name__)

BASE_HTML = """
<a href="/about">About Page</a>
<a href="/no">I do not exist!</a>
</br></br>
<form action="/", method="post">
    <label for="fname">First Name:</label>
    <input type="text" name="first_name"><br><br>
    <label for="fname">Last Name:</label>
    <input type="text" name="last_name">
    <input type="submit" value="Submit">
</form>
<p style="color: red;">Copy this string and put it into an input field for JS injection:</br></br>&lt;script&gt;alert("You've been hacked");&lt;/script&gt;<p>
<form action="/">
    <input type="submit" value="Reload" />
</form>"""

@app.post("/")
def entry_page_post():

    first_name = ""
    last_name = ""
    image = ""

    # Use the get method for the entry page if the input is empty
    if request.form['first_name'] == '' and request.form['last_name'] == '':
        return entry_page_get()

    if request.form['first_name'] != '':
        first_name = request.form['first_name']
        if request.form['first_name'] == 'Peter':
            image = '<img src="static/images/hello_peter.jpg" alt="Shiggy Img" width="279" height="300">'

    # Escape the input for the last name to avoid code injection
    if request.form['last_name'] != '':
        last_name = escape(request.form['last_name'])

    resp = Response()
    returned_content = f"""<h1>Hello, {first_name} {last_name}!</h1>
    {image}</br>""" + BASE_HTML + f"""
    <h2>HTTP Info:</h2>
    <p>    <strong>Header:</strong> {resp.headers}</p>
    <p>    <strong>Status Code:</strong> {resp.status}</p>"""

    return returned_content + f"""<p><strong>HTML:</strong></p>
    <p style="white-space: pre-line;">{escape(returned_content)}</p>
    """


@app.get("/")
def entry_page_get():
    return """<h1>Hello, World!</h1>
    </br>""" + BASE_HTML

@app.route("/about")
def about_page():
    return """
    <h1>Do not press the red button! It's not allowed!</h1>
    <form action="/about" method="post">
        <input style="color: red;" type="submit" value="Press ME!" />
    </form>
    <p>About this page</p>"""


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    resp = Response()
    resp.status_code = 404
    return f"""
    <h2>HTTP Info:</h2>
    <p>    <strong>Header:</strong> {resp.headers}</p>
    <p>    <strong>Status Code:</strong> {resp.status}</p>
    <img src="static/images/confused-john-travolta.gif" alt="Shiggy Img" width="279" height="300">
    """, 404


@app.errorhandler(405)
def page_not_found(e):
    # note that we set the 405 status explicitly
    resp = Response()
    resp.status_code = 405
    return f"""
    <h2>HTTP Info:</h2>
    <p>    <strong>Header:</strong> {resp.headers}</p>
    <p>    <strong>Status Code:</strong> {resp.status}</p>
    <img src="static/images/office_happening.gif" alt="Office Happening" width="480" height="270">
    """, 405
