'''
TODO:
[] 1. Develope Dynamic Randering of Dropdown list
[] 2. Develope Dynamic Randering of Additional Dropdown Confirmation View
[] 3. Incorporate Randering of Ipython Table Widget
[] 4. Refactorization
'''

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__,
            static_url_path="/python",
            static_folder="static",
            template_folder="templates"
            )  # 定義出Flask服務器的根目錄


class Config(object):
    '''
    Config類似一個字典，讓server可以去使用。
    '''
    DEBUG = True
    ITCAST = "python"


ButtonPressed = 0


@app.route('/simple_post', methods=["GET", "POST"])
def simple_post():
    global ButtonPressed
    if request.method == "POST":
        print("Logs:")
        print("content of request (values)", request.values)
        print(request.values.get('member_name'))
        print(request.values.get('project'))
        print()
        if ButtonPressed == 0:
            ButtonPressed = 1
        else:
            ButtonPressed = 0
        return render_template(
            "simple_post.html",
            ButtonPressed=ButtonPressed)
        # I think you want to increment, that case ButtonPressed will be plus 1.
    return render_template(
        "simple_post.html",
        ButtonPressed=ButtonPressed)


@app.route('/simple_widget', methods=["GET", "POST"])
def simple_widget():
    if request.method == "POST":
        print(request.values)
        return render_template(
            "simple_widget.html")
    return render_template(
        "simple_widget.html")


app.config.from_object(Config)


@app.route("/index")
def index():
    print(app.config.get("ITCAST"))
    return "Hello index"


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    # 如果是在其他的文件去啟動執行這個文件的code
    # 那__name___就不是__main__，
    # 如此就不會去執行下面的app.run()。
    app.run(host="127.0.0.1", port=5000, debug=True)
'''
為什麼會有“This is a development server. Do not use it in a production deployment.”
的warning...

在目錄底下的HTML也可以執行

'''
