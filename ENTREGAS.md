# Guía de Entregas - GitHub

## Configuración Inicial (una sola vez)

1. **Acepta la invitación** al repositorio del curso en GitHub Classroom
2. **Clona** tu repositorio:
   ```powershell
   git clone https://github.com/UNAM-FI-MINERIADATOS-2026-1/mineria-datos-tu-usuario.git
   cd mineria-datos-tu-usuario
   ```
3. **Configura** tu nombre:
   ```powershell
   git config user.name "Tu Nombre"
   git config user.email "tu@email.com"
   ```

---

## Estructura de Entregas

```
tu-repositorio/
├── entregas/
│   ├── tareas/
│   │   ├── tarea_01/
│   │   │   └── tarea_01_apellido_nombre.pdf
│   │   ├── tarea_02/
│   │   └── ...
│   └── practicas/
│       ├── practica_01/
│       │   ├── bubble_sort.py
│       │   └── merge_sort.py
│       ├── practica_02/
│       └── ...
└── README.md
```

---

## Entrega de Tareas (PDF)

1. Resuelve los ejercicios indicados
2. Genera un PDF con tus respuestas
3. Nombra el archivo: `tarea_XX_apellido_nombre.pdf`
4. Colócalo en `entregas/tareas/tarea_XX/`
5. Haz commit y push:
   ```powershell
   git add entregas/tareas/tarea_01/
   git commit -m "Entrega tarea 01"
   git push
   ```

---

## Entrega de Prácticas (Código)

1. Implementa las funciones requeridas
2. Coloca tus archivos `.py` en `entregas/practicas/practica_XX/`
3. **Verifica que pasen los tests localmente:**
   ```powershell
   cd entregas/practicas/practica_01
   pytest tests/ -v
   ```
4. Haz commit y push:
   ```powershell
   git add entregas/practicas/practica_01/
   git commit -m "Entrega practica 01"
   git push
   ```
5. **Verifica el badge** ✅ en GitHub (los tests corren automáticamente)

---

## Fechas Límite

- La fecha de entrega es a las **23:59 hrs** del día indicado
- El **último commit antes de la fecha límite** es el que cuenta
- Puedes ver tu historial de commits en GitHub

---

## Política de Entregas Tardías

| Retraso | Penalización |
|---------|--------------|
| 1-2 días | -10% |
| 3-5 días | -25% |
| >5 días | -50% |

---

## Problemas Comunes

### "No puedo hacer push"
```powershell
git pull --rebase
git push
```

### "Mis tests no pasan en GitHub pero sí localmente"
- Verifica que no tengas paths absolutos en tu código
- Asegúrate de que todos los archivos necesarios estén en el commit

### "Quiero modificar mi entrega"
Mientras sea antes de la fecha límite, simplemente haz otro commit:
```powershell
git add .
git commit -m "Corrección tarea 01"
git push
```

---

## Contacto

Si tienes problemas con GitHub, contacta al profesor o ayudante **antes** de la fecha límite.
