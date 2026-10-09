from odoo import api, fields, models #type: ignore
from odoo.exceptions import ValidationError #type: ignore

class OrderLine(models.Model):
    _name = 'bengkel_service.order.line'
    _description = 'Item Pekerjaan'

    order_id = fields.Many2one(
        'bengkel_service.order', string='Work Order',
        required=True, ondelete='cascade')  # type: ignore
    product_id = fields.Many2one(
        'product.product', string='Jasa / Sparepart', required=True)
    quantity = fields.Float(string='Jumlah', default=1.0)
    price_unit = fields.Float(string='Harga Satuan')
    currency_id = fields.Many2one(related='order_id.currency_id')
    subtotal = fields.Monetary(
        string='Subtotal', compute='_compute_subtotal', store=True,
        currency_field='currency_id')

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
