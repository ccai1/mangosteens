import os
import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for, flash
from passlib.hash import sha256_crypt

import db_edit
from util import routes, transit, music

app = Flask(__name__)
app.secret_key = os.urandom(8)

@app.route('/')
def home():
    ''' this function loads up home session, from where user can login and navigate through the website'''
    #checks if there is a session
    if 'user' in session:
        #if there is then just show the welcome screen
        return render_template('welcome.html',
                               user=session['user'])
    else:
        #if not just ask for info
        return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''logs the user in by checking if their login info matches with registered user'''
    username = request.form['usr'].strip()
    password = request.form['pwd'].strip()
    user_exists = db_edit.findInfo('users', db_edit.checkApos(username), 'username', fetchOne = True)
    '''find password for username'''
    if user_exists:
        # print (user_exists)
        # print (password)
        # print (sha256_crypt.verify(password, user_exists[2]))
        if sha256_crypt.verify(password, user_exists[2]):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash("Wrong password!")
            return render_template('home.html')
        flash("Wrong username!")
    return redirect(url_for('home'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    '''registers new account for user'''
    password = request.form['new_pwd'].strip()
    username= request.form['new_usr'].strip()
    pwdCopy = request.form['re_pwd'].strip()
    if username.find("'") == -1:
            if password == pwdCopy:
                # db_edit.insert('users', [username, sha256_crypt.encrypt(password), ""])
                try:
                    db_edit.insert('users', [username, '', sha256_crypt.encrypt(password)])
                    '''insert username and password into database'''
                    flash("Registration complete! Please re-enter your login info.");
                except:
                    flash("That username is taken. Please use a different one.");
            else:
                flash('Passwords do not match.')
    else:
        flash("Pick a username without apostrophes")
    return redirect(url_for('home'))

@app.route('/route', methods=['POST', 'GET'])
def route():
    start = request.form['start'].strip()
    destination = request.form['destination'].strip()
    mode = request.form['mode']

    top_hit = music.get_top_tracks(1)
    print ('---TOP HIT---')
    print (top_hit)

    if start and destination:
        info = routes.getDirectionsInfo(start, destination, "shortest")
        map = routes.get_maps(info)
        distance = routes.get_distance(info)

    # add driving to this
        if mode == "Walking" or mode == "Driving" or mode == "Bicycle":
            '''runs the route.py algorithm'''

            '''ROUTE DIRECTIONS'''

            if mode == "Walking":
                try:
                    info = routes.getDirectionsInfo(start, destination, "pedestrian")
                    route = routes.get_directions(info)
                except:
                    flash("You can't walk that far! Please select a different transportation type.")
                    return redirect(url_for('home'))

            elif mode == "Bicycle":
                info = routes.getDirectionsInfo(start, destination, "bicycle")
            else:
                info = routes.getDirectionsInfo(start, destination, "shortest")

            route = routes.get_directions(info)
            time = routes.get_time(info)
            # time = time[3:5] + ' minutes and ' + time[7:9] + ' seconds'

            # print ("-----ROUTE INFO-----")
            # print (info)

        else:

            '''TRANSIT DIRECTIONS'''

            info = transit.get_transit_info(start, destination)
            route = []

            for i in range (0, len(info)):

                #per route found
                one_route = {}

                #in seconds

                time = transit.get_total_time(info[i])
                directions = transit.get_directions(info[i])
                one_route['time'] = time
                one_route['directions'] = directions
                route.append(one_route)

        # print ("----TRANSIT ROUTES----")
        # print (route)
        print("\n\n-----TOP HITS-----")
        print(time)
        print(top_hit)

        return render_template('route.html',
                               mode=mode,
                               time=time,
                               distance=distance,
                               map=map,
                               routes=route,
                               top_hit = top_hit)
    else:
        flash("Please fill in all address forms.")
        return redirect(url_for('home'))


@app.route('/play', methods=['POST', 'GET'])
def play():
    '''runs the song algorithm'''

    tags = request.form.get('tags')
    s_tags = tags
    tags = tags.split(',')
    artist = request.form.get('artist')

    transit_length = request.form.get('transit_length')
    route_length = request.form.get('route_length')

    if transit_length:
        time = int(transit_length)
    else:
        time = int(route_length)

    print ('---PLAY IS CALLED---')
    print (type(time))
    print (time)

    # playlist = music.get_tracks_tagged(time, tags)

    # if len(tags) == 0:
    #
    #     playlist = music.get_tracks_tagged("None", "None", "None", time)
    # elif len(tags) == 1:
    #     playlist = music.get_tracks_tagged(tags[0], "None", "None", time)
    # elif len(tags) == 2:
    #     playlist = music.get_tracks_tagged(tags[0], tags[1], "None", time)
    # else:
    #     playlist = music.get_tracks_tagged(tags[0], tags[1], tags[2], time)

    if len(tags) == 0:
        playlist = music.gen_playlist(time, "None", "None", "None")
    elif len(tags) == 1:
        playlist = music.gen_playlist(time, tags[0], "None", "None")
    elif len(tags) == 2:
        playlist = music.gen_playlist(time, tags[0], tags[1], "None")
    else:
        playlist = music.gen_playlist(time, tags[0], tags[1], tags[2])

    # if len(tags) == 0:
    #     playlist = music.gen_playlist(time, "None", "None", "None")
    # elif len(tags) == 1:
    #     playlist = music.gen_playlist(time, tags[0], "None", "None")
    # elif len(tags) == 2:
    #     playlist = music.gen_playlist(time, tags[0], tags[1], "None")
    # else:
    #     playlist = music.gen_playlist(time, tags[0], tags[1], tags[2])

    length = len(playlist)
    time = music.get_total_time(playlist)

    # db_edit.insert('playlists', playlist)
    # playlists = db_edit.findInfo('playlists', playlist, 'Songs')
    # print('---HERE---')
    # print (playlists)
    # print (transit_time)

    # playlist = music.gen_playlist(time, tags)

    s_playlist = str(playlist)

    return render_template('play.html',
                           tags=s_tags,
                           playlist = playlist,
                           s_playlist = s_playlist,
                           time = time,
                           length = length
    )

# Consider: Do we need an edit page?
#
@app.route('/edit', methods=['POST', 'GET'])
def edit():
    '''displays the playlist with options to delete, select, and shuffle'''
    # playlist = request.form['playlist']

    playlist = request.form.get('save')
    print ('---PLAYLIST LOOKS LIKE---')
    print (playlist)
    print ('-------------------------')
    user = session['user']
    db_edit.insert('playlists', playlist)
    db_edit.modify('users', 'playlists', playlist, 'Username', user)
    flash("Playlist has been saved!")
    # getting songs and to display
    return redirect(url_for('play'))
# return redirect(url_for('play')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    user=session['user']
    playlists = db_edit.findInfo('users', user, 'Username')[0][1]
    return render_template('profile.html',
                            playlists=playlists,
                            user=session['user'],
    )

@app.route('/user_profile', methods=['POST', 'GET'])
def user_profile():
    user = request.form['user']
    user = db_edit.findInfo('users',user,'Username')
    # print ('--user profile--')
    # print (user)
    username = user[0][0]
    playlists = user[0][1]
    return render_template('user_profile.html',
                            username=username,
                            playlists=playlists,
    )

@app.route('/users', methods=['POST', 'GET'])
def users():
    user = session['user']
    users = db_edit.findInfo('users',user,'Username', notEqual = True)
    print ('our users')
    print (users)
    return render_template('users.html',
                            users=users
        )

@app.route('/logout')
def logout():
    '''pops user from session, brings user back to home page'''
    session.pop('user')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
