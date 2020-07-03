from flask import Flask, request, render_template, Markup
from processing import load_data, person_id_for_name, display_result, confirm
app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True

@app.route('/degrees', methods=["GET", "POST"])
def adder_page():
  return None