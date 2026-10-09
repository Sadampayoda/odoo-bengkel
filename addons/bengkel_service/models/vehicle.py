from odoo import api, fields, models #type: ignore
from odoo.exceptions import ValidationError #type: ignore



class Vehicle(models.Model):
    _name="bengkel_service.vehicle"
    _description="Kendaraan"
    _rec_name="name"
    _order="name"

    name = fields.Char(string="Name", required=True)
    plate = fields.Char(string="Plat Nomor", required=True)
    brand = fields.Char(string='Merek')
    type = fields.Selection(
        [('car', 'Mobil'), ('motorcycle', 'Motor'), ('truck', 'Truk')],
        string='Jenis', default='car')
    color = fields.Char(string="Warna")
    year = fields.Integer(string="Tahun")
    customer_id = fields.Many2one('res.partner', string='Pemilik')
    order_ids = fields.One2many(
        'bengkel_service.order', 'vehicle_id', string='Riwayat Servis')  # type: ignore

    @api.constrains('plate')
    def _check_plate(self):
        for rec in self:
            if self.search_count([('plate', '=', rec.plate), ('id', '!=', rec.id)]):
                raise ValidationError("Plat nomor sudah terdaftar.")
