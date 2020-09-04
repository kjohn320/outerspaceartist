from flask import Flask, render_template, request, url_for, send_file, jsonify, session
from flask_s3 import FlaskS3
import boto3, botocore
from botocore.exceptions import ClientError
import time
import os
import base64

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

s3 = boto3.client(
	"s3",
   aws_access_key_id=app.config["S3_KEY"],
   aws_secret_access_key=app.config["S3_SECRET"],
   region_name=app.config["S3_REGION"],
   config = boto3.session.Config(signature_version=app.config["S3_SIGNATURE_VERSION"])
)

bucket_name = app.config["S3_BUCKET"]
space_img = ''

@app.route('/')
def root():
	return render_template('index.html')

@app.route('/galaxy_creator')
def galaxy_creator():
	return render_template('galaxy_creator.html')

@app.route('/sendtogalaxyForm')
def sendtogalaxyForm():
	return render_template('_form_edit.html')

@app.route('/saveimgLocal',methods=['POST'])
def saveimgLocal():
	if request.method == 'POST':
		data = request.get_json()
		app.logger.warning('hello')

		space_img = request.json['data']
		space_img = space_img.replace("data:image/png;base64,","")
		session['space_img'] = space_img
		app.logger.warning(space_img)
	return 'success',200

@app.route('/uploadToSpace',methods=['POST'])
def uploadToSpace():
	username = request.form.get('username')
	galaxyname = request.form.get('galaxyname')
	ts = time.time()
	name = username+ "/"+ galaxyname + "/" + str(int(ts)) + ".png"
	app.logger.warning(space_img)
	myimg = session['space_img']
	try:
		kwargs = {'Bucket': bucket_name,
		'Key': name,
		'Body': base64.b64decode(my_img),
		'ContentType':'image/png'}
		resp = s3.put_object(**kwargs)
		app.logger.warn(resp)
		return 'success',200
	except ClientError as e:
		raise e

@app.route('/saveimage/<base64>')
def saveimage(base64):
	space_img = base64
	return render_template('_form_edit.html', title="Send To Space", form=form)



if __name__ == "__main__":
    app.run(debug=True,host = "0.0.0.0", port=80)