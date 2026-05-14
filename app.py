from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/pago_sub')
def login():
    return render_template('pago_sub.html')

@app.route('/planes')
def planes():
    return render_template('Plan5.html')

@app.route('/plan5')
def plan5():
    return render_template('Plan5.html')


if __name__ == '__main__':
    app.run(debug=True)