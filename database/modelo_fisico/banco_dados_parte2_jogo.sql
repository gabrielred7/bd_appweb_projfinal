
DROP TABLE IF EXISTS jogo;

CREATE TABLE jogo (
  Titulo varchar(45) NOT NULL,
  Genero varchar(45) DEFAULT NULL,
  PRIMARY KEY (Titulo)
);

INSERT INTO jogo (Titulo, Genero) VALUES 
('Arena of Valor','Multiplayer Online Battle Arena'),
('Counter-Strike: Global Offensive','First-Person Shooter'),
('Dota 2','Multiplayer Online Battle Arena'),
('Fortnite','Battle Royale'),
('Hearthstone','Collectible Card Game'),
('Heroes of the Storm','Multiplayer Online Battle Arena'),
('League of Legends','Multiplayer Online Battle Arena'),
('Overwatch','First-Person Shooter'),
('PUBG','Battle Royale'),
('Starcraft II','Strategy');