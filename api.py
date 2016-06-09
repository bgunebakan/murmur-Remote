from flask import Flask #
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import mice


app = Flask(__name__) #

s1 = mice.m.getServer(1)

if s1.isRunning():
    print "server is running"



# Web api commands     
@app.route("/")
def hello():
        
    return "Mumble Remote Rest api"

@app.route('/userlist', methods=['GET'])
def userlist():
    userlist = ""
    	
    for k,v in s1.getUsers().iteritems():
        print(v.name,v.session)
        userlist = userlist + v.name + ","

    return userlist



@app.route('/<username>/add/<channel>', methods=['GET' , 'POST'])
def addchannel(username,channel):

	
    return username + " added to " + channel

@app.route('/<username>/join/<channel>', methods=['GET' , 'POST'])
def joinchannel(username,channel):
   
    channelid = findChannelid(channel)
    userid = findUserid(username)
    if channelid != -1 and userid != -1: #user and channel exist
 
        User = s1.getUsers()[userid]
        User.channel = channelid

        s1.setState(User)
    
        return username + " joined to " + channel
    else:
        return "error"

@app.route('/<username>/mute/<muted>', methods=['GET' , 'POST'])
def mute(username,muted):

    userid = findUserid(username)
    if userid != -1: # user exist

        User = s1.getUsers()[userid]
	if muted == "True":
	    User.mute = True
        elif muted == "False":
            User.mute = False
        s1.setState(User)

        return username + " is muted"
    else:
        return "error"

@app.route('/<username>/deaf/<deafen>', methods=['GET' , 'POST'])
def deaf(username,deafen):

    userid = findUserid(username)
    if userid != -1: # user exist

        User = s1.getUsers()[userid]
        if deafen == "True":
            User.deaf = True
        elif deafen == "False":
            User.deaf = False
        s1.setState(User)

        return username + " is deafen"
    else:
        return "error"



def findUserid(username):
    userid = -1

    for k,v in s1.getUsers().iteritems():
        if v.name == username:
	    userid = v.session

    return userid

def findChannelid(channel):
    channelid = -1
    
    for k,v in s1.getChannels().iteritems():
        if v.name == channel:
            channelid = v.id
	    
    return channelid


if __name__ == "__main__":
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
