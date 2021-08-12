#!/bin/bash

DATE=$(date +%Y%m%d%H%M%S)
BACKUP_DIR=/var/lib/mysql/

# 볼륨으로 지정되어 있는 디렉토리에 bobrytime DB 백업
mysqldump -u root -proot --databases bobrytime > $BACKUP_DIR"backup_"$DATE.sql

# 7일 지난 백업 파일은 찾아서 삭제
find $BACKUP_DIR -ctime +7 -exec rm -f {} \;