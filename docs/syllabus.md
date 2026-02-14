# Syllabus - Minería de Datos

**Curso**: Minería de Datos  
**Nivel**: Grado/Máster  
**Duración**: 12 semanas  
**Modalidad**: Presencial + Práctica

## Descripción del Curso

Este curso enseña el proceso completo de **Knowledge Discovery in Databases (KDD)** y técnicas de **Data Mining** mediante un proyecto práctico que implementa una arquitectura moderna de **Lakehouse**.

Los estudiantes trabajarán en equipos para construir un pipeline de analytics completo desde datos crudos hasta modelos de Machine Learning desplegables, usando herramientas industriales (PySpark, scikit-learn, Git, CI/CD).

## Objetivos de Aprendizaje

Al finalizar el curso, los estudiantes serán capaces de:

1. **Comprender** el proceso KDD y su aplicación en problemas reales
2. **Diseñar** arquitecturas de datos escalables (Lakehouse)
3. **Implementar** pipelines ETL con PySpark y validación de calidad
4. **Construir** features para Machine Learning
5. **Entrenar** y evaluar modelos de clasificación, regresión y clustering
6. **Aplicar** buenas prácticas de ingeniería de software (testing, CI/CD, documentación)
7. **Comunicar** resultados técnicos y recomendaciones de negocio

## Metodología

- **Proyecto en equipo** (3-4 estudiantes)
- **Cada equipo** genera datos únicos (misma estructura, diferentes parámetros)
- **Checkpoints semanales** con entregas incrementales
- **Code reviews** y feedback continuo
- **Presentación final** de resultados

## Estructura del Curso

### Semana 1-2: Fundamentos y Setup

**Temas**:
- Introducción al KDD y Data Mining
- Arquitecturas de datos: Data Lake vs Data Warehouse vs Lakehouse
- Introducción a PySpark y Parquet
- Control de versiones con Git

**Práctica**:
- Setup del entorno de desarrollo
- Fork del repositorio del curso
- Configuración del equipo (team config)
- Ejecución del pipeline completo (`make all`)

**Entregable**: 
- Repositorio configurado
- Pipeline ejecutado exitosamente
- README con nombres de equipo

---

### Semana 3: Capa Bronze - Generación de Datos

**Temas**:
- Proceso de simulación de datos
- Reproducibilidad en ciencia de datos
- Schemas y validación de tipos
- Particionado de datos (run_date)

**Práctica**:
- Análisis del generador de datos
- Exploración de tablas Bronze
- Verificación de reproducibilidad (mismo seed = mismos datos)
- Análisis exploratorio con PySpark

**Entregable**:
- Notebook con análisis exploratorio de Bronze
- Verificación de reproducibilidad (test)
- Documentación de esquemas de datos

---

### Semana 4: Capa Silver - Limpieza y Calidad

**Temas**:
- Data quality frameworks
- Validación de integridad referencial
- Deduplicación y normalización
- Manejo de valores nulos y outliers

**Práctica**:
- Implementación de reglas de calidad personalizadas
- Bronze → Silver pipeline
- Testing de validaciones
- Documentación de decisiones de limpieza

**Entregable**:
- Pipeline Bronze→Silver funcionando
- Reporte de calidad de datos
- Tests de calidad (pytest)

---

### Semana 5: Capa Gold - Agregaciones y Features

**Temas**:
- Feature engineering para ML
- Agregaciones temporales (ventanas 7d, 30d)
- Fact tables y dimensional modeling
- KPIs de negocio

**Práctica**:
- Silver → Gold pipeline
- Construcción de fact tables
- Features para churn/LTV/segmentación
- Análisis de KPIs

**Entregable**:
- Pipeline Silver→Gold funcionando
- Tablas Gold documentadas
- Dashboard con KPIs principales

---

### Semana 6-7: Modelos de Clasificación - Churn Prediction

**Temas**:
- Problema de churn
- Feature selection
- Random Forest para clasificación
- Métricas: Accuracy, Precision, Recall, F1, ROC AUC
- Matriz de confusión

**Práctica**:
- Entrenamiento de modelo de churn
- Análisis de feature importance
- Tuning de hiperparámetros
- Validación cruzada

**Entregable**:
- Modelo de churn entrenado
- Análisis de feature importance
- Reporte de métricas
- Recomendaciones de negocio

---

### Semana 8: Modelos de Regresión - LTV Prediction

**Temas**:
- Lifetime Value (LTV)
- Regresión con Random Forest
- Métricas: MAE, RMSE, R²
- Interpretación de errores

**Práctica**:
- Entrenamiento de modelo de LTV
- Análisis de predicciones vs reales
- Segmentación por LTV predicho
- Estrategias de pricing/retención

**Entregable**:
- Modelo de LTV entrenado
- Análisis de errores
- Segmentación por valor
- Business case

---

### Semana 9: Clustering - User Segmentation

**Temas**:
- Clustering con K-Means
- Elección del número de clusters
- Métricas: Silhouette, Calinski-Harabasz
- Interpretación de segmentos

**Práctica**:
- Entrenamiento de modelo de segmentación
- Perfilado de segmentos
- Estrategias personalizadas por segmento
- Visualización de clusters

**Entregable**:
- Modelo de segmentación entrenado
- Perfiles de segmentos
- Estrategias de marketing por segmento
- Visualizaciones

---

### Semana 10: Evaluación y Optimización

**Temas**:
- Model evaluation best practices
- A/B testing concepts
- Model monitoring
- Retraining strategies

**Práctica**:
- Comparación de modelos entre equipos
- Análisis de sensibilidad a parámetros
- Optimización de features
- Documentación técnica completa

**Entregable**:
- Reporte de evaluación completo
- Comparación con otros equipos
- Plan de monitoreo de modelos

---

### Semana 11: Testing y CI/CD

**Temas**:
- Testing en pipelines de datos
- GitHub Actions
- Code quality (linting, formatting)
- Documentación técnica

**Práctica**:
- Implementación de tests completos
- Setup de CI/CD pipeline
- Code review entre equipos
- Mejora de documentación

**Entregable**:
- Suite de tests completa (pytest)
- CI/CD funcionando (GitHub Actions)
- Documentación técnica
- Code review de otro equipo

---

### Semana 12: Presentación Final

**Formato**:
- Presentación de 20 minutos + 10 minutos Q&A
- Demo en vivo del pipeline
- Resultados de negocio

**Contenido requerido**:
1. Descripción del problema de negocio
2. Arquitectura implementada
3. Resultados de cada modelo
4. Insights y recomendaciones
5. Lecciones aprendidas
6. Próximos pasos

**Entregable**:
- Presentación (slides)
- Demo funcionando
- Repositorio completo
- Documentación final

---

## Evaluación

Ver [rubrica.md](rubrica.md) para detalles completos.

**Distribución**:
- Checkpoints semanales: 40%
- Tests y calidad de código: 20%
- Modelos y análisis: 25%
- Presentación final: 15%

## Recursos

### Herramientas
- Python 3.11+
- PySpark 3.5
- Jupyter Notebooks
- Git/GitHub
- VS Code (recomendado)

### Libros Recomendados
- *Data Mining: Concepts and Techniques* (Han, Kamber, Pei)
- *Designing Data-Intensive Applications* (Kleppmann)
- *Feature Engineering for Machine Learning* (Zheng, Casari)

### Documentación
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Delta Lake](https://delta.io/) (opcional, para extender)

## Políticas del Curso

### Trabajo en Equipo
- Equipos de 3-4 estudiantes
- Todos los miembros deben contribuir al código (verificado via Git)
- Code reviews obligatorios

### Entregas
- Checkpoints semanales (ver [checkpoints.md](checkpoints.md))
- Deadline: Domingos 23:59
- Penalización por entrega tardía: -10% por día

### Integridad Académica
- Código propio del equipo
- Permitido: Consultar documentación, Stack Overflow, discusiones entre equipos
- No permitido: Copiar código de otros equipos
- Plagio detectado via similarity checking = 0 en el curso

### Soporte
- Office hours: Martes y Jueves 16:00-18:00
- GitHub Discussions para preguntas técnicas
- Slack del curso para coordinación

## Calendario Detallado

Ver [checkpoints.md](checkpoints.md) para fechas exactas y entregables.

---

**Instructor**: [Nombre]  
**Email**: [email]  
**Office**: [Ubicación]  
**GitHub**: [repo URL]
