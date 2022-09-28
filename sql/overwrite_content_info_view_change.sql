TRUNCATE TABLE `ithome-jenkins-2022.ithome.content_info_view_change`;
INSERT INTO `ithome-jenkins-2022.ithome.content_info_view_change` (
    `ironman_id`,
    `article_id`,
    `view`,
    `crawl_datetime`,
    `latest_datetime`
)
SELECT
  `ironman_id`,
  `article_id`,
  `view`,
  `crawl_datetime`,
  CASE WHEN
      DATE(crawl_datetime) = @execute_date THEN true ELSE false
  END AS `latest_datetime`
FROM
  `ithome-jenkins-2022.ithome.content_info_hist`
WHERE DATE(crawl_datetime) <= @execute_date
;