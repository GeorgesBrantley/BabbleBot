# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
import groupMe

response.menu = [
    ('Home', False, URL('core', 'featureList'), []),

    ('Profiles', False, URL('core', 'featureList'), [])
]

response.menu.append(('My Groups', False, URL('auth','chooseGroup'), []))

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

# if not configuration.get('app.production'):
#     _app = request.application
#     response.menu += [
#         (T('Documentation'), False, '#', [
#             (T('Online book'), False, 'http://www.web2py.com/book'),
#             (T('Preface'), False,
#              'http://www.web2py.com/book/default/chapter/00'),
#             (T('Introduction'), False,
#              'http://www.web2py.com/book/default/chapter/01'),
#             (T('Python'), False,
#              'http://www.web2py.com/book/default/chapter/02'),
#             (T('Overview'), False,
#              'http://www.web2py.com/book/default/chapter/03'),
#             (T('The Core'), False,
#              'http://www.web2py.com/book/default/chapter/04'),
#             (T('The Views'), False,
#              'http://www.web2py.com/book/default/chapter/05'),
#             (T('Database'), False,
#              'http://www.web2py.com/book/default/chapter/06'),
#             (T('Forms and Validators'), False,
#              'http://www.web2py.com/book/default/chapter/07'),
#             (T('Email and SMS'), False,
#              'http://www.web2py.com/book/default/chapter/08'),
#             (T('Access Control'), False,
#              'http://www.web2py.com/book/default/chapter/09'),
#             (T('Services'), False,
#              'http://www.web2py.com/book/default/chapter/10'),
#             (T('Ajax Recipes'), False,
#              'http://www.web2py.com/book/default/chapter/11'),
#             (T('Components and Plugins'), False,
#              'http://www.web2py.com/book/default/chapter/12'),
#             (T('Deployment Recipes'), False,
#              'http://www.web2py.com/book/default/chapter/13'),
#             (T('Other Recipes'), False,
#              'http://www.web2py.com/book/default/chapter/14')
#         ])
#     ]
