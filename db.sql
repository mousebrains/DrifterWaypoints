--
-- Define database for Nilza's drifter project
--

DROP TABLE IF EXISTS gliderPos;
CREATE TABLE gliderPos ( -- Where glider's dialog data is stored
	name TEXT, -- Glider's name
	t DATETIME DEFAULT NULL, -- current time + GPS Location: secs ago
	lat REAL DEFAULT NULL, -- GPS Location: latitude
	lon REAL DEFAULT NULL, -- GPS Location: longitude
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS gliderSpeed;
CREATE TABLE gliderSpeed( -- How fast the glider is moving through the water
	name TEXT, -- Glider's name
	t DATETIME, -- timestamp
	speed REAL DEFAULT NULL, -- m_avg_speed (m/sec)
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS gliderVX;
CREATE TABLE gliderVX( -- m_final_water_vx
	name TEXT, -- Glider's name
	t DATETIME, -- When observed
	v REAL DEFAULT NULL, -- m_final_water_vx (m/sec)
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS gliderVY;
CREATE TABLE gliderVY( -- m_final_water_vy
	name TEXT, -- Glider's name
	t DATETIME, -- When observed
	v REAL DEFAULT NULL, -- m_final_water_vy (m/sec)
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS gliderWptLat;
CREATE TABLE gliderWptLat( -- x_last_wpt_lat
	name TEXT, -- Glider's name
	t DATETIME, -- When observed
	val REAL DEFAULT NULL, -- x_last_wpt_lat
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS gliderWptLon;
CREATE TABLE gliderWptLon( -- x_last_wpt_lon
	name TEXT, -- Glider's name
	t DATETIME, -- When observed
	val REAL DEFAULT NULL, -- x_last_wpt_lon
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS gliderComplete;
CREATE TABLE gliderComplete( -- Water Velocity Ccalculations COMPLETE seen
	name TEXT, -- Glider's name
	t DATETIME, -- When observed
	PRIMARY KEY(t, name) -- One observation per glider
);

DROP TABLE IF EXISTS drifter;
CREATE TABLE drifter ( -- Drifter's fixes
	tObs DATETIME PRIMARY KEY, -- GPS fix time
	tRecv DATETIME, -- When fix was received
	lat REAL, -- latitude
	lon REAL -- longitude
);

DROP TABLE IF EXISTS waypoints;
CREATE TABLE waypoints ( -- Generated glider waypoints
	tGen DATETIME PRIMARY KEY, -- When waypoint was generated
	cnt INT, -- waypoint ordering index
	lat REAL, -- latitude
	lon REAL, -- longitude
	tArrive DATETIME, -- When the glider should arrive here
	UNIQUE (tGen, cnt)
);
