Create table If Not Exists Teams (team_id int, team_name varchar(20))
Create table If Not Exists Matches (home_team_id int, away_team_id int, home_team_goals int, away_team_goals int)
Truncate table Teams
insert into Teams (team_id, team_name) values ('1', 'Ajax')
insert into Teams (team_id, team_name) values ('4', 'Dortmund')
insert into Teams (team_id, team_name) values ('6', 'Arsenal')
Truncate table Matches
insert into Matches (home_team_id, away_team_id, home_team_goals, away_team_goals) values ('1', '4', '0', '1')
insert into Matches (home_team_id, away_team_id, home_team_goals, away_team_goals) values ('1', '6', '3', '3')
insert into Matches (home_team_id, away_team_id, home_team_goals, away_team_goals) values ('4', '1', '5', '2')
insert into Matches (home_team_id, away_team_id, home_team_goals, away_team_goals) values ('6', '1', '0', '0')