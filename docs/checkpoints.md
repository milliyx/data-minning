# Checkpoints y Entregables

Este documento detalla los entregables semanales del curso.

## Formato de Entrega

Todos los entregables se suben al repositorio GitHub del equipo:

```
your-repo/
├── checkpoints/
│   ├── week01/
│   │   ├── README.md
│   │   └── [archivos específicos]
│   ├── week02/
│   └── ...
```

**Deadline**: Domingos 23:59  
**Método**: Pull Request a rama `main` con tag `checkpoint-XX`

---

## Checkpoint 1 (Semana 1-2): Setup y Ejecución Inicial

**Fecha límite**: Semana 2, Domingo 23:59

### Entregables

1. **Repositorio configurado**
   - Fork del template
   - README con nombres del equipo y team_id
   - `.gitignore` correcto (no subir `data/`)

2. **Pipeline ejecutado**
   - Evidencia de ejecución exitosa de `make all`
   - Screenshots de:
     - CLI output completo
     - Carpeta `data/` con Bronze/Silver/Gold
     - Un reporte de evaluación generado

3. **Configuración de equipo**
   - `configs/teams/teamXX.yaml` con parámetros propios
   - Documentación de por qué eligieron sus parámetros

### Criterios de Evaluación
- ✅ Repositorio funcional (40%)
- ✅ Pipeline ejecuta sin errores (40%)
- ✅ Documentación clara (20%)

---

## Checkpoint 2 (Semana 3): Análisis de Bronze Layer

**Fecha límite**: Semana 3, Domingo 23:59

### Entregables

1. **Notebook de exploración**
   - `checkpoints/week03/bronze_exploration.ipynb`
   - Análisis de cada tabla Bronze:
     - Row counts
     - Distribuciones (edad, planes, ciudades)
     - Estadísticas descriptivas
     - Visualizaciones (al menos 5)

2. **Test de reproducibilidad**
   - Evidencia de que mismo seed genera mismos datos
   - Test automatizado en `tests/test_reproducibility_team.py`
   - Comparación de hashes entre dos ejecuciones

3. **Documentación de esquemas**
   - `checkpoints/week03/schemas.md`
   - Descripción de cada columna de cada tabla
   - Business meaning de cada campo

### Criterios de Evaluación
- ✅ Análisis completo y profundo (50%)
- ✅ Test de reproducibilidad pasa (30%)
- ✅ Documentación clara (20%)

---

## Checkpoint 3 (Semana 4): Pipeline Bronze→Silver

**Fecha límite**: Semana 4, Domingo 23:59

### Entregables

1. **Reglas de calidad implementadas**
   - Al menos 3 reglas personalizadas adicionales
   - Documentadas en `checkpoints/week04/quality_rules.md`

2. **Reporte de calidad**
   - `checkpoints/week04/quality_report.md`
   - Resultados de todas las validaciones
   - Número de filas filtradas y por qué
   - Comparación Bronze vs Silver counts

3. **Tests de calidad**
   - `tests/test_quality_team.py`
   - Al menos 5 tests que verifican reglas
   - Todos los tests pasan

### Criterios de Evaluación
- ✅ Reglas de calidad correctas (40%)
- ✅ Reporte detallado (30%)
- ✅ Tests completos (30%)

---

## Checkpoint 4 (Semana 5): Pipeline Silver→Gold

**Fecha límite**: Semana 5, Domingo 23:59

### Entregables

1. **Tablas Gold generadas**
   - Todas las tablas Gold requeridas
   - Schemas documentados

2. **Dashboard de KPIs**
   - `checkpoints/week05/kpis_dashboard.ipynb`
   - Visualización de:
     - ARPU diario
     - Churn rate diario
     - Uso promedio por plan
     - Revenue total
     - Al menos 3 KPIs adicionales

3. **Feature documentation**
   - `checkpoints/week05/features.md`
   - Descripción de cada feature en `churn_features`
   - Razón de negocio para incluirla

### Criterios de Evaluación
- ✅ Tablas Gold correctas (40%)
- ✅ Dashboard informativo (40%)
- ✅ Documentación de features (20%)

---

## Checkpoint 5 (Semana 6-7): Modelo de Churn

**Fecha límite**: Semana 7, Domingo 23:59

### Entregables

1. **Modelo entrenado**
   - `data/models/churn_metrics_*.json` con métricas
   - F1 > 0.5 (mínimo aceptable)

2. **Análisis de features**
   - `checkpoints/week07/churn_analysis.ipynb`
   - Top 10 features con interpretación
   - Análisis de correlaciones
   - Feature ablation study (opcional, +bonus)

3. **Recomendaciones de negocio**
   - `checkpoints/week07/churn_recommendations.md`
   - Al menos 3 acciones concretas basadas en el modelo
   - Segmentos a targetear
   - ROI estimado

### Criterios de Evaluación
- ✅ Modelo con métricas aceptables (40%)
- ✅ Análisis técnico profundo (30%)
- ✅ Recomendaciones de negocio (30%)

---

## Checkpoint 6 (Semana 8): Modelo de LTV

**Fecha límite**: Semana 8, Domingo 23:59

### Entregables

1. **Modelo entrenado**
   - `data/models/ltv_metrics_*.json`
   - R² > 0.5 (mínimo aceptable)

2. **Análisis de predicciones**
   - `checkpoints/week08/ltv_analysis.ipynb`
   - Scatter plot: predicho vs real
   - Análisis de errores por segmento
   - Identificación de high-value users

3. **Business case**
   - `checkpoints/week08/ltv_business_case.md`
   - Cómo usar LTV para priorización
   - Estrategias de pricing
   - Análisis de CAC vs LTV

### Criterios de Evaluación
- ✅ Modelo con métricas aceptables (40%)
- ✅ Análisis de predicciones (30%)
- ✅ Business case sólido (30%)

---

## Checkpoint 7 (Semana 9): Segmentación

**Fecha límite**: Semana 9, Domingo 23:59

### Entregables

1. **Modelo de segmentación**
   - `data/models/segmentation_metrics_*.json`
   - Silhouette score documentado

2. **Perfiles de segmentos**
   - `checkpoints/week09/segments.ipynb`
   - Caracterización de cada segmento
   - Visualizaciones (scatter, heatmap)
   - Nombres descriptivos para segmentos

3. **Estrategias por segmento**
   - `checkpoints/week09/segment_strategies.md`
   - Plan de acción para cada segmento
   - Promos personalizadas
   - Canales de comunicación

### Criterios de Evaluación
- ✅ Segmentación coherente (40%)
- ✅ Perfiles bien caracterizados (30%)
- ✅ Estrategias accionables (30%)

---

## Checkpoint 8 (Semana 10): Evaluación Comparativa

**Fecha límite**: Semana 10, Domingo 23:59

### Entregables

1. **Reporte de evaluación completo**
   - `checkpoints/week10/evaluation.md`
   - Comparación de los 3 modelos
   - Análisis de sensibilidad a parámetros
   - Comparación con otro equipo (intercambio)

2. **Optimización de features**
   - Evidencia de feature selection/engineering
   - Mejora de métricas vs baseline

3. **Plan de monitoreo**
   - `checkpoints/week10/monitoring_plan.md`
   - Métricas a trackear en producción
   - Alertas y thresholds
   - Estrategia de retraining

### Criterios de Evaluación
- ✅ Reporte completo (40%)
- ✅ Optimización demostrada (30%)
- ✅ Plan de monitoreo realista (30%)

---

## Checkpoint 9 (Semana 11): Testing y CI/CD

**Fecha límite**: Semana 11, Domingo 23:59

### Entregables

1. **Suite de tests completa**
   - Coverage > 70%
   - Tests de:
     - Reproducibilidad
     - Calidad de datos
     - Esquemas Gold
     - Modelos (smoke tests)

2. **CI/CD funcionando**
   - `.github/workflows/ci.yml` configurado
   - Badge en README
   - Todas las PRs pasan CI

3. **Documentación técnica**
   - README actualizado con instrucciones completas
   - Docstrings en funciones principales
   - Diagramas de arquitectura

### Criterios de Evaluación
- ✅ Tests comprehensivos (50%)
- ✅ CI/CD funcionando (30%)
- ✅ Documentación profesional (20%)

---

## Checkpoint 10 (Semana 12): Presentación Final

**Fecha límite**: Semana 12, según calendario de presentaciones

### Entregables

1. **Presentación (slides)**
   - 20 minutos de contenido
   - Formato profesional
   - Incluir:
     - Problema de negocio
     - Arquitectura
     - Resultados de modelos
     - Insights clave
     - Recomendaciones
     - Lecciones aprendidas

2. **Demo en vivo**
   - Ejecución de `make all` sin errores
   - Mostrar al menos 2 notebooks
   - Navegación por tablas Gold

3. **Repositorio final**
   - Todo el código limpio y documentado
   - README profesional
   - Todos los checkpoints completados
   - CI pasando

### Criterios de Evaluación
- ✅ Presentación clara y profesional (40%)
- ✅ Demo funcional (30%)
- ✅ Repositorio completo (30%)

---

## Resumen de Fechas

| Semana | Checkpoint | Tema | Deadline |
|--------|-----------|------|----------|
| 2 | 1 | Setup | Semana 2, Dom 23:59 |
| 3 | 2 | Bronze Analysis | Semana 3, Dom 23:59 |
| 4 | 3 | Silver Pipeline | Semana 4, Dom 23:59 |
| 5 | 4 | Gold Pipeline | Semana 5, Dom 23:59 |
| 7 | 5 | Churn Model | Semana 7, Dom 23:59 |
| 8 | 6 | LTV Model | Semana 8, Dom 23:59 |
| 9 | 7 | Segmentation | Semana 9, Dom 23:59 |
| 10 | 8 | Evaluation | Semana 10, Dom 23:59 |
| 11 | 9 | Testing/CI | Semana 11, Dom 23:59 |
| 12 | 10 | Final Presentation | Variable |

---

## Políticas de Entrega

### Entregas Tardías
- Hasta 24h tarde: -10%
- 24-48h tarde: -25%
- >48h tarde: -50%
- No aceptado después de 1 semana

### Formato
- Todo vía GitHub (commits, PRs)
- Tag cada checkpoint: `git tag checkpoint-XX`
- Pull Request con descripción detallada

### Revisiones
- Feedback en 1 semana máximo
- Posibilidad de resubmit (1 vez) para checkpoints 1-9
- Checkpoint 10 (final) no admite resubmits

---

**Preguntas**: Usar GitHub Discussions o office hours.
