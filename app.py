from flask import Flask, render_template,request

app = Flask(__name__)

# @app.route("/")
# def home():
# 	return "hi"

#dropdown menu for selecting ETF, testing with colors
@app.route("/", methods=['GET'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template("home.html", colours=colours)

if __name__ == '__main__':
    app.run()