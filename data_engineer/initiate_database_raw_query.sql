-- CREATE DATABASE nerpcgaming;

BEGIN;

CREATE TABLE discussion(
	question VARCHAR(1000)
);

CREATE TABLE kata_tag_dict(
	sentence VARCHAR(1000),
	kata VARCHAR(100),
	tag VARCHAR(50)
);

-- THis can only be run in PSQL Tool
-- \COPY kata_tag_dict FROM '/Users/nyomanyudis/Desktop/hactiv8/web scraping/NER_PC_GAMING/dataset/DatasetWithTagFinal.csv' DELIMITER ',' CSV HEADER;
-- \COPY discussion FROM '/Users/nyomanyudis/Desktop/hactiv8/web scraping/NER_PC_GAMING/dataset/question.csv' DELIMITER ',' CSV HEADER;

END;
