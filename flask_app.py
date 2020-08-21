# TODO:
# Jinja:
# - [V] Sent a list from backend to html
# - [V] Generate two or more repeated selection view
# - [V] Incorporate selection view behavior.
#       - [V] Generate response variable guided by the posted information
# - [V] Using Class (ViewController) for global variables
from jinja2 import Template

from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request
from interactive_widgets_builder.flask_view_controller import ViewController

# if __name__ == 'main':
app = Flask(__name__)
#run_with_ngrok(app)  # starts ngrok when the app is run

vw_con = ViewController()


def __my_render_template(html_dir,
                         titles=None,
                         options_collection=None,
                         ipywidget_info=None
                         ):
    template = Template(open('templates/' + html_dir).read())
    rendered_template = template.render(
        titles=titles,
        options_collection=options_collection,
        ipywidget_info=ipywidget_info
    )
    return rendered_template


@app.route("/", methods=['GET', "POST"])
def selection_view():
    if request.method == 'POST':
        vw_con.response_by_altering_view(request)
    else:
        pass
    rendered_template = __my_render_template(
        "selection_view.html",
        titles=vw_con.titles,
        options_collection=vw_con.options_collection,
        ipywidget_info=vw_con.ipywidget_info
    )
    return rendered_template
    # return rendered_template


app.run()
