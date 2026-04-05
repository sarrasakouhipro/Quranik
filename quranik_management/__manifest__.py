{
    'name': 'Quranik Management',
    'version': '1.0',
    'summary': 'Quran Academy Management System (MVP)',
    'description': """
        Management module for Quranik.org:
        - Profiles for Teachers (Readings, Bio, Languages)
        - Profiles for Students (Credits, Progress)
        - Quran Session Scheduling & Reporting
        - Moral Values (Makarim Al-Akhlaq) Tracking
        - Automated Meeting Links
    """,
    'category': 'Education',
    'author': 'Quranik',
    'website': 'https://quranik.org',
    
    # Dependencies: 
    # 'mail' for tracking changes/chatter
    # 'calendar' for scheduling integration
    'depends': [
        'base', 
        'mail', 
        'calendar'
    ],
    
    # Data files loaded on installation/update
    'data': [
        'security/ir.model.access.csv',
        'security/quranik_security.xml',
        'data/quran_data.xml',
        'data/mail_template_data.xml',
        'wizard/session_close_view.xml',
        'views/res_partner_views.xml',
        'views/quran_session_views.xml',
        'views/menu_views.xml',        
    ],
    
    # Demo data for testing (only loaded if 'Load Demo Data' is checked)
    'demo': [
        'demo/quran_demo.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
