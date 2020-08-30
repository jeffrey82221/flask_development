from flask import Flask, request
from interactive_widgets_builder.view_controller import ViewController

# if __name__ == 'main':
app = Flask(__name__)

vw_con = ViewController()


@app.route("/", methods=['GET', "POST"])
def selection_view():
    if request.method == 'POST':
        vw_con.response_by_altering_view(request)
    else:
        vw_con.entry()
    rendered_template = vw_con.view_para_holder.render_template()
    return rendered_template
    # return rendered_template


app.run()
