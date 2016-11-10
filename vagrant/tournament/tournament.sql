-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (id SERIAL primary key, name TEXT);

create table matches (id SERIAL primary key, winner INTEGER REFERENCES players (id), loser INTEGER REFERENCES players(id));
