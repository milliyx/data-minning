# Rúbrica de Evaluación

## Distribución de Puntos

| Componente | Peso | Puntos |
|-----------|------|--------|
| Checkpoints 1-9 | 40% | 40 |
| Testing y Calidad de Código | 20% | 20 |
| Modelos y Análisis Técnico | 25% | 25 |
| Presentación Final | 15% | 15 |
| **TOTAL** | **100%** | **100** |

---

## 1. Checkpoints Semanales (40 puntos)

Cada checkpoint vale según peso específico:

| Checkpoint | Tema | Puntos | Peso |
|-----------|------|--------|------|
| 1 | Setup y Ejecución | 2 | 5% |
| 2 | Bronze Analysis | 4 | 10% |
| 3 | Silver Pipeline | 5 | 12.5% |
| 4 | Gold Pipeline | 5 | 12.5% |
| 5 | Churn Model | 6 | 15% |
| 6 | LTV Model | 6 | 15% |
| 7 | Segmentation | 5 | 12.5% |
| 8 | Evaluation | 4 | 10% |
| 9 | Testing/CI | 3 | 7.5% |

### Criterios Generales por Checkpoint

**Excelente (90-100%)**:
- Todos los entregables completos y funcionando
- Código limpio y bien documentado
- Análisis profundo con insights valiosos
- Presentación profesional

**Bueno (75-89%)**:
- Entregables completos con errores menores
- Código funcional pero mejorable
- Análisis adecuado
- Documentación suficiente

**Aceptable (60-74%)**:
- Entregables con funcionalidad básica
- Código con bugs o mal estructurado
- Análisis superficial
- Documentación mínima

**Insuficiente (<60%)**:
- Entregables incompletos o no funcionan
- Código con errores graves
- Análisis ausente o incorrecto
- Sin documentación

---

## 2. Testing y Calidad de Código (20 puntos)

### 2.1 Suite de Tests (10 puntos)

| Criterio | Puntos |
|----------|--------|
| Tests de reproducibilidad implementados y pasando | 2 |
| Tests de calidad de datos (>5 checks) | 3 |
| Tests de esquemas Gold | 2 |
| Tests de modelos (smoke tests) | 2 |
| Coverage >70% | 1 |

### 2.2 Calidad de Código (5 puntos)

| Criterio | Puntos |
|----------|--------|
| Linting pasa (ruff/flake8) | 1 |
| Código bien estructurado (modular) | 1 |
| Docstrings en funciones principales | 1 |
| Type hints donde apropiado | 1 |
| Nombres descriptivos de variables | 1 |

### 2.3 CI/CD (5 puntos)

| Criterio | Puntos |
|----------|--------|
| GitHub Actions configurado | 2 |
| CI pasa en todas las PRs | 2 |
| Badge en README | 1 |

---

## 3. Modelos y Análisis Técnico (25 puntos)

### 3.1 Modelo de Churn (8 puntos)

| Criterio | Puntos | Umbral Mínimo |
|----------|--------|---------------|
| F1 Score | 3 | >0.50 |
| Análisis de feature importance | 2 | Top 10 features |
| Interpretación de negocio | 2 | 3+ recomendaciones |
| Documentación técnica | 1 | Completa |

**Escala F1 Score**:
- F1 > 0.75: 3 puntos
- F1 > 0.60: 2 puntos
- F1 > 0.50: 1 punto
- F1 ≤ 0.50: 0 puntos

### 3.2 Modelo de LTV (8 puntos)

| Criterio | Puntos | Umbral Mínimo |
|----------|--------|---------------|
| R² Score | 3 | >0.50 |
| Análisis de errores | 2 | Scatter + residuals |
| Business case | 2 | CAC/LTV analysis |
| Documentación técnica | 1 | Completa |

**Escala R²**:
- R² > 0.75: 3 puntos
- R² > 0.60: 2 puntos
- R² > 0.50: 1 punto
- R² ≤ 0.50: 0 puntos

### 3.3 Modelo de Segmentación (6 puntos)

| Criterio | Puntos |
|----------|--------|
| Silhouette score razonable (>0.3) | 2 |
| Perfiles de segmentos bien caracterizados | 2 |
| Estrategias por segmento accionables | 2 |

### 3.4 Análisis Comparativo (3 puntos)

| Criterio | Puntos |
|----------|--------|
| Comparación entre modelos del equipo | 1 |
| Comparación con otro equipo | 1 |
| Análisis de sensibilidad a parámetros | 1 |

---

## 4. Presentación Final (15 puntos)

### 4.1 Contenido (8 puntos)

| Criterio | Puntos |
|----------|--------|
| Claridad del problema de negocio | 1 |
| Explicación de arquitectura | 1 |
| Resultados de churn model | 2 |
| Resultados de LTV model | 2 |
| Resultados de segmentación | 1 |
| Insights y recomendaciones | 1 |

### 4.2 Presentación (4 puntos)

| Criterio | Puntos |
|----------|--------|
| Slides profesionales | 1 |
| Claridad en comunicación | 1 |
| Tiempo respetado (20 min) | 1 |
| Respuestas a preguntas | 1 |

### 4.3 Demo en Vivo (3 puntos)

| Criterio | Puntos |
|----------|--------|
| Pipeline ejecuta sin errores | 1 |
| Navegación fluida por código/resultados | 1 |
| Explicación técnica clara | 1 |

---

## Criterios de Penalización

### Penalizaciones Automáticas

| Infracción | Penalización |
|-----------|--------------|
| Entrega tardía (por día) | -10% del checkpoint |
| CI no pasa | -5 puntos totales |
| Código no ejecuta | -20 puntos totales |
| Datos en repositorio (no .gitignored) | -5 puntos |
| Sin documentación README | -10 puntos |

### Plagio / Integridad Académica

- **Plagio detectado**: 0 en el curso
- **Código copiado de otro equipo**: 0 en checkpoint afectado
- **Contribución desigual** (verificado via Git):
  - Miembro sin commits: 0 individual
  - Miembro con <10% commits: -50% nota final individual

---

## Bonificaciones

| Logro | Bonificación |
|-------|--------------|
| Feature engineering creativo (+3 features útiles) | +2 puntos |
| Visualizaciones excepcionales | +2 puntos |
| Análisis de sensibilidad completo | +2 puntos |
| Extensión a Delta Lake (time-travel real) | +5 puntos |
| Contribución a template (PR aceptado) | +3 puntos |

**Máximo de bonificaciones**: +10 puntos (total puede ser >100)

---

## Escala Final

| Nota | Calificación |
|------|--------------|
| 90-100+ | Sobresaliente (A) |
| 80-89 | Notable (B) |
| 70-79 | Bien (C) |
| 60-69 | Aprobado (D) |
| <60 | Suspenso (F) |

---

## Trabajo en Equipo

### Evaluación Individual

Cada miembro recibe:
```
Nota Individual = (Nota Equipo × 0.7) + (Contribución Individual × 0.3)
```

**Contribución Individual** se evalúa por:
- % de commits (verificado via `git log`)
- Participación en presentación
- Peer evaluation (evaluación entre miembros)

### Peer Evaluation

Cada miembro evalúa a sus compañeros en:
1. Contribución técnica (código)
2. Participación en análisis
3. Comunicación y colaboración
4. Cumplimiento de deadlines

---

## Requisitos Mínimos para Aprobar

Para obtener nota ≥60 (aprobado):

✅ **Checkpoints**: Completar al menos 7 de 9 checkpoints  
✅ **Testing**: Coverage >50% y CI pasando  
✅ **Modelos**: F1 >0.5 (churn) y R² >0.5 (LTV)  
✅ **Presentación**: Asistir y presentar  
✅ **Código**: Pipeline ejecuta de inicio a fin sin errores críticos

---

## Revisión y Apelaciones

- **Feedback**: Provisto en 1 semana por checkpoint
- **Resubmits**: Permitido 1 vez para checkpoints 1-9 (máximo +50% de puntos perdidos)
- **Apelaciones**: Hasta 1 semana después de recibir nota
- **Nota final**: Publicada máximo 2 semanas post-presentación

---

## Contacto

**Preguntas sobre evaluación**: Office hours o email del instructor  
**Disputas de nota**: Procedimiento formal vía coordinación académica
