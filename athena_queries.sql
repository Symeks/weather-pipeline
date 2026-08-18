-- Alle Daten anzeigen
SELECT * FROM weather.forecast LIMIT 10;

-- Durchschnittstemperatur pro Tag
SELECT date, ROUND(AVG(temperature_c), 1) AS avg_temp
FROM weather.forecast
GROUP BY date
ORDER BY date;

-- Wann regnet es?
SELECT timestamp, temperature_c, precipitation_mm
FROM weather.forecast
WHERE is_raining = true
ORDER BY timestamp