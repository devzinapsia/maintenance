# -*- coding: utf-8 -*-

import base64
from odoo import http, _
from odoo.http import request


class MaintenanceWebsiteRequest(http.Controller):

    @http.route('/maintenance/request', type='http', auth='public', website=True, sitemap=True)
    def maintenance_request_form(self, **kwargs):
        """Renderiza el formulario de solicitud de mantenimiento"""
        # Obtener empleados, equipos y equipos de mantenimiento disponibles
        employees = request.env['hr.employee'].sudo().search([])
        equipments = request.env['maintenance.equipment'].sudo().search([])
        maintenance_teams = request.env['maintenance.team'].sudo().search([])
        
        values = {
            'employees': employees,
            'equipments': equipments,
            'maintenance_teams': maintenance_teams,
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
        required_fields = ['employee_id', 'maintenance_team_id', 'equipment_id', 'description']
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
            maintenance_teams = request.env['maintenance.team'].sudo().search([])
            
            values = {
                'employees': employees,
                'equipments': equipments,
                'maintenance_teams': maintenance_teams,
                'error': error,
                'error_message': error_message,
                'employee_id': post.get('employee_id'),
                'maintenance_team_id': post.get('maintenance_team_id'),
                'equipment_id': post.get('equipment_id'),
                'description': post.get('description'),
            }
            
            return request.render('maintenance_website_request.maintenance_request_form_template', values)
        
        # Crear la solicitud de mantenimiento
        try:
            # Obtener el empleado y equipo seleccionados
            employee = request.env['hr.employee'].sudo().browse(int(post.get('employee_id')))
            equipment = request.env['maintenance.equipment'].sudo().browse(int(post.get('equipment_id')))
            
            # Preparar valores para la solicitud
            vals = {
                'name': _('Solicitud desde sitio web - %s') % employee.name,
                'request_date': request.env.cr.now(),
                'owner_user_id': employee.user_id.id if employee.user_id else False,
                'maintenance_team_id': int(post.get('maintenance_team_id')),
                'equipment_id': equipment.id,
                'description': post.get('description'),
                'maintenance_type': 'corrective',
                'schedule_date': request.env.cr.now(),
            }
            
            # Usar la empresa del equipo si existe
            if equipment.company_id:
                vals['company_id'] = equipment.company_id.id
            
            # Crear la solicitud
            maintenance_request = request.env['maintenance.request'].sudo().create(vals)
            
            # Procesar archivo adjunto si existe
            attachment_file = request.httprequest.files.get('attachment')
            if attachment_file and attachment_file.filename:
                # Leer el contenido del archivo
                file_content = attachment_file.read()
                
                # Crear el adjunto
                request.env['ir.attachment'].sudo().create({
                    'name': attachment_file.filename,
                    'datas': base64.b64encode(file_content),
                    'res_model': 'maintenance.request',
                    'res_id': maintenance_request.id,
                    'type': 'binary',
                })
            
            # Redirigir a página de confirmación
            return request.redirect('/maintenance/request/thanks?request_id=%s' % maintenance_request.id)
            
        except Exception as e:
            error_message.append(_('Error al crear la solicitud: %s') % str(e))
            
            employees = request.env['hr.employee'].sudo().search([])
            equipments = request.env['maintenance.equipment'].sudo().search([])
            maintenance_teams = request.env['maintenance.team'].sudo().search([])
            
            values = {
                'employees': employees,
                'equipments': equipments,
                'maintenance_teams': maintenance_teams,
                'error': error,
                'error_message': error_message,
                'employee_id': post.get('employee_id'),
                'maintenance_team_id': post.get('maintenance_team_id'),
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