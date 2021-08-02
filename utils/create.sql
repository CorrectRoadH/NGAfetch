CREATE TABLE IF NOT EXISTS `post`(
   `post_id` INT UNSIGNED NOT NULL,
   `time` DATETIME,
   `title` VARCHAR(100) NOT NULL,
   `state` INT,
   PRIMARY KEY ( `post_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `reply`(
   `post_id` INT UNSIGNED NOT NULL,
   `flood_num` INT UNSIGNED NOT NULL,
   `edit_count` INT UNSIGNED NOT NULL,
   `time` DATETIME,
   `context` TEXT NOT NULL,
   `author` VARCHAR(10),
   PRIMARY KEY ( `post_id`,`flood_num`,`edit_count`  )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user`(
   `username` VARCHAR(10),
   `uid` VARCHAR(10),
   `level` INT,
   `registerDate` Date,
   PRIMARY KEY ( `uid`  )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
