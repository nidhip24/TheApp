CREATE TABLE IF NOT EXISTS users (
	id serial4 PRIMARY KEY,
	"name" varchar NULL,
	email varchar NULL,
	created_at timestamp NULL
);

INSERT INTO users ( "name", email, created_at)
VALUES('nidhip', 'nidhipk@gmail.com', CURRENT_TIMESTAMP);