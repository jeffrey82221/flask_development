from flask import Flask
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
