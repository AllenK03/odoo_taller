from odoo import models, fields, api

class TallerOrden(models.Model):
    _name = 'taller.orden'
    _description = 'Orden de Trabajo de Taller'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Número de Orden',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        tracking=True
    )
    vehicle_id = fields.Many2one(
        'taller.vehicle',
        string='Vehículo',
        required=True,
        domain="[('partner_id', '=', partner_id)]",
        tracking=True
    )
    date_entry = fields.Datetime(
        string='Fecha de Ingreso',
        default=fields.Datetime.now,
        required=True,
        tracking=True
    )
    date_delivery_expected = fields.Date(
        string='Entrega Estimada',
        tracking=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Mecánico Asignado',
        default=lambda self: self.env.user,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Proceso'),
        ('waiting_parts', 'En Espera de Repuestos'),
        ('ready', 'Listo para Entrega'),
        ('done', 'Entregado / Finalizado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft', tracking=True, required=True)

    diagnosis = fields.Text(string='Diagnóstico / Falla Reportada')
    notes = fields.Text(string='Observaciones Internas')

    line_ids = fields.One2many(
        'taller.orden.line',
        'orden_id',
        string='Líneas de Trabajo / Repuestos'
    )

    amount_total = fields.Float(
        string='Total ($)',
        compute='_compute_amount_total',
        store=True
    )

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(line.subtotal for line in record.line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('taller.orden') or 'Nuevo'
        return super().create(vals_list)

    # Métodos para los botones de flujo de trabajo
    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_waiting_parts(self):
        self.write({'state': 'waiting_parts'})

    def action_ready(self):
        self.write({'state': 'ready'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})


class TallerOrdenLine(models.Model):
    _name = 'taller.orden.line'
    _description = 'Línea de Orden de Trabajo'

    orden_id = fields.Many2one('taller.orden', string='Orden', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Servicio / Repuesto', required=True)
    name = fields.Char(string='Descripción')
    quantity = fields.Float(string='Cantidad', default=1.0, required=True)
    price_unit = fields.Float(string='Precio Unitario', required=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.display_name
            self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit