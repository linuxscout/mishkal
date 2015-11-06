create table verbs
			(
			id int unique not null,
			vocalized varchar(30) not null,
			unvocalized varchar(30) not null,
			root varchar(30),
			normalized varchar(30) not null,
			stamped varchar(30) not null,
			future_type varchar(5),
			triliteral  varchar(2) NOT NULL default 'y', 
			transitive  varchar(2) NOT NULL default 'y', 
			double_trans  varchar(2) NOT NULL default 'y', 
			think_trans  varchar(2) NOT NULL default 'y', 
			unthink_trans  varchar(2) NOT NULL default 'y', 
			reflexive_trans  varchar(2) NOT NULL default 'y', 
			past  varchar(2) NOT NULL default 'y', 
			future  varchar(2) NOT NULL default 'y',  
			imperative  varchar(2) NOT NULL default 'y', 
			passive  varchar(2) NOT NULL default 'y',  
			future_moode  varchar(2) NOT NULL default 'y', 
			confirmed  varchar(2) NOT NULL default 'y', 
			PRIMARY KEY (id)
			);