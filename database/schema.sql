-- =====================================================
-- DDL para PostgreSQL - Dashboard Indicadores Educativos
-- Base de datos normalizada en Tercera Forma Normal (3NF)
-- =====================================================

-- --- 1. Tablas Fundamentales (Dimensiones) ---

CREATE TABLE Grados (
    id_grado SERIAL PRIMARY KEY,
    nombre_grado VARCHAR(100) NOT NULL UNIQUE,
    nivel_educativo VARCHAR(50) NOT NULL
);

CREATE TABLE Asignaturas (
    id_asignatura SERIAL PRIMARY KEY,
    nombre_asignatura VARCHAR(150) NOT NULL,
    codigo_asignatura VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE Periodos_Academicos (
    id_periodo SERIAL PRIMARY KEY,
    ano_academico INT NOT NULL,
    nombre_periodo VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

CREATE TABLE Profesores (
    id_profesor SERIAL PRIMARY KEY,
    rut VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    email_institucional VARCHAR(255) NOT NULL UNIQUE,
    especialidad VARCHAR(100),
    estado VARCHAR(20) NOT NULL DEFAULT 'Activo'
);

CREATE TABLE Estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    rut VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(20),
    fecha_ingreso DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'Activo'
);

CREATE TABLE Apoderados (
    id_apoderado SERIAL PRIMARY KEY,
    rut VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(20)
);

-- --- 2. Tablas de Unión y Contexto ---

CREATE TABLE Cursos (
    id_curso SERIAL PRIMARY KEY,
    id_profesor INTEGER NOT NULL REFERENCES Profesores(id_profesor) ON DELETE RESTRICT,
    id_asignatura INTEGER NOT NULL REFERENCES Asignaturas(id_asignatura) ON DELETE RESTRICT,
    id_grado INTEGER NOT NULL REFERENCES Grados(id_grado) ON DELETE RESTRICT,
    id_periodo INTEGER NOT NULL REFERENCES Periodos_Academicos(id_periodo) ON DELETE RESTRICT,
    UNIQUE (id_profesor, id_asignatura, id_grado, id_periodo)
);

CREATE TABLE Inscripciones (
    id_inscripcion SERIAL PRIMARY KEY,
    id_estudiante INTEGER NOT NULL REFERENCES Estudiantes(id_estudiante) ON DELETE CASCADE,
    id_curso INTEGER NOT NULL REFERENCES Cursos(id_curso) ON DELETE CASCADE,
    UNIQUE (id_estudiante, id_curso)
);

CREATE TABLE Estudiantes_Apoderados (
    id_estudiante INTEGER NOT NULL REFERENCES Estudiantes(id_estudiante) ON DELETE CASCADE,
    id_apoderado INTEGER NOT NULL REFERENCES Apoderados(id_apoderado) ON DELETE CASCADE,
    relacion VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_estudiante, id_apoderado)
);

-- --- 3. Tablas de Hechos ---

CREATE TABLE Evaluaciones (
    id_evaluacion SERIAL PRIMARY KEY,
    id_curso INTEGER NOT NULL REFERENCES Cursos(id_curso) ON DELETE CASCADE,
    nombre_evaluacion VARCHAR(200) NOT NULL,
    tipo_evaluacion VARCHAR(50),
    fecha_evaluacion DATE NOT NULL,
    ponderacion DECIMAL(5,2) NOT NULL -- Ponderación como porcentaje (ej: 0.25)
);

CREATE TABLE Calificaciones (
    id_calificacion SERIAL PRIMARY KEY,
    id_evaluacion INTEGER NOT NULL REFERENCES Evaluaciones(id_evaluacion) ON DELETE CASCADE,
    id_inscripcion INTEGER NOT NULL REFERENCES Inscripciones(id_inscripcion) ON DELETE CASCADE,
    nota_obtenida DECIMAL(4,2) NOT NULL,
    fecha_registro TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Asistencia (
    id_asistencia SERIAL PRIMARY KEY,
    id_inscripcion INTEGER NOT NULL REFERENCES Inscripciones(id_inscripcion) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    estado_asistencia VARCHAR(30) NOT NULL, -- 'Presente', 'Ausente Injustificado', etc.
    UNIQUE (id_inscripcion, fecha)
);

-- =====================================================
-- Comentarios y Documentación
-- =====================================================

COMMENT ON TABLE Grados IS 'Tabla de grados académicos (Primero A, Segundo B, etc.)';
COMMENT ON TABLE Asignaturas IS 'Materias académicas con códigos únicos';
COMMENT ON TABLE Periodos_Academicos IS 'Períodos escolares (semestres, trimestres)';
COMMENT ON TABLE Profesores IS 'Docentes del sistema educativo';
COMMENT ON TABLE Estudiantes IS 'Alumnos matriculados en el sistema';
COMMENT ON TABLE Apoderados IS 'Tutores y contactos de emergencia';

COMMENT ON TABLE Cursos IS 'Tabla de contexto: une profesor, asignatura, grado y período';
COMMENT ON TABLE Inscripciones IS 'Matrícula de estudiantes en cursos específicos';
COMMENT ON TABLE Estudiantes_Apoderados IS 'Relación muchos a muchos estudiante-apoderado';

COMMENT ON TABLE Evaluaciones IS 'Pruebas, tareas y evaluaciones con ponderación';
COMMENT ON TABLE Calificaciones IS 'Notas obtenidas por cada estudiante en evaluaciones';
COMMENT ON TABLE Asistencia IS 'Registro diario de asistencia por estudiante y curso';

-- =====================================================
-- Índices para Optimización (Opcional)
-- =====================================================

-- Índices para búsquedas frecuentes en KPIs
CREATE INDEX idx_calificaciones_inscripcion ON Calificaciones(id_inscripcion);
CREATE INDEX idx_calificaciones_evaluacion ON Calificaciones(id_evaluacion);
CREATE INDEX idx_asistencia_inscripcion ON Asistencia(id_inscripcion);
CREATE INDEX idx_asistencia_fecha ON Asistencia(fecha);
CREATE INDEX idx_cursos_periodo ON Cursos(id_periodo);

-- =====================================================
-- Fin del DDL
-- =====================================================