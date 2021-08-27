create role user login password 'password';
create database testapp;
grant all privileges on database testapp to 'user'@'%';

FLUSH PRIVILEGES;