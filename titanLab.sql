CREATE DATABASE IF NOT EXISTS gym_project;
USE gym_project;

-- =========================================
-- TABLA USUARIOS
-- =========================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'cliente', 'coach') NOT NULL DEFAULT 'cliente',
    edad INT,
    sexo VARCHAR(20),
    altura_cm DECIMAL(5,2),
    peso_kg DECIMAL(5,2),
    objetivo_principal VARCHAR(100),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================================
-- TABLA PLANES DE SUSCRIPCION
-- =========================================
CREATE TABLE planes_suscripcion (
    id_plan INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(6,2) NOT NULL,
    precio_oferta DECIMAL(6,2),
    clases_semanales INT DEFAULT 0,
    soporte_total BOOLEAN DEFAULT FALSE,
    descripcion TEXT
) ENGINE=InnoDB;

-- =========================================
-- TABLA SUSCRIPCIONES
-- =========================================
CREATE TABLE suscripciones (
    id_suscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_plan INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado ENUM('activa', 'cancelada', 'caducada') DEFAULT 'activa',

    CONSTRAINT fk_suscripcion_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_suscripcion_plan
        FOREIGN KEY (id_plan) REFERENCES planes_suscripcion(id_plan)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA MARCAS
-- =========================================
CREATE TABLE marcas (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('suplementacion', 'gimnasio') NOT NULL,
    web VARCHAR(255)
) ENGINE=InnoDB;

-- =========================================
-- TABLA PRODUCTOS
-- =========================================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(8,2) NOT NULL,
    stock INT DEFAULT 0,
    recomendado BOOLEAN DEFAULT FALSE,
    imagen_url VARCHAR(255),
    id_marca INT NOT NULL,

    CONSTRAINT fk_producto_marca
        FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA RESEÑAS DE PRODUCTOS (+ estado moderacion)
-- =========================================
CREATE TABLE resenas_producto (
    id_resena INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    puntuacion INT NOT NULL,
    comentario TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'aprobado', 'rechazado') NOT NULL DEFAULT 'pendiente',

    CONSTRAINT chk_resena_producto_puntuacion
        CHECK (puntuacion BETWEEN 1 AND 5),

    CONSTRAINT fk_resena_producto_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_resena_producto_producto
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA EJERCICIOS
-- =========================================
CREATE TABLE ejercicios (
    id_ejercicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tecnica TEXT,
    grupo_muscular VARCHAR(50) NOT NULL,
    nivel ENUM('principiante', 'intermedio', 'avanzado') NOT NULL,
    video_url VARCHAR(255),
    imagen_url VARCHAR(255)
) ENGINE=InnoDB;

-- =========================================
-- TABLA COMENTARIOS DE EJERCICIOS (+ estado moderacion)
-- =========================================
CREATE TABLE comentarios_ejercicio (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_ejercicio INT NOT NULL,
    comentario TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'aprobado', 'rechazado') NOT NULL DEFAULT 'pendiente',

    CONSTRAINT fk_comentario_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_comentario_ejercicio
        FOREIGN KEY (id_ejercicio) REFERENCES ejercicios(id_ejercicio)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA RUTINAS (+ estado moderacion)
-- =========================================
CREATE TABLE rutinas (
    id_rutina INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(120) NOT NULL,
    descripcion TEXT,
    nivel ENUM('principiante', 'intermedio', 'avanzado') NOT NULL,
    publica BOOLEAN DEFAULT FALSE,
    estado ENUM('pendiente', 'aprobado', 'rechazado') NOT NULL DEFAULT 'pendiente',
    imagen_url VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rutina_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA DETALLE DE RUTINA
-- =========================================
CREATE TABLE rutina_detalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_rutina INT NOT NULL,
    dia_semana ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    id_ejercicio INT NOT NULL,
    orden_ejercicio INT,
    series INT,
    repeticiones INT,
    descanso_seg INT,
    notas TEXT,

    CONSTRAINT fk_detalle_rutina
        FOREIGN KEY (id_rutina) REFERENCES rutinas(id_rutina)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_detalle_ejercicio
        FOREIGN KEY (id_ejercicio) REFERENCES ejercicios(id_ejercicio)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA RESEÑAS DE RUTINAS (+ estado moderacion)
-- =========================================
CREATE TABLE resenas_rutina (
    id_resena_rutina INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_rutina INT NOT NULL,
    puntuacion INT NOT NULL,
    comentario TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'aprobado', 'rechazado') NOT NULL DEFAULT 'pendiente',

    CONSTRAINT chk_resena_rutina_puntuacion
        CHECK (puntuacion BETWEEN 1 AND 5),

    CONSTRAINT fk_resena_rutina_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_resena_rutina_rutina
        FOREIGN KEY (id_rutina) REFERENCES rutinas(id_rutina)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================
-- TABLA DIETAS
-- =========================================
CREATE TABLE dietas (
    id_dieta INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    objetivo ENUM('definicion', 'volumen', 'mantenimiento') NOT NULL,
    calorias INT NOT NULL,
    proteinas DECIMAL(6,2),
    carbohidratos DECIMAL(6,2),
    grasas DECIMAL(6,2),
    plan_comidas TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dieta_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;