from flask import Flask, render_template, jsonify, request, make_response, json, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import s3troposphere
import ec2troposphere
import vpctroposphere
import rdstroposphere
import customizetroposphere

class Config(object):
    SECRET_KEY = '\xf5\xd4\x90sd\xed\xa8\xf6\x867B\n\xd0\xdcR\xb1'
    SQLALCHEMY_DATABASE_URI='mysql://root:AmazingTheory62@localhost:3306/cloud_formation'
    DEBUG = True


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:AmazingTheory62@localhost:3306/cloud_formation'
app.config.from_object(Config)
db = SQLAlchemy(app)


class s3_table(db.Model):
    sname = db.Column(db.String(50))
    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(80), nullable=False)

    def __init__(self, sname, name, description):
        self.sname = sname
        self.name = name
        self.description = description

    def __repr__(self):
        return '<s3_table %r>' % self.username


class ec2_table(db.Model):
    sname = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(80))
    region = db.Column(db.String(80))
    instance = db.Column(db.String(80))
    vpc = db.Column(db.String(80))
    subnet = db.Column(db.String(80))

    def __init__(self, sname, name, region, instance, vpc, subnet):
        self.sname = sname
        self.name = name
        self.region = region
        self.instance = instance
        self.vpc = vpc
        self.subnet = subnet

    def __repr__(self):
        return '<ec2_table %r>' % self.username


class vpc_table(db.Model):
    sname = db.Column(db.String(50), primary_key=True)
    vname = db.Column(db.String(80))
    vcidr = db.Column(db.String(80))
    sbname = db.Column(db.String(80))
    scidr = db.Column(db.String(80))
    rname = db.Column(db.String(80))
    iname = db.Column(db.String(80))

    def __init__(self, sname, vname, vcidr, sbname, scidr, rname, iname):
        self.sname = sname
        self.vname = vname
        self.vcidr = vcidr
        self.sbname = sbname
        self.scidr = scidr
        self.rname = rname
        self.iname =iname

    def __repr__(self):
        return '<vpc_table %r>' % self.username

class rds_table(db.Model):
    sname = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    storage = db.Column(db.String(80))
    instance = db.Column(db.String(80))
    vname = db.Column(db.String(80))

    def __init__(self, sname, name, username, password, storage, instance, vname):
        self.sname = sname
        self.name = name
        self.username = username
        self.password = password
        self.storage = storage
        self.instance = instance
        self.vname = vname

    def __repr__(self):
        return '<rds_table %r>' % self.username


class login_table(db.Model):
    access_id = db.Column(db.String(50), primary_key=True)
    access_key = db.Column(db.String(80))
    region = db.Column(db.String(50), nullable=False)

    def __init__(self, access_id, access_key, region):
        self.access_id = access_id
        self.access_key = access_key
        self.region = region

    def __repr__(self):
        return '<login_table %r>' % self.username

class customize_table(db.Model):
    sname = db.Column(db.String(50), primary_key=True)
    instance1 = db.Column(db.String(80))
    instancetype1 = db.Column(db.String(80))
    instance2 = db.Column(db.String(80))
    instancetype2 = db.Column(db.String(80))
    dbname = db.Column(db.String(80))
    dbuser = db.Column(db.String(80))
    dbpassword = db.Column(db.String(80))
    dbstorage = db.Column(db.String(80))
    dbinstance = db.Column(db.String(80))
    vpcname = db.Column(db.String(80))
    subnetname = db.Column(db.String(80))

    def __init__(self, sname, instance1, instancetype1, instance2, instancetype2, dbname, dbuser, dbpassword, dbstorage, dbinstance, vpcname, subnetname):
        self.sname = sname
        self.instance1 = instance1
        self.instancetype1 = instancetype1
        self.instance2 = instance2
        self.instancetype2 = instancetype2
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbstorage = dbstorage
        self.dbinstance = dbinstance
        self.vpcname = vpcname
        self.subnetname = subnetname

    def __repr__(self):
        return '<vpc_table %r>' % self.username


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/s3')
def s3_render():
    return render_template('s3.html')


@app.route('/create_s3_bucket', methods=['GET', 'POST'])
def s3():
    if request.method == 'POST':
        if not request.form['stack_name'] or not request.form['bucket_name'] or not request.form['description']:
            flash('Please enter all the fields', 'error')
        else:
            s3dbs = s3_table(request.form['stack_name'], request.form['bucket_name'], request.form['description'])
            db.session.add(s3dbs)
            db.session.commit()
            flash('Record was successfully added')
            s3troposphere.create()
            return redirect(url_for('s3success'))

    return render_template('s3.html')


@app.route('/s3success')
def s3success():
    return render_template('s3success.html')


@app.route('/ec2')
def ec2_render():
    return render_template('ec2.html')


@app.route('/ec2_instance', methods=['GET', 'POST'])
def ec2():
    if request.method == 'POST':
        if not request.form['stack_name'] or not request.form['instance_name'] or not request.form['region'] or not request.form['instance'] or not request.form['vpc'] or not request.form['subnet']:
            flash('Please enter all the fields', 'error')
        else:
            ec2dbs = ec2_table(request.form['stack_name'], request.form['instance_name'], request.form['region'], request.form['instance'], request.form['vpc'], request.form['subnet'])
            db.session.add(ec2dbs)
            db.session.commit()
            flash('Record was successfully added')
            ec2troposphere.create()
            return redirect(url_for('ec2success'))
    return render_template('ec2.html')


@app.route('/ec2success')
def ec2success():
    return render_template('ec2success.html')


@app.route('/rds')
def rds_render():
    return render_template('rds.html')


@app.route('/rds_database', methods=['GET', 'POST'])
def rds():
    if request.method == 'POST':
        if not request.form['stack_name'] or not request.form['db_name'] or not request.form['db_user'] or not request.form['password'] or not request.form['allocated_storage'] or not request.form['instance'] or not request.form['vpc']:
            flash('Please enter all the fields', 'error')
        else:
            rdsdbs = rds_table(request.form['stack_name'], request.form['db_name'], request.form['db_user'], request.form['password'], request.form['allocated_storage'], request.form['instance'], request.form['vpc'])
            db.session.add(rdsdbs)
            db.session.commit()
            flash('Record was successfully added')
            rdstroposphere.create()
            return redirect(url_for('rdssuccess'))
    return render_template('rds.html')


@app.route('/rdssuccess')
def rdssuccess():
    return render_template('rdssuccess.html')


@app.route('/login')
def login_render():
    return render_template('login.html')


@app.route('/login_access', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['id'] or not request.form['key'] or not request.form['region']:
            flash('Please enter all the fields', 'error')
        else:
            logindbs = login_table(request.form['id'], request.form['key'], request.form['region'])
            db.session.add(logindbs)
            db.session.commit()
            flash('Record was successfully added')
            #s3troposphere.create()
            return redirect(url_for('loginsuccess'))
    return render_template('login.html')


@app.route('/loginsuccess')
def loginsuccess():
    return render_template('loginsuccess.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/vpc')
def vpc_render():
    return render_template('vpc.html')


@app.route('/create_vpc', methods=['GET', 'POST'])
def vpc():
    if request.method == 'POST':
        if not request.form['stack_name'] or not request.form['vpc_name'] or not request.form['vpc_cidr'] or not request.form['subnet_name'] or not request.form['subnet_cidr'] or not request.form['route_name'] or not request.form['igw_name']:
            flash('Please enter all the fields', 'error')
        else:
            vpcdbs = vpc_table(request.form['stack_name'], request.form['vpc_name'], request.form['vpc_cidr'], request.form['subnet_name'], request.form['subnet_cidr'], request.form['route_name'], request.form['igw_name'])
            db.session.add(vpcdbs)
            db.session.commit()
            flash('Record was successfully added')
            vpctroposphere.create()
            return redirect(url_for('vpcsuccess'))
    return render_template('vpc.html')


@app.route('/vpcsuccess')
def vpcsuccess():
    return render_template('vpcsuccess.html')


@app.route('/customize')
def customize_render():
    return render_template('customize.html')


@app.route('/custom_arch', methods=['GET', 'POST'])
def customize():
    if request.method == 'POST':
        if not request.form['stack_name'] or not request.form['instance_name1'] or not request.form['instance_type1'] or not request.form['instance_name2'] or not request.form['instance_type2'] or not request.form['db_name'] or not request.form['db_user'] or not request.form['db_password'] or not request.form['allocated_storage'] or not request.form['db_instance'] or not request.form['vpc_name'] or not request.form['subnet_name']:
            flash('Please enter all the fields', 'error')
        else:
            customizedbs = customize_table(request.form['stack_name'], request.form['instance_name1'], request.form['instance_type1'], request.form['instance_name2'], request.form['instance_type2'], request.form['db_name'], request.form['db_user'], request.form['db_password'], request.form['allocated_storage'], request.form['db_instance'], request.form['vpc_name'], request.form['subnet_name'])
            db.session.add(customizedbs)
            db.session.commit()
            flash('Record was successfully added')
            customizetroposphere.create()
            return redirect(url_for('customizesuccess'))
    return render_template('customize.html')


@app.route('/customizesuccess')
def customizesuccess():
    return render_template('customizesuccess.html')


if __name__ == "__main__":
    app.run(port=8080, debug=True)