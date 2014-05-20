
CREATE TABLE wordfreq (
  id int(11)  NOT NULL UNIQUE,
  vocalized varchar(30)NOT NULL DEFAULT NULL,
  unvocalized varchar(30) NOT NULL DEFAULT NULL,
  word_type varchar(30) NOT NULL,  
  freq int(11)  NOT NULL DEFAULT 1,
  future_type varchar(6) NOT NULL
);