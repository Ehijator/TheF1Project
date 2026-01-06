drop table if exists SessionsStaging;
drop table if exists RaceControlStaging;
drop table if exists OvertakeStaging;
drop table if exists PositionStaging;
drop table if exists WeatherStaging;
drop table if exists SessionResultStaging;
drop table if exists PitsStaging;
drop table if exists DriversStaging;
drop table if exists StintsStaging;
drop table if exists LapsStaging;

CREATE TABLE SessionsStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    Meeting_key int,
    session_key int,
    location TEXT,
    date_start timestamp,
    date_end timestamp ,
    session_type TEXT,
    session_name TEXT,
    country_key int,
    country_code int,
    country_name TEXT,
    circuit_key int,
    circuit_short_name TEXT,
    gmt_offset time,
    year int
);
CREATE TABLE RaceControlStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    Meeting_key int,
    session_key int,
    date timestamp,
    driver_number int,
    lap_number int,
    category TEXT,
    flag TEXT,
    scope TEXT,
    sector INT,
    message TEXT
);
CREATE TABLE OvertakeStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    Meeting_key int,
    session_key int,
    overtaking_driver_number int,
    overtaken_driver_number int,
    date timestamp,
    position int
);
CREATE TABLE PositionStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    date timestamp,
    session_key int,
    position int,
    meeting_key int,
    driver_number int
); 
CREATE TABLE WeatherStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    date timestamp,
    session_key int,
    wind_direction int,
    meeting_key int,
    wind_speed DOUBLE precision,
    rainfall int,
    track_temperature DOUBLE precision,
    air_temperature DOUBLE precision,
    humidity int,
    pressure DOUBLE precision
); 
CREATE TABLE SessionResultStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    position int,
    driver_number int,
    number_of_laps int,
    dnf TEXT,
    dns TEXT,
    dsq TEXT,
    duration DOUBLE precision,
    gap_to_leader DOUBLE precision,
    meeting_key int,
    session_key int,
    points INT
);
CREATE TABLE PitsStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    date TIMESTAMP,
    session_key int,
    driver_number int,
    meeting_key int,
    pit_duration DOUBLE precision,
    lap_number INT
);
CREATE TABLE DriversStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),    
    meeting_key int,
    session_key int,
    driver_number int,
    broadcast_name text,
    full_name text,
    name_acronym text,
    team_name text,
    team_colour text,
    first_name text,
    last_name text,
    headshot_url text,
    country_code TEXT
);
CREATE TABLE StintsStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_key int,
    session_key int,
    stint_number int,
    driver_number int,
    lap_start int,
    lap_end int,
    compound text,
    tyre_age_at_start int
);
CREATE TABLE LapsStaging(
    ID uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_key int,
    session_key int,
    driver_number int,
    lap_number int,
    date_start TIMESTAMP,
    duration_sector_1 DOUBLE precision,
    duration_sector_2 DOUBLE precision,
    duration_sector_3 DOUBLE precision,
    i1_speed int,
    i2_speed int,
    is_pit_out_lap bit,
    lap_duration DOUBLE precision,
    segments_sector_1 TEXT,
    segments_sector_2 TEXT,
    segments_sector_3 TEXT,
    st_speed INT
);


