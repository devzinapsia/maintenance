# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request


class MaintenanceWebsiteRequest(http.Controller):

    @http.route('/maintenance/request', type='http', auth='public', website=True, sitemap=True)
    def maintenance_request_form(self, **kwargs):
        """Renderiza el formulario de solicitud de mantenimiento"""
        # Obtener empleados y equipos disponibles
        employees = request.env['hr.employee'].sudo().search([])
        equipments = request.env['maintenance.equipment'].sudo().search([])
        
        values = {
            'employees': employees,
            'equipments': equipments,
            'error': {},
            'error_message': [],
        }
        
        return request.render('maintenance_website_request.maintenance_request_form_template', values)

    @http.route('/maintenance/request/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def maintenance_request_submit(self, **post):
        """Procesa el envío del formulario de solicitud de mantenimiento"""
        error = {}
        error_message = []
        
        # Validación de campos requeridos
        required_fields = ['employee_id', 'equipment_id', 'description']
        for field in required_fields:
            if not post.get(field):
                error[field] = 'missing'
        
        # Validación de descripción
        if post.get('description') and len(post.get('description').strip()) < 10:
            error['description'] = 'too_short'
            error_message.append(_('La descripción debe tener al menos 10 caracteres.'))
        
        # Si hay errores, volver a mostrar el formulario con los errores
        if error:
            employees = request.env['hr.employee'].sudo().search([])
            equipments = request.env['maintenance.equipment'].sudo().search([])
            
            values = {
                'employees': employees,
                'equipments': equipments,
                'error': error,
                'error_message': error_message,
                'employee_id': post.get('employee_id'),
                'equipment_id': post.get('equipment_id'),
                'description': post.get('description'),
            }
            
            return request.render('maintenance_website_request.maintenance_request_form_template', values)
        
        # Crear la solicitud de mantenimiento
        try:
            # Obtener el empleado seleccionado
            employee = request.env['hr.employee'].sudo().browse(int(post.get('employee_id')))
            
            # Crear la solicitud
            maintenance_request = request.env['maintenance.request'].sudo().create({
                'name': _('Solicitud desde sitio web - %s') % employee.name,
                'request_date': request.env.cr.now(),
                'owner_user_id': employee.user_id.id if employee.user_id else False,
                'equipment_id': int(post.get('equipment_id')),
                'description': post.get('description'),
                'maintenance_type': 'corrective',
                'schedule_date': request.env.cr.now(),
            })
            
            # Redirigir a página de confirmación
            return request.redirect('/maintenance/request/thanks?request_id=%s' % maintenance_request.id)
            
        except Exception as e:
            error_message.append(_('Error al crear la solicitud: %s') % str(e))
            
            employees = request.env['hr.employee'].sudo().search([])
            equipments = request.env['maintenance.equipment'].sudo().search([])
            
            values = {
                'employees': employees,
                'equipments': equipments,
                'error': error,
                'error_message': error_message,
                'employee_id': post.get('employee_id'),
                'equipment_id': post.get('equipment_id'),
                'description': post.get('description'),
            }
            
            return request.render('maintenance_website_request.maintenance_request_form_template', values)

    @http.route('/maintenance/request/thanks', type='http', auth='public', website=True)
    def maintenance_request_thanks(self, **kwargs):
        """Página de agradecimiento después de enviar la solicitud"""
        request_id = kwargs.get('request_id')
        
        values = {
            'request_id': request_id,
        }
        
        return request.render('maintenance_website_request.maintenance_request_thanks_template', values)