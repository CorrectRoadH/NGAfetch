CREATE TABLE IF NOT EXISTS `post`(
   `post_id` INT UNSIGNED NOT NULL,
   `time` DATE,
   `title` VARCHAR(100) NOT NULL,
   PRIMARY KEY ( `post_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `reply`(
   `post_id` INT UNSIGNED NOT NULL,
   `flood_num` INT UNSIGNED NOT NULL,
   `edit_count` INT UNSIGNED NOT NULL,
   `time` DATE,
   `title` VARCHAR(100) NOT NULL,
   PRIMARY KEY ( `post_id`,`flood_num`,`edit_count`  )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
