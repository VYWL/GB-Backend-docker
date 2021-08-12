docker exec -it ggulbob-mysql-container bash
mysql --user=root --password=root
ALTER USER 'ggulbob' IDENTIFIED WITH mysql_native_password BY 'ggulbobpasswd';