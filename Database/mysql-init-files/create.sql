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
    vote INT(10),
    unlike INT(10),
    commentcount INT(10),
    writer CHAR(20),
    isAnony BOOLEAN NOT NULL DEFAULT 1,
    isDel BOOLEAN NOT NULL DEFAULT 0,
    isEdit BOOLEAN,
    fileCount INT(10) DEFAULT 0,
    imageCount INT(10) DEFAULT 0,
    thumbnail VARCHAR(100) NOT NULL DEFAULT '',
    password VARCHAR(32) NOT NULL,
    FOREIGN KEY (boardID) REFERENCES Board (boardID)
);

CREATE TABLE Comment (
    articleID INT(10) NOT NULL,
    commentID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    content VARCHAR(2000) NOT NULL,
    timeStamp TIMESTAMP DEFAULT now(),
    parentCID INT(10),
    vote INT(10),
    unlike INT(10),
    writer CHAR(20),
    isAnony BOOLEAN NOT NULL DEFAULT 1,
    isReply BOOLEAN DEFAULT 0,
    isDel BOOLEAN NOT NULL DEFAULT 0,
    isVisible BOOLEAN NOT NULL DEFAULT 1,
    password VARCHAR(32),
    FOREIGN KEY (articleID) REFERENCES Article (articleID)
);

CREATE TABLE LikeLog (
    articleID INT(10) DEFAULT 0,
    commentID INT(10) DEFAULT 0,
    likeID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    isUnlike BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (commentID) REFERENCES Comment (commentID),
    FOREIGN KEY (articleID) REFERENCES Article (articleID)
);

CREATE TABLE File (
    articleID INT(10) DEFAULT 0,
    fID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    file VARCHAR(100) NOT NULL,
    uuid VARCHAR(32),
    filename VARCHAR(50) NOT NULL,
    filesize BIGINT NOT NULL,
    timeStamp TIMESTAMP DEFAULT now(),
    isDel BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (articleID) REFERENCES Article (articleID)
);

CREATE TABLE Image (
    articleID INT(10) DEFAULT 0,
    imgID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    file VARCHAR(100) NOT NULL,
    uuid VARCHAR(32),
    filename VARCHAR(50) NOT NULL,
    filesize BIGINT NOT NULL,
    timeStamp TIMESTAMP DEFAULT now(),
    isDel BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (articleID) REFERENCES Article (articleID)
);