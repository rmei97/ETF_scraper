from flask import Flask, render_template,request

app = Flask(__name__)

# @app.route("/")
# def home():
# 	return "hi"

#dropdown menu for selecting ETF, testing with colors
# @app.route("/", methods=['GET'])
# def dropdown():
#     colours = ['Red', 'Blue', 'Black', 'Orange']
#     return render_template("home.html", colours=colours)

# if __name__ == '__main__':
#     app.run()


@app.route("/")
# def home():
#     return render_template('home.html')	

def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            render_template('about.html') # do something
        elif request.form['submit_button'] == 'Do Something Else':
            print('do something else') # do something else
        else:
            print('sometung something else') # unknown
    elif request.method == 'GET':
        return render_template('home.html')

@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

@app.route("/about")
def about():
	return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)