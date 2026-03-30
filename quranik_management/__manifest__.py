{
    'name': 'Quranik Management',
    'version': '1.0',
    'summary': 'Quran Teaching Management System for Teachers and Students',
    'description': 'Manage Quran teachers, students, subscriptions, and moral values tracking.',
    'category': 'Education',
    'author': 'Quranik',
    'depends': ['base', 'mail', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'data/quran_data.xml',
        'views/res_partner_views.xml',
        'views/quran_session_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}