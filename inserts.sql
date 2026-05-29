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