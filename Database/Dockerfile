FROM mysql:8.0.26

MAINTAINER JuwonLee <webmon0727@gmail.com>
# 첫 실행 시 create.sql 파일 실행
ADD ./mysql-init-files /docker-entrypoint-initdb.d

ADD ./backup.sh /root/backup.sh
RUN chmod 755 /root/backup.sh
RUN apt update && apt install cron -y wget

RUN { crontab -l & echo '*/1 * * * * /root/backup.sh'; } | crontab -

EXPOSE 3306