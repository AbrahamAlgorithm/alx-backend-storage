-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    user_id INT
)
BEGIN
    DECLARE avg_cal_score FLOAT;
    SET avg_cal_score = (SELECT SUM(score * weight) / SUM(weight) 
                        FROM users AS U 
                        JOIN corrections as C ON U.id=C.user_id 
                        JOIN projects AS P ON C.project_id=P.id 
                        WHERE U.id=user_id);
    UPDATE users SET average_score = avg_cal_score WHERE id=user_id;
END
$$
DELIMITER ;
