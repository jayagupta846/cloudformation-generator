from troposphere import GetAtt, Join, Output, Parameter, Ref, Template
from troposphere.ec2 import SecurityGroup
from troposphere.rds import DBInstance, DBSubnetGroup
import mysql.connector
import os

def create():
    mydb1 = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="AmazingTheory62",
        database="cloud_formation"
    )

    mycursor = mydb1.cursor()
    mycursor.execute("SELECT * FROM rds_table")
    myresult = (mycursor.fetchone())
    sname = myresult[0]
    name = myresult[1]
    username = myresult[2]
    password = myresult[3]
    storage = myresult[4]
    instance = myresult[5]
    vname = myresult[6]

    t = Template()

    t.set_description(
        "AWS CloudFormation Sample Template VPC_RDS_DB_Instance: Sample template "
        "showing how to create an RDS DBInstance in an existing Virtual Private "
        "Cloud (VPC). **WARNING** This template creates an Amazon Relational "
        "Database Service database instance. You will be billed for the AWS "
        "resources used if you create a stack from this template.")

    vpcid = t.add_parameter(Parameter(
        "VpcId",
        Type="String",
        Default=vname,
        Description="VpcId of your existing Virtual Private Cloud (VPC)"
    ))

    subnet = t.add_parameter(Parameter(
        "Subnets",
        Type="CommaDelimitedList",
        Default="subnet-022285e80f9d67db7, subnet-0cccbdd282866c95e",
        Description=(
            "The list of SubnetIds, for at least two Availability Zones in the "
            "region in your Virtual Private Cloud (VPC)")
    ))

    dbname = t.add_parameter(Parameter(
        "DBName",
        Default=name,
        Description="The database name",
        Type="String",
        MinLength="1",
        MaxLength="64",
        AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
        ConstraintDescription=("must begin with a letter and contain only"
                               " alphanumeric characters.")
    ))

    dbuser = t.add_parameter(Parameter(
        "DBUser",
        NoEcho=True,
        Default=username,
        Description="The database admin account username",
        Type="String",
        MinLength="1",
        MaxLength="16",
        AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
        ConstraintDescription=("must begin with a letter and contain only"
                               " alphanumeric characters.")
    ))

    dbpassword = t.add_parameter(Parameter(
        "DBPassword",
        NoEcho=True,
        Default=password,
        Description="The database admin account password",
        Type="String",
        MinLength="1",
        MaxLength="41",
        AllowedPattern="[a-zA-Z0-9]*",
        ConstraintDescription="must contain only alphanumeric characters."
    ))

    dbclass = t.add_parameter(Parameter(
        "DBClass",
        Default=instance,
        Description="Database instance class",
        Type="String",
        AllowedValues=[
          "db.m5.large", "db.m1.small", "db.m5.xlarge", "db.m5.2xlarge", "db.m5.4xlarge",
          "db.m5.12xlarge", "db.m5.24xlarge", "db.m4.large", "db.m4.xlarge",
          "db.m4.2xlarge", "db.m4.4xlarge", "db.m4.10xlarge", "db.m4.16xlarge",
          "db.r4.large", "db.r4.xlarge", "db.r4.2xlarge", "db.r4.4xlarge",
          "db.r4.8xlarge", "db.r4.16xlarge", "db.x1e.xlarge", "db.x1e.2xlarge",
          "db.x1e.4xlarge", "db.x1e.8xlarge", "db.x1e.16xlarge", "db.x1e.32xlarge",
          "db.x1.16xlarge", "db.x1.32xlarge", "db.r3.large", "db.r3.xlarge",
          "db.r3.2xlarge", "db.r3.4xlarge", "db.r3.8xlarge", "db.t2.micro",
          "db.t2.small", "db.t2.medium", "db.t2.large", "db.t2.xlarge",
          "db.t2.2xlarge"
        ],
        ConstraintDescription="must select a valid database instance type.",
    ))

    dballocatedstorage = t.add_parameter(Parameter(
        "DBAllocatedStorage",
        Default=storage,
        Description="The size of the database (Gb)",
        Type="Number",
        MinValue="5",
        MaxValue="1024",
        ConstraintDescription="must be between 5 and 1024Gb.",
    ))


    mydbsubnetgroup = t.add_resource(DBSubnetGroup(
        "MyDBSubnetGroup",
        DBSubnetGroupDescription="Subnets available for the RDS DB Instance",
        SubnetIds=Ref(subnet),
    ))

    myvpcsecuritygroup = t.add_resource(SecurityGroup(
        "myVPCSecurityGroup",
        GroupDescription="Security group for RDS DB Instance.",
        VpcId=Ref(vpcid)
    ))

    mydb = t.add_resource(DBInstance(
        "MyDB",
        DBName=Ref(dbname),
        AllocatedStorage=Ref(dballocatedstorage),
        DBInstanceClass=Ref(dbclass),
        Engine="MySQL",
        EngineVersion="5.5",
        MasterUsername=Ref(dbuser),
        MasterUserPassword=Ref(dbpassword),
        DBSubnetGroupName=Ref(mydbsubnetgroup),
        VPCSecurityGroups=[Ref(myvpcsecuritygroup)],
    ))

    t.add_output(Output(
        "JDBCConnectionString",
        Description="JDBC connection string for database",
        Value=Join("", [
            "jdbc:mysql://",
            GetAtt("MyDB", "Endpoint.Address"),
            GetAtt("MyDB", "Endpoint.Port"),
            "/",
            Ref(dbname)
        ])
    ))

    print(t.to_json())
    file = open('rdsjson.json', 'w')
    file.write(t.to_json())
    file.close()
    os.system('aws cloudformation create-stack --stack-name ' + sname + ' --template-body file://rdsjson.json')