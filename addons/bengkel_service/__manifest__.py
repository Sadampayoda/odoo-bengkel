{
    'name': 'Bengkel Service',
    'version': '1.0',
    'summary': 'Manajemen servis bengkel',
    'category': 'Services',
    'author': 'Sadam',
    'license': 'LGPL-3',
    'depends': ['base','product', 'stock', 'account'],
    'data': [
        'security/ir.access.csv',
        'views/vehicle_views.xml',
        'views/order_views.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
}