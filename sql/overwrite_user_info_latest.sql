TRUNCATE TABLE `ithome-jenkins-2022.ithome.user_info_latest`;
INSERT INTO `ithome-jenkins-2022.ithome.user_info_latest`
SELECT
  `_id`,
  `crawl_datetime`,
  `user_id`,
  `user_name`,
  `ithome_level`,
  `ithome_point`,
  `user_viewed`,
  `user_followed`,
  `ask_question`,
  `article`,
  `answer`,
  `invitation_answer`,
  `best_answer`
FROM `ithome-jenkins-2022.ithome.user_info_hist`
WHERE DATE(crawl_datetime) = @execute_date
;