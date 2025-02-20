CREATE DATABASE IF NOT EXISTS library_admin;
CREATE DATABASE IF NOT EXISTS library_frontend;


GRANT ALL PRIVILEGES ON library_frontend.* TO 'motunrayo'@'%';
GRANT ALL PRIVILEGES ON library_admin.* TO 'motunrayo'@'%';

FLUSH PRIVILEGES;