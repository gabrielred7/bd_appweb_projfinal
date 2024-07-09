DROP TABLE IF EXISTS continente;

CREATE TABLE continente (
  Continente_Nome varchar(45) NOT NULL,
  Continente_Codigo varchar(45) DEFAULT NULL,
  PRIMARY KEY (Continente_Nome)
);

INSERT INTO continente VALUES 
  ('Africa','AF'),
  ('Antarctica','AN'),
  ('Asia','AS'),
  ('Europe','EU'),
  ('North America','valor padrão'),
  ('Oceania','OC'),
  ('South America','SA');