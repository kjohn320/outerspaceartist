from flask import Flask, render_template, request, url_for, send_file, jsonify
from flask_s3 import FlaskS3
import boto3, botocore
from botocore.exceptions import ClientError

import os

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config["S3_KEY"],
   aws_secret_access_key=app.config["S3_SECRET"],
   region_name=app.config["S3_REGION"],
   config = boto3.session.Config(signature_version=app.config["S3_SIGNATURE_VERSION"])
)

bucket_name = ''
space_img = ''

@app.route('/')
def root():
	items = get_buckets()
	return render_template('index.html',items=items)

@app.route('/saveimage/<base64>')
def saveimage(base64):
	space_img = base64
	return render_template('_form_edit.html', title="Send To Space", form=form)

@app.route('/user/<id>/edit', methods=['GET', 'POST'])
def user_edit(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = ProfileEditForm(user.email)
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.commit()
        return jsonify(status='ok')
    elif request.method == 'GET':
        form.email.data = user.email
    else:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    return render_template('_form_edit.html', title="Send To Space", form=form)

def get_buckets():
	try:
		objects = s3.list_buckets()
		return objects['Buckets']
	except ClientError as e:
		raise e

@app.route('/files', methods=['POST'])
def files():	
	bucket_name = request.form.get('comp_select')
	app.logger.warning("Bucket Name selected %s" % bucket_name)
	try:
		"""Get a list of all keys in an S3 bucket."""
		keys = []
		kwargs = {'Bucket': bucket_name}
		while True:
			resp = s3.list_objects_v2(**kwargs)
			for obj in resp['Contents']:                            
				if obj['Size'] > 0:
					tmpKey = obj['Key']
					keys.append({
						'Key':tmpKey,
						'Client': tmpKey.split('/')[0],
						'File':os.path.split(tmpKey)[1] 
						})
			try:
				kwargs['ContinuationToken'] = resp['NextContinuationToken']
			except KeyError:
				break
                
    
	except ClientError as e:
	# This is a catch all exception, edit this part to fit your needs.
		print("S3 Error: ", e)
		app.logger.error(e, extra={'stack':True})
		raise e
    
	return render_template('results.html',types = resp,files=keys)
    

@app.route('/sendtospace',methods=['POST'])
def sendtospace():
	app.logger.warning('hello')
	if request.method == 'POST':
		return redirect(request.url)
	
@app.route('/download/<path:obj_name>')
def download(obj_name):
    try:
        app.logger.warning(obj_name)
        fileName = os.path.split(obj_name)[1]   
        with open(fileName, 'wb') as f:  
            file = s3.download_fileobj(bucket_name, obj_name, f)

    except ClientError as e:
        raise e

    h = send_file(fileName,
                     mimetype='text/csv',
                     attachment_filename=fileName,
                     as_attachment=True)
    os.remove(fileName)
    return h


if __name__ == "__main__":
    app.run(debug=True,host = "0.0.0.0", port=80)