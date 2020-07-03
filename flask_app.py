from flask import Flask, request
from processing import load_data, person_id_for_name, display_result, confirm
app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True

@app.route('/', methods=["GET", "POST"])
def adder_page():
    load_data("mysite/small")
    confirmation = ""
    errors = ""
    confirmation_form = '''
        <form method="post" action=".">
            <input type="hidden" id="actor-one" name="actor-one" value="{actor1}">
            <input type="hidden" id="actor-two" name="actor-two" value="{actor2}">
            <input type="hidden" id="duplicate" name="duplicate" value="{number}">
        '''
    id_field = '''<label for="{confirmed}">ID:</label>
        <input type="text" id="{confirmed}" name="{confirmed}" required><br>
        '''
    form_end = '''
            <input type=submit name="action" value="Confirm ID">
        </form>
        '''
    if request.method == "POST":
        source = None
        target = None

        if request.form["action"] == "Find degrees":
            actor1 = str(request.form["actor-one"])
            actor2 = str(request.form["actor-two"])
            try:
                source = person_id_for_name(actor1)
                target = person_id_for_name(actor2)

                if source is None:
                    confirmation = ""
                    errors += "<p>{!r} was not found.<p>".format(request.form["actor-one"])
                elif target is None:
                    confirmation = ""
                    errors += "<p>{!r} was not found.<p>".format(request.form["actor-two"])
                elif ((len(source) > 20) and (source != None) and (target != None)):
                    confirmation += source
                    source = None
                    if (len(target) > 20):
                        confirmation += confirmation_form.format(actor1=actor1, actor2=actor2, number="3")
                        confirmation += id_field.format(confirmed="confirmed-id1")
                        confirmation += target
                        target = None
                        confirmation += id_field.format(confirmed="confirmed-id2")
                    else:
                        confirmation += confirmation_form.format(actor1=actor1, actor2=actor2, number="1")
                        confirmation += id_field.format(confirmed="confirmed-id1")
                    confirmation += form_end
                elif ((len(target) > 20) and (target != None) and (source != None)):
                    confirmation += target
                    target = None
                    confirmation += confirmation_form.format(actor1=actor1, actor2=actor2, number="2")
                    confirmation += id_field.format(confirmed="confirmed-id2")
                    confirmation += form_end

            except:
                confirmation = ""
                errors += "Not a valid entry"

        else:
            actor1 = request.form["actor-one"]
            actor2 = request.form["actor-two"]
            duplicate = request.form["duplicate"]

            if (duplicate == "1"):
                actor_id = str(request.form["confirmed-id1"])
                source = confirm(request.form["actor-one"], actor_id)
                if source is None:
                    errors += "<p>{!r} hey was not found.<p>".format(request.form["actor-one"])
                target = person_id_for_name(actor2)
            elif (duplicate == "2"):
                actor_id = str(request.form["confirmed-id2"])
                target = confirm(actor2, actor_id)
                if target is None:
                    errors += "<p>{!r} no was not found.<p>".format(request.form["actor-two"])
                source = person_id_for_name(actor1)
            else:
                actor_id1 = str(request.form["confirmed-id1"])
                actor_id2 = str(request.form["confirmed-id2"])
                source = confirm(actor1, actor_id1)
                target = confirm(actor2, actor_id2)
                if source is None:
                    errors += "<p>{!r} hey was not found.<p>".format(request.form["actor-one"])
                if target is None:
                    errors += "<p>{!r} no was not found.<p>".format(request.form["actor-two"])

        if source is not None and target is not None:
            result = display_result(source, target)
            return '''
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Degrees of Separation</title>
                    </head>
                    <body>
                        <div class="hero-text">
                            <p>{result}</p>
                            <p><a href="/">Click here to calculate again</a>
                        </div>
                    </body>
                </html>
            '''.format(result=result)
    href = 'styles/style.css'

    return '''
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Degrees of Separation</title>
                <link rel="stylesheet" type= "text/css" href="{{ url_for('static', filename={href}) }}">
            </head>
            <body>
                <div class="hero-text">
                    <h1> Degrees of Separation</h1>
                    <p>
                        This program  determines how many
                        <a href=https://en.wikipedia.org/wiki/Six_degrees_of_separation>
                            degrees of separation
                        </a>
                        apart two actors are given an IMDb dataset.
                    </p>
                </div>
                <div class="form-container">
                    <h3>Please enter two actors</h3>
                    <form class="name-form" method="post" action=".">
                        <label for="actor-one">Actor 1:</label>
                        <input type="text" id="actor-one" name="actor-one" required><br>
                        <label for="actor-two">Actor 2:</label>
                        <input type="text" id="actor-two" name="actor-two" required><br>
                        <input type=submit name="action" value="Find degrees"><br><br>
                    </form>
                      <p>{confirmation}</p>
                      <p>{errors}</p>
                </div>
            </body>
        </html>
        '''.format(href=href, confirmation=confirmation, errors=errors)
