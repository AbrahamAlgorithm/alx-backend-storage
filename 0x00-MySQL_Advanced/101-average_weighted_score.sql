--  SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS U, 
        (SELECT U.id, SUM(score * weight) / SUM(weight) AS w_avg 
        FROM users AS U 
        JOIN corrections as C ON U.id=C.user_id 
        JOIN projects AS P ON C.project_id=P.id 
        GROUP BY U.id)
    AS WAT
    SET U.average_score = WAT.w_avg 
    WHERE U.id=WAT.id;
END
$$
DELIMITER ;
