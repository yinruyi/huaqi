#coding=utf8

from app import app

if __name__ == '__main__':
    # run app
    app.run(host=app.config['DEBUG_HOST'], \
        port=app.config['DEBUG_PORT'], \
        debug=True)
