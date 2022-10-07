CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	firstname TEXT,
 	lastname TEXT,
	password TEXT,
	username TEXT UNIQUE,
	isteacher BOOLEAN
);

CREATE TABLE courses (
	id SERIAL PRIMARY KEY,
	coursename TEXT UNIQUE,
	teacher_id INTEGER REFERENCES users,
	description TEXT
);

CREATE TABLE participants (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses ON DELETE CASCADE,
	user_id INTEGER REFERENCES users	
);

CREATE TABLE tasks (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses ON DELETE CASCADE,
	question TEXT,
	correctanswer TEXT,
	maxpoints INTEGER,
	max_tries INTEGER,
	week INTEGER
);

CREATE TABLE submissions (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses ON DELETE CASCADE,
	user_id INTEGER REFERENCES users,
	task_id INTEGER REFERENCES tasks,
	tries INTEGER,
	points INTEGER
);

CREATE TABLE texts (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses ON DELETE CASCADE,
	content TEXT,
	week INTEGER
);

CREATE TABLE choices (
	id SERIAL PRIMARY KEY,
	task_id INTEGER REFERENCES tasks,
	choice TEXT,
	course_id INTEGER REFERENCES courses ON DELETE CASCADE
);
