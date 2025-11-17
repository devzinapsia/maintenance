# Módulos de Mantenimiento - Odoo

Este directorio contiene módulos personalizados para extender y mejorar las funcionalidades del módulo de Mantenimiento de Odoo.

## 📦 Módulos incluidos
- **maintenance_website_request**  
    Permite crear solicitudes de mantenimiento directamente desde el sitio web público.

## Características principales
- 🌐 Formulario web público y accesible  
- 👤 Selección de empleado responsable  
- 🔧 Selección de equipo averiado  
- 📝 Descripción detallada del problema  
- ✅ Página de confirmación tras el envío  
- 🔔 Integración directa con el módulo de mantenimiento de Odoo

## Estado
- ✅ Estable

## Versión compatible
- Odoo 18, 19 y Odoo.sh

## 🚀 Instalación

### Requisitos previos
- Odoo 18.0 o superior  
- Módulo `maintenance` instalado  
- Módulo `website` instalado  
- Módulo `hr` instalado

### Pasos generales
1. Copiar la carpeta del módulo (`maintenance_website_request`) al directorio de addons de Odoo (o al repositorio del proyecto en Odoo.sh).  
2. Actualizar la lista de aplicaciones en Odoo (Apps → Actualizar).  
3. Buscar e instalar `maintenance_website_request` desde el panel de Apps.  
4. Reiniciar el servicio de Odoo si es necesario.

Consejo (línea de comandos): asegúrate de que la ruta de addons esté incluida en `odoo.conf` y, si lo prefieres, instala el módulo con la opción `-i maintenance_website_request` al iniciar Odoo.

## Contribuciones y soporte
- Reporta issues o solicita mejoras en el repositorio.  
- Incluye detalles del entorno (versión de Odoo, sistema operativo, pasos para reproducir).
