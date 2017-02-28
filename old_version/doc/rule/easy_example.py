"""
This file is a easy sample code of server
"""

import flask

# create an server application object
Server_App = flask.Flask(__name__)

# a handler for example
@Server_App.route("/action",methods=['POST'])
def action():
    # get post data
    post_data = flask.request.form
    a = post_data['a']
    b = post_data['b']
    # return result to client
    response = {'recv_a':a,'recv_b':b}
    return flask.jsonify(response)

if __name__ == '__main__':
    Server_App.run(host="127.0.0.1",port=8081)

"""
how to run when debug ?
    python easy_example.py
how to check ?
    curl -XPOST 127.0.0.1:8081/action -d 'a=hello&b=world'
"""
