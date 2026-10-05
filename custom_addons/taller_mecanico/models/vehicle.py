from odoo import models, fields, api

class TallerVehicle(models.Model):
    _name = 'taller.vehicle'
    _description = 'Vehículo del Taller'
    _rec_name = 'license_plate'

    license_plate = fields.Char(string='Placa', required=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Propietario / Cliente', required=True, ondelete='restrict')
    brand = fields.Char(string='Marca', required=True)
    model = fields.Char(string='Modelo', required=True)
    year = fields.Integer(string='Año')
    vin = fields.Char(string='VIN / Número de Chasis')
    color = fields.Char(string='Color')
    mileage = fields.Integer(string='Último Kilometraje (Km)', default=0)
    notes = fields.Text(string='Observaciones')

    _sql_constraints = [
        ('unique_license_plate', 'unique(license_plate)', '¡Ya existe un vehículo registrado con esta misma placa!')
    ]