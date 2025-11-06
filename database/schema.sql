-- ================================================================
-- DASHBOARD DE INDICADORES EDUCATIVOS - ESQUEMA POSTGRESQL
-- ================================================================
-- Sistema para Detección Temprana de Riesgo Académico
-- Django 5 + PostgreSQL + Plotly Dash
-- Universidad Autónoma Juan Misael Saracho (UAJMS)
-- ================================================================

-- Tabla: indicadores_grado
CREATE TABLE indicadores_grado (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla: indicadores_asignatura
CREATE TABLE indicadores_asignatura (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla: indicadores_periodoacademico
CREATE TABLE indicadores_periodoacademico (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BOOLEAN DEFAULT FALSE,
    UNIQUE(nombre, fecha_inicio)
);

-- Tabla: indicadores_profesor
CREATE TABLE indicadores_profesor (
    id BIGSERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    especialidad VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: indicadores_estudiante
CREATE TABLE indicadores_estudiante (
    id BIGSERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    ci VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(254),
    telefono VARCHAR(15),
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: indicadores_apoderado
CREATE TABLE indicadores_apoderado (
    id BIGSERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    ci VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(254),
    telefono VARCHAR(15) NOT NULL,
    direccion TEXT,
    parentesco VARCHAR(10) DEFAULT 'padre' CHECK (parentesco IN ('padre', 'madre', 'tutor', 'abuelo', 'hermano', 'tio', 'otro'))
);

-- Tabla: indicadores_curso
CREATE TABLE indicadores_curso (
    id BIGSERIAL PRIMARY KEY,
    grado_id BIGINT NOT NULL REFERENCES indicadores_grado(id) ON DELETE CASCADE,
    asignatura_id BIGINT NOT NULL REFERENCES indicadores_asignatura(id) ON DELETE CASCADE,
    profesor_id BIGINT NOT NULL REFERENCES indicadores_profesor(id) ON DELETE CASCADE,
    periodo_academico_id BIGINT NOT NULL REFERENCES indicadores_periodoacademico(id) ON DELETE CASCADE,
    seccion VARCHAR(10) DEFAULT 'A',
    UNIQUE(grado_id, asignatura_id, periodo_academico_id, seccion)
);

-- Tabla: indicadores_inscripcion
CREATE TABLE indicadores_inscripcion (
    id BIGSERIAL PRIMARY KEY,
    estudiante_id BIGINT NOT NULL REFERENCES indicadores_estudiante(id) ON DELETE CASCADE,
    curso_id BIGINT NOT NULL REFERENCES indicadores_curso(id) ON DELETE CASCADE,
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    activa BOOLEAN DEFAULT TRUE,
    UNIQUE(estudiante_id, curso_id)
);

-- Tabla: indicadores_estudianteapoderado
CREATE TABLE indicadores_estudianteapoderado (
    id BIGSERIAL PRIMARY KEY,
    estudiante_id BIGINT NOT NULL REFERENCES indicadores_estudiante(id) ON DELETE CASCADE,
    apoderado_id BIGINT NOT NULL REFERENCES indicadores_apoderado(id) ON DELETE CASCADE,
    es_principal BOOLEAN DEFAULT FALSE,
    fecha_asignacion DATE DEFAULT CURRENT_DATE,
    activa BOOLEAN DEFAULT TRUE,
    UNIQUE(estudiante_id, apoderado_id)
);

-- Tabla: indicadores_evaluacion
CREATE TABLE indicadores_evaluacion (
    id BIGSERIAL PRIMARY KEY,
    curso_id BIGINT NOT NULL REFERENCES indicadores_curso(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(15) DEFAULT 'examen' CHECK (tipo IN ('examen', 'tarea', 'proyecto', 'practica', 'participacion')),
    fecha DATE NOT NULL,
    ponderacion DECIMAL(5,2) NOT NULL CHECK (ponderacion >= 0.01 AND ponderacion <= 100.00)
);

-- Tabla: indicadores_calificacion
CREATE TABLE indicadores_calificacion (
    id BIGSERIAL PRIMARY KEY,
    evaluacion_id BIGINT NOT NULL REFERENCES indicadores_evaluacion(id) ON DELETE CASCADE,
    estudiante_id BIGINT NOT NULL REFERENCES indicadores_estudiante(id) ON DELETE CASCADE,
    nota DECIMAL(4,2) NOT NULL CHECK (nota >= 0.00 AND nota <= 100.00),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    UNIQUE(evaluacion_id, estudiante_id)
);

-- Tabla: indicadores_asistencia
CREATE TABLE indicadores_asistencia (
    id BIGSERIAL PRIMARY KEY,
    estudiante_id BIGINT NOT NULL REFERENCES indicadores_estudiante(id) ON DELETE CASCADE,
    curso_id BIGINT NOT NULL REFERENCES indicadores_curso(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    estado VARCHAR(12) DEFAULT 'presente' CHECK (estado IN ('presente', 'ausente', 'tardanza', 'justificada')),
    observaciones TEXT,
    UNIQUE(estudiante_id, curso_id, fecha)
);

-- ================================================================
-- ÍNDICES PARA OPTIMIZACIÓN DE CONSULTAS KPI
-- ================================================================

-- Índices para reportes de rendimiento académico
CREATE INDEX idx_calificacion_estudiante_fecha ON indicadores_calificacion(estudiante_id, fecha_registro);
CREATE INDEX idx_calificacion_curso_evaluacion ON indicadores_calificacion(evaluacion_id);
CREATE INDEX idx_evaluacion_curso_fecha ON indicadores_evaluacion(curso_id, fecha);

-- Índices para análisis de asistencia
CREATE INDEX idx_asistencia_estudiante_fecha ON indicadores_asistencia(estudiante_id, fecha);
CREATE INDEX idx_asistencia_curso_fecha ON indicadores_asistencia(curso_id, fecha);
CREATE INDEX idx_asistencia_estado ON indicadores_asistencia(estado, fecha);

-- Índices para consultas de cursos
CREATE INDEX idx_curso_periodo_grado ON indicadores_curso(periodo_academico_id, grado_id);
CREATE INDEX idx_inscripcion_activa ON indicadores_inscripcion(activa, curso_id);

-- ================================================================
-- VISTAS PARA KPIs PRINCIPALES
-- ================================================================

-- Vista: Promedio de notas por curso
CREATE VIEW vista_promedio_por_curso AS
SELECT 
    c.id as curso_id,
    g.nombre as grado,
    a.nombre as asignatura,
    p.nombre as periodo,
    prof.nombres || ' ' || prof.apellidos as profesor,
    ROUND(AVG(cal.nota), 2) as promedio_curso,
    COUNT(DISTINCT cal.estudiante_id) as total_estudiantes
FROM indicadores_curso c
JOIN indicadores_grado g ON c.grado_id = g.id
JOIN indicadores_asignatura a ON c.asignatura_id = a.id
JOIN indicadores_periodoacademico p ON c.periodo_academico_id = p.id
JOIN indicadores_profesor prof ON c.profesor_id = prof.id
JOIN indicadores_evaluacion e ON e.curso_id = c.id
JOIN indicadores_calificacion cal ON cal.evaluacion_id = e.id
GROUP BY c.id, g.nombre, a.nombre, p.nombre, prof.nombres, prof.apellidos;

-- Vista: Tasa de ausentismo por estudiante
CREATE VIEW vista_ausentismo_estudiante AS
SELECT 
    e.id as estudiante_id,
    e.nombres || ' ' || e.apellidos as estudiante,
    c.id as curso_id,
    g.nombre as grado,
    a.nombre as asignatura,
    COUNT(*) as total_registros,
    COUNT(CASE WHEN ast.estado = 'ausente' THEN 1 END) as ausencias,
    COUNT(CASE WHEN ast.estado = 'tardanza' THEN 1 END) as tardanzas,
    ROUND(
        (COUNT(CASE WHEN ast.estado IN ('ausente', 'tardanza') THEN 1 END) * 100.0) / 
        COUNT(*), 2
    ) as porcentaje_ausentismo
FROM indicadores_estudiante e
JOIN indicadores_inscripcion i ON i.estudiante_id = e.id
JOIN indicadores_curso c ON i.curso_id = c.id
JOIN indicadores_grado g ON c.grado_id = g.id
JOIN indicadores_asignatura a ON c.asignatura_id = a.id
JOIN indicadores_asistencia ast ON ast.estudiante_id = e.id AND ast.curso_id = c.id
WHERE i.activa = true
GROUP BY e.id, e.nombres, e.apellidos, c.id, g.nombre, a.nombre;

-- Vista: Estudiantes en riesgo académico
CREATE VIEW vista_estudiantes_riesgo AS
SELECT DISTINCT
    e.id as estudiante_id,
    e.nombres || ' ' || e.apellidos as estudiante,
    e.ci,
    ROUND(AVG(cal.nota), 2) as promedio_general,
    ROUND(AVG(
        CASE WHEN ast.estado IN ('ausente', 'tardanza') 
        THEN 1.0 ELSE 0.0 END
    ) * 100, 2) as porcentaje_ausentismo,
    CASE 
        WHEN AVG(cal.nota) < 60 AND 
             AVG(CASE WHEN ast.estado IN ('ausente', 'tardanza') THEN 1.0 ELSE 0.0 END) > 0.20
        THEN 'RIESGO ALTO'
        WHEN AVG(cal.nota) < 70 OR 
             AVG(CASE WHEN ast.estado IN ('ausente', 'tardanza') THEN 1.0 ELSE 0.0 END) > 0.15
        THEN 'RIESGO MEDIO'
        ELSE 'NORMAL'
    END as nivel_riesgo
FROM indicadores_estudiante e
JOIN indicadores_inscripcion i ON i.estudiante_id = e.id AND i.activa = true
JOIN indicadores_curso c ON i.curso_id = c.id
JOIN indicadores_evaluacion ev ON ev.curso_id = c.id
JOIN indicadores_calificacion cal ON cal.evaluacion_id = ev.id AND cal.estudiante_id = e.id
LEFT JOIN indicadores_asistencia ast ON ast.estudiante_id = e.id AND ast.curso_id = c.id
WHERE e.activo = true
GROUP BY e.id, e.nombres, e.apellidos, e.ci
HAVING COUNT(cal.nota) >= 3; -- Al menos 3 calificaciones

-- ================================================================
-- DATOS DE EJEMPLO (OPCIONAL - SOLO PARA DESARROLLO)
-- ================================================================

-- Grados
INSERT INTO indicadores_grado (nombre, descripcion) VALUES 
('1° Primaria', 'Primer grado de educación primaria'),
('2° Primaria', 'Segundo grado de educación primaria'),
('1° Secundaria', 'Primer año de educación secundaria'),
('2° Secundaria', 'Segundo año de educación secundaria');

-- Asignaturas
INSERT INTO indicadores_asignatura (codigo, nombre, descripcion) VALUES 
('MAT', 'Matemáticas', 'Matemáticas básicas y avanzadas'),
('LEN', 'Lenguaje', 'Lengua y Literatura'),
('CIE', 'Ciencias', 'Ciencias Naturales'),
('SOC', 'Sociales', 'Estudios Sociales');

-- Período Académico Actual
INSERT INTO indicadores_periodoacademico (nombre, fecha_inicio, fecha_fin, activo) VALUES 
('Primer Semestre 2024', '2024-02-01', '2024-06-30', true);

COMMIT;

-- ================================================================
-- FIN DEL ESQUEMA
-- ================================================================