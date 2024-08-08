from flask import Flask

app = Flask(__name__)

# here's how you can create a route
@app.route('/test')
def say_hello():   
    return ('hello')

if __name__ == '__main__':
    app.run(debug=True)