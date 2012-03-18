import os
import re

from tornado.template import Loader


class MapTemplateLoader(Loader):

    def __init__(self, mappings, root_directory, **kwargs):
        super(MapTemplateLoader, self).__init__(root_directory, **kwargs)
        self.mappings = dict(self._prepare_mappings(mappings))

    def _prepare_mappings(self, mappings):
        for pretend_path, real_path in mappings.iteritems():
            expression = re.compile('^%s(?=/)' % re.escape(pretend_path))
            yield expression, real_path

    def resolve_path(self, name, parent_path=None):
        for pattern, real_path in self.mappings.iteritems():
            if pattern.search(name):
                path = pattern.sub(real_path, name)
                return os.path.relpath(path, start=self.root)
        else:
            return os.path.join(self.root, 'templates', name)
