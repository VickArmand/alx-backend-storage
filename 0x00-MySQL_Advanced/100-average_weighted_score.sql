-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

-- Requirements:
-- Procedure is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    UPDATE users SET average_score = getAverageWeight(user_id) WHERE id=user_id;
END;
CREATE FUNCTION getAverageWeight(user_id INT)
RETURNS INT
BEGIN
    SET @sum_weight = (SELECT SUM(weight) FROM projects);
    SET @wp = (SELECT SUM(weight * score) FROM corrections c JOIN projects p ON p.id = c.project_id WHERE c.user_id = user_id);
    RETURN (@wp / @sum_weight);
END;$$
