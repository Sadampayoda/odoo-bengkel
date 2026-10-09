from odoo import api, fields, models #type: ignore
from odoo.exceptions import UserError #type: ignore



class Order(models.Model):
    _name = "bengkel_service.order"
    _description = "Pesanan Servis"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(string='Nomor', default='New', readonly=True, copy=False)
    vehicle_id = fields.Many2one(
        'bengkel_service.vehicle', string='Kendaraan', required=True)  # type: ignore
    customer_id = fields.Many2one(
        'res.partner', string='Pelanggan',
        related='vehicle_id.customer_id', store=True)
    mechanic_id = fields.Many2one('res.users', string='Mekanik')
    date_in = fields.Datetime(string='Tanggal Masuk', default=fields.Datetime.now)
    complaint = fields.Text(string='Keluhan')
    diagnosis = fields.Text(string='Diagnosa')
    state = fields.Selection(
        [('draft', 'Draft'), ('diagnosa', 'Diagnosa'), ('proses', 'Dikerjakan'),
         ('done', 'Selesai'), ('cancel', 'Dibatalkan')],
        string='Status', default='draft')
    line_ids = fields.One2many(
        'bengkel_service.order.line', 'order_id', string='Item Pekerjaan')  # type: ignore
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id)
    total = fields.Monetary(
        string='Total', compute='_compute_total', store=True,
        currency_field='currency_id')

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total = sum(rec.line_ids.mapped('subtotal'))

    def action_diagnosa(self):
        self.write({'state': 'diagnosa'})

    def action_proses(self):
        for rec in self:
            if not rec.mechanic_id:
                raise UserError('Mekanik belum dipilih')
        self.write({'state': 'proses'})

    def action_done(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError('Item Pekerjaan belum diisi')
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})


