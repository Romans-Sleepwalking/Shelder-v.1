from bottle import route, run, static_file
import data


@route('/')
def root():
    return static_file("index.html", "./")


@route('/speedDating.js')
def speedDatingJS():
    return static_file("speedDating.js", "./")


@route('/data')
def Data():
    shelter = data.LabasMajasShelter()
    return shelter.getCutties()
    

run(host='0.0.0.0', port=8080, debug=True)