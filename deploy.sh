#!/usr/bin/env bash

scp -i ~/.ssh/apollobrigkey.pem  /Users/brlamore/IdeaProjects/untitled/target/flume-sources-1.0-SNAPSHOT.jar  ec2-user@54.172.245.126:/home/ec2-user

ssh  -i ~/.ssh/apollobrigkey.pem ec2-user@54.172.245.126

sudo mv /home/ec2-user/flume-sources-1.0-SNAPSHOT.jar /home/admin/flume-sources-1.0-SNAPSHOT.jar
sudo chown admin:admin /home/admin/flume-sources-1.0-SNAPSHOT.jar

sudo su admin

cd /home/admin
hadoop fs -rm -R /user/admin/out
hadoop jar flume-sources-1.0-SNAPSHOT.jar com.rockit.nesoi.AssignBounds names out