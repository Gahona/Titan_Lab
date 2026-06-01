-- =========================================
-- EJERCICIOS
-- =========================================
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

-- =========================================
-- USUARIO ADMIN
-- =========================================
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

-- =========================================
-- PLANES DE SUSCRIPCIÓN
-- =========================================
INSERT INTO planes_suscripcion (nombre, precio, precio_oferta, clases_semanales, soporte_total, descripcion) VALUES
('Coach Básico',   11.99, NULL,  2, FALSE, 'Acceso a rutinas básicas y seguimiento semanal con tu coach personal.'),
('Coach Premium',  22.99, 19.99, 5, TRUE,  'Acceso completo a todas las rutinas, dietas personalizadas y soporte total 24/7.');

-- =========================================
-- MARCAS
-- =========================================
INSERT INTO marcas (nombre, tipo, web) VALUES
('Io.Genix',    'suplementacion', 'https://www.iogenix.com'),
('Panatta',     'gimnasio',       'https://www.panatta.it'),
('PayPal',      'gimnasio',       'https://www.paypal.com');

-- =========================================
-- PRODUCTOS (suplementos del catálogo)
-- Los precios son orientativos, cámbialos si quieres
-- id_marca 1 = Io.Genix
-- =========================================
INSERT INTO productos (nombre, descripcion, categoria, precio, stock, recomendado, imagen_url, id_marca) VALUES
(
    'Proteína Whey',
    'Aumenta tu recuperación muscular y acelera tus resultados con proteína de alta calidad. Ideal para ganar masa muscular, mantener tus músculos y recuperarte después de entrenamientos intensos.',
    'proteina',
    34.99,
    100,
    TRUE,
    'proteina.jpg',
    1
),
(
    'Creatina Monohidrato',
    'Mejora tu fuerza, potencia y rendimiento en cada entrenamiento. La creatina es uno de los suplementos más eficaces para aumentar masa muscular y superar tus límites físicos.',
    'creatina',
    19.99,
    80,
    TRUE,
    'creatina.jpg',
    1
),
(
    'Pre-entreno',
    'Activa tu energía y concentración antes de entrenar. Consigue más intensidad, motivación y resistencia para rendir al máximo en cada sesión.',
    'pre-entreno',
    29.99,
    60,
    FALSE,
    'prewornk.jpg',
    1
),
(
    'BCAAs / EAAs',
    'Protege tu masa muscular y mejora la recuperación durante y después del entrenamiento. Perfectos para reducir la fatiga y mantener el rendimiento incluso en rutinas exigentes.',
    'aminoacidos',
    24.99,
    70,
    FALSE,
    'intrawork.jpg',
    1
),
(
    'Omega 3',
    'Cuida tu corazón, articulaciones y bienestar general con ácidos grasos esenciales. Un suplemento clave para mejorar la salud y favorecer una recuperación más eficiente.',
    'salud',
    14.99,
    90,
    FALSE,
    'omega3.jpg',
    1
),
(
    'Zinc / Magnesio',
    'Mejora tu descanso, recuperación muscular y niveles de energía. Una combinación perfecta para optimizar el rendimiento físico y apoyar tu sistema inmunológico.',
    'salud',
    12.99,
    90,
    FALSE,
    'zmzinc.jpg',
    1
);
