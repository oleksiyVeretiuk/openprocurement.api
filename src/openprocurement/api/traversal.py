# -*- coding: utf-8 -*-

from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
)


class Root(object):
    __name__ = None
    __parent__ = None
    __acl__ = [
        # (Allow, Everyone, ALL_PERMISSIONS),
        (Allow, 'g:admins', ALL_PERMISSIONS),
        (Allow, 'g:bots', 'upload_tender_documents')
    ]

    def __init__(self, request):
        self.request = request
        self.db = request.registry.db


def generate_plural_name(name):
    if name.endswith('s'):
        plural_name = '{}es'.format(name)
    else:
        plural_name = '{}s'.format(name)
    return plural_name


def get_item(parent, key, request):
    request.validated['{}_id'.format(key)] = request.matchdict['{}_id'.format(key)]
    field_name = generate_plural_name(key)
    items = [i for i in getattr(parent, field_name, []) if i.id == request.matchdict['{}_id'.format(key)]]
    if not items:
        from openprocurement.api.utils import error_handler
        request.errors.add('url', '{}_id'.format(key), 'Not Found')
        request.errors.status = 404
        raise error_handler(request)
    else:
        if key == 'document':
            request.validated['{}s'.format(key)] = items
        item = items[-1]
        request.validated[key] = item
        request.validated['id'] = request.matchdict['{}_id'.format(key)]
        item.__parent__ = parent
        return item


def factory(request):
    root = Root(request)
    return root
