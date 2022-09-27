TRUNCATE TABLE `ithome-jenkins-2022.ithome.content_info_latest`;
INSERT INTO `ithome-jenkins-2022.ithome.content_info_latest`
SELECT
  `_id`,
  `crawl_datetime`,
  `text`,
  `user_id`,
  `ironman_id`,
  `title`,
  `like`,
  `comment`,
  `view`,
  `article_id`,
  `article_url`,
  `create_datetime`
FROM `ithome-jenkins-2022.ithome.content_info_hist`
WHERE DATE(crawl_datetime) = @execute_date
;