SELECT
  PickerIds,
  AVG(PickwalkDurationInSeconds) AS avrg_pw_duration,
  AVG(PicksDurationInSeconds) AS avrg_p_duration,
  AVG(IdleTimeInSeconds) AS avrg_idle_duration
FROM
  [{{project}}:mock_pick_action.pickwalk_dataObject_{{scheduledDate | adddays(dt) | dateformat("%Y%m%d")}}]
GROUP BY
  PickerIds
ORDER BY
  avrg_pw_duration DESC

