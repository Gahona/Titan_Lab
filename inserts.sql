Insertar ejercicios
  
INSERT INTO ejercicios (nombre, grupo_muscular, nivel) VALUES
('Press banca', 'Pecho', 'intermedio'),
('Press inclinado con mancuernas', 'Pecho', 'intermedio'),
('Aperturas en polea', 'Pecho', 'principiante'),

('Dominadas', 'Espalda', 'intermedio'),
('Remo con barra', 'Espalda', 'intermedio'),

('Sentadilla trasera', 'Pierna', 'principiante'),
('Peso muerto rumano', 'Pierna', 'intermedio'),
('Extension de cuadriceps', 'Pierna', 'intermedio'),

('Press militar', 'Hombro', 'intermedio'),
('Elevaciones laterales', 'Hombro', 'principiante'),
('Pájaros con mancuernas', 'Hombro', 'intermedio'),

('Curl convencional', 'Bíceps', 'principiante'),
('Curl martillo', 'Bíceps', 'principiante'),

('Press francés', 'Tríceps', 'intermedio'),
('Extensión en polea alta', 'Tríceps', 'principiante'),

('Rueda abdominal', 'Abdomen', 'avanzado'),
('Plancha', 'Abdomen', 'intermedio');


Insertar admin 
  
INSERT INTO usuarios (
    nombre,
    email,
    password_hash,
    rol,
    edad,
    sexo,
    altura_cm,
    peso_kg,
    objetivo_principal
) VALUES (
    'admin',
    'admin@admin.com',
    'scrypt:32768:8:1$3hAliRFJ9cgqzN5J$6e27f6a7e45624eec453f0fc4cb78e075fc960213407272a9f0adcf9716b22d09be275f317c162018ca7ffc52b6d40c11a8374e6341f19907cbf5a4f5766d2ab',
    'admin',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
);

INSERT INTO usuarios (
    nombre,
    email,
    password_hash,
    rol,
    edad,
    sexo,
    altura_cm,
    peso_kg,
    objetivo_principal
) VALUES (
    'jorge',
    'jorge@titan.com',
    'scrypt:32768:8:1$IJYYXQwG7XYspEzC$d89ccc1ec8110962c4bbfefc6ce8504d08db7e6dbabe370feadac0a40febda9bddd00bcefcf5a21d629307b965748a5d1feeff2f3185c5378107beab8ccc8aa4',
    'admin',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
);