from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

kick_url = "https://player.kick.com/"

available_platforms = [
    {'name': 'Kick', 'url': kick_url}
]

themes = ['green', 'purple', 'black', 'light']

@app.route('/')
def index():
    selected_theme = session.get('theme', 'green')
    return render_template('index.html', available_platforms=available_platforms, themes=themes, theme=selected_theme)

@app.route('/select_theme', methods=['POST'])
def select_theme():
    selected_theme = request.form['theme']
    session['theme'] = selected_theme
    return redirect(request.referrer or url_for('index'))

@app.route('/select_streams', methods=['POST'])
def select_streams():
    names = request.form.getlist('name')
    
    if len(names) < 1 or len(names) > 4:
        return redirect(url_for('index'))

    selected_streams = [f"{kick_url}{name}" for name in names]
    session['selected_streams'] = selected_streams
    return redirect(url_for('streams'))

@app.route('/streams')
def streams():
    selected_streams = session.get('selected_streams', [])
    selected_theme = session.get('theme', 'green')
    return render_template('streams.html', selected_streams=selected_streams, themes=themes, theme=selected_theme)

@app.route('/change_stream', methods=['POST'])
def change_stream():
    index = int(request.form['index'])
    name = request.form['name']
    new_stream_url = f"{kick_url}{name}"

    selected_streams = session.get('selected_streams', [])
    selected_streams[index] = new_stream_url
    session['selected_streams'] = selected_streams
    return redirect(url_for('streams'))

if __name__ == '__main__':
#    app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)
