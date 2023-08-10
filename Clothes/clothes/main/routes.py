from flask import render_template, Response, request, url_for, flash, redirect, request, abort, Blueprint, session, jsonify
from clothes.models import Post
#Favorite_Post
import os
import secrets
from PIL import Image
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from flask_login import login_user, current_user, logout_user, login_required
from clothes.posts.forms import SearchForm, ClothesForm
import time
import random
from camera import Camera
import base64
import json
#camera = Camera()



main = Blueprint('main', __name__)

#camera = cv2.VideoCapture(0)
#def video_feed():
   # return camera.get_video_feed()
yellow_lower = (20, 100, 100)
yellow_upper = (30, 255, 255)
yellow_lower1 = (90, 60, 0)    # Lower range for navy blue
yellow_upper1 = (130, 255, 70)
yellow_lower2 = (0, 0, 0)    # Lower range for dark grey
yellow_upper2 = (180, 255, 40)

def generate_frames():
    video = cv2.VideoCapture(0)

    while True:
        success, frame = video.read()
        if not success:
            break

        # Process the frame to detect yellow objects and draw a yellow box
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        n = 0
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if n > 5:
                break
            if(area > 300):
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                n = n + 1
                cv2.putText(frame, f'Item {n}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    video.release()

def generate_frames1():
    video = cv2.VideoCapture(0)

    while True:
        success, frame = video.read()
        if not success:
            break

        # Process the frame to detect yellow objects and draw a yellow box
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, yellow_lower1, yellow_upper1)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        n = 0
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if n > 5:
                break
            if(area > 300):
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                n = n + 1
                cv2.putText(frame, f'Item {n}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    video.release()

def generate_frames2():
    video = cv2.VideoCapture(0)

    while True:
        success, frame = video.read()
        if not success:
            break

        # Process the frame to detect yellow objects and draw a yellow box
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, yellow_lower2, yellow_upper2)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        n = 0
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if n > 5:
                break
            if(area > 300):
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                n = n + 1
                cv2.putText(frame, f'Item {n}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    video.release()

'''
def get_video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
def get_video_feed1():
    return Response(generate_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')
def get_video_feed2():
    return Response(generate_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')
def detect(frame):
    #_, imageFrame = camera.read()


    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    yellow_lower = np.array([20, 100, 100], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    kernal = np.ones((5, 5), "uint8")
    
    #for yellow color
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(frame, frame,
                            mask = yellow_mask)

    
    # Creating contour to track yellow color
    contours, hierarchy = cv2.findContours(yellow_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
            
            cv2.putText(frame, "Minion", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))

def gen_frames():  
    while True:
        success, frame = camera.read()
        frame = detect(frame)
          # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

'''

@main.route('/',methods=['GET'])
def extra():
    return render_template('home.html', title = 'Home', form1 = SearchForm())

@main.route('/cams',methods=['POST','GET'])
@login_required
def index():
    return render_template('index.html',title='Cam', form1 = SearchForm())

@main.route('/posts')
def about():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=10)
    return render_template('about.html', title='Posts',posts=posts, form1 = SearchForm())

@main.route('/postsn')
def about1():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.asc()).paginate(per_page=10)
    return render_template('about1.html', title='Posts',posts=posts, form1 = SearchForm())

@main.route('/postsr')
def about3():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=10)
    return render_template('about3.html', title='Posts',posts=posts, form1 = SearchForm())

@main.route('/postsf')
def about4():
    page = request.args.get('page', 1, type = int)
    #posts = Favorite_Post.query.order_by(Favorite_Post.date_posted.desc()).paginate(per_page=10)
    #return render_template('about4.html', title='Posts',posts=posts, form1 = SearchForm())
    posts = Post.query.order_by(Post.date_posted.asc()).paginate(per_page=10)
    return render_template('about1.html', title='Posts',posts=posts, form1 = SearchForm())

@main.route('/questions',methods=['POST','GET'])
def questions():
    form = ClothesForm()
    if form.validate_on_submit():
        session['formality'] = form.formality.data
        session['mood'] = form.mood.data
        flash('We have sent your results to our Artificial Intelligence!', 'success')
        return redirect(url_for('main.processing'))
    return render_template('questions.html', title='Questions', form = ClothesForm(),form1 = SearchForm())

@main.route('/processing',methods=['POST','GET'])
def processing():
    return render_template('processing.html', title='Processing Results',form1 = SearchForm())
    time.sleep(random.random()*10)
    return redirect(url_for('main.index'))
    '''
@main.route('/process_video', methods=['POST'])
def process_video():
    # Get the image_data from the request
    image_data = request.json.get('image_data', None)

    # Convert the base64 image data to a NumPy array
    image_data = image_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(image_data), dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform the yellow object detection using OpenCV.js
    bounding_boxes = detect_yellow_opencv_js(image)

    # Convert the bounding boxes data to a Python list
    bounding_boxes_list = bounding_boxes.tolist()

    # Return the bounding box data as JSON response
    return json.dumps({'boxes': bounding_boxes_list})


    #formality = session.get('formality')
    #mood = session.get('mood')
    #if mood > 7:
    #    return get_video_feed()
    #elif formality < 7:
   #     return get_video_feed1()
  #  else:
   #     return get_video_feed2()

@main.route('/video_feed')
def video_feed():
    camera = Camera()
    camera = cv2.VideoCapture(0)
    formality = session.get('formality')
    mood = session.get('mood')
    if mood > 7:
        return get_video_feed()
    elif formality < 7:
        return get_video_feed1()
    else:
        return get_video_feed2()
    #return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(Camera.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@main.route("/favorite/<int:post_id>", methods=["POST"])
@login_required
def favorite_post(post_id):
    post = Favorite_Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    fav_post = Favorite_Post.query.get_or_404(post_id)
    db.session.add(fav_post)
    db.session.commit()
    flash('Successfully favorited post', 'success')
   # q = session.query(fav_post.id).filter(Item.email==email)
   # session.query(q.exists()).scalar() 
   # else:
   #     current_user.favorite_posts.remove(post)
   #     db.session.commit()
    #    flash('Post removed from favorites', 'danger')
    return render_template('about.html', title='Posts',posts=posts, form1 = SearchForm())
     <!--  <form method="post" action="{{ url_for('main.video_feed') }}">-->

           <!-- <img src="{{ url_for('main.video_feed') }}" height="35%">-->'''