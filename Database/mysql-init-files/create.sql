CREATE USER 'ggulbob'@'localhost' IDENTIFIED WITH mysql_native_password BY 'ggulbobpasswd';
CREATE USER 'ggulbob'@'%' IDENTIFIED WITH mysql_native_password BY 'ggulbobpasswd';

GRANT ALL PRIVILEGES ON bobrytime.* to 'ggulbob'@'localhost';
GRANT ALL PRIVILEGES ON * . * TO 'ggulbob'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE TABLE Board (
    boardName char(20) NOT NULL,
    boardID int(10) NOT NULL PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE Article (
    boardID INT(10) NOT NULL,
    articleID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title CHAR(20) NOT NULL,
    content VARCHAR(2000) NOT NULL,
    timeStamp TIMESTAMP DEFAULT now(),
    isEdit BOOLEAN,
    vote INT(10) ,
    unlike INT(10),
    isAnony BOOLEAN NOT NULL DEFAULT 1,
    writer CHAR(20),
    password VARCHAR(32),
    isDel BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (boardID) REFERENCES Board (boardID)
);

CREATE TABLE Comment (
    articleID INT(10) NOT NULL,
    commentID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    content VARCHAR(2000) NOT NULL,
    timeStamp TIMESTAMP DEFAULT now(),
    writer CHAR(20),
    isReply BOOLEAN,
    parentCID INT(10),
    isAnony BOOLEAN NOT NULL DEFAULT 1,
    password VARCHAR(32),
    vote INT(10),
    isDel BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (articleID) REFERENCES Article (articleID)
);