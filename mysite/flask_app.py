from flask import Flask, request, render_template, Markup
from processing import load_data, person_id_for_name, display_result, confirm
app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True

@app.route('/degrees', methods=["GET", "POST"])
def adder_page():
    confirmation = ""
    errors = ""

    if request.method == "POST":
        load_data("mysite/smallweb")

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
                    errors += "{!r} was not found.".format(request.form["actor-one"])
                elif target is None:
                    confirmation = ""
                    errors += "{!r} was not found.".format(request.form["actor-two"])
                elif ((len(source) > 20) and (source != None) and (target != None)):
                    confirmation = Markup(source)
                    source = None
                    if (len(target) > 15):
                        confirmation2 = Markup(target)
                        source = None
                        return render_template('confirmations.html',
                        confirmation1=confirmation, confirmation2=confirmation2,
                        errors=errors, number="3", actor1=actor1, actor2=actor2,
                        confirmed1="confirmed-id1", confirmed2="confirmed-id2")
                    else:
                        return render_template('confirmation.html',
                        confirmation=confirmation, errors=errors, number="1",
                        actor1=actor1, actor2=actor2, confirmed="confirmed-id1")

                elif ((len(target) > 20) and (target != None) and (source != None)):
                    confirmation = Markup(target)
                    target = None
                    return render_template('confirmation.html',
                    confirmation=confirmation, errors=errors, number="2",
                    actor1=actor1, actor2=actor2, confirmed="confirmed-id2")

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
                    errors += "{!r} was not found.".format(request.form["actor-one"])
                target = person_id_for_name(actor2)
            elif (duplicate == "2"):
                actor_id = str(request.form["confirmed-id2"])
                target = confirm(actor2, actor_id)
                if target is None:
                    errors += "{!r} was not found.".format(request.form["actor-two"])
                source = person_id_for_name(actor1)
            else:
                actor_id1 = str(request.form["confirmed-id1"])
                actor_id2 = str(request.form["confirmed-id2"])
                source = confirm(actor1, actor_id1)
                target = confirm(actor2, actor_id2)
                if source is None:
                    errors += "{!r} was not found.".format(request.form["actor-one"])
                if target is None:
                    errors += "{!r} was not found.".format(request.form["actor-two"])

        if source is not None and target is not None:
            result = display_result(source, target)
            value = Markup(result)
            return render_template('result.html', result=value)

    return render_template('index.html', confirmation=confirmation, errors=errors)
