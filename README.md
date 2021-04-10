# web-apps-hw5
Group Homework 5 for CSCI 4710 Web Applications


Database setup instructions

The following instructions assume that you have a database user created. That user will be referred to as [user] from now on. 

```
create database hw5db;
create user admin5 with encrypted password 'web_apps';
grant all privileges on database hw5db to admin5;
```