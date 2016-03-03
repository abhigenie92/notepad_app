#https://github.com/udacity/APIs/tree/master/Lesson_3/06_Adding%20Features%20to%20your%20Mashup/Solution%20Code
#https://www.youtube.com/playlist?list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX
from flask import Flask
app=Flask(__name__)

@app.route('/')
def home():
    return  "This is from Flas again!!!"

if __name__ == "__main__":
    app.run()
