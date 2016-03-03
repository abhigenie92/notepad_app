#https://github.com/udacity/APIs/tree/master/Lesson_3/06_Adding%20Features%20to%20your%20Mashup/Solution%20Code
#https://www.youtube.com/playlist?list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX
from flask import Flask,jsonify, request
app=Flask(__name__)

@app.route('/login',methods=['POST'])
def home():
	data_received = {'username' : request.json['username'], 'password' : request.json['password']}
	# Check if password is correct

    return jsonify({'data_received' : data_received})

@app.route('/create',methods=['POST'])

if __name__ == "__main__":
    app.run()
