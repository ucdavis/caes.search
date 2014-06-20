import json
import datetime
from Products.Five.browser import BrowserView
from caes.search import search
import plone.api


def dt_handler(obj):
    if isinstance(obj, datetime.datetime):
        # Strip microseconds, format as ISO 8601, so iOS app can read properly.
        return obj.replace(microsecond=0).isoformat()
    else:
        return obj


class CaesSearchResults(BrowserView):
    """
    serialize the search results and then return as json
    """
    def __call__(self):
        if self.json:
            self.request.response.setHeader('Content-Type',
                                            'application/json; charset=utf-8')
            return json.dumps(self.results, default=dt_handler)
        self._results = {}
        return self.index()

    # TODO: throw a memoize up here
    @property
    def results(self):
        if not self.needle:
            return {}
        else:
            return search.haystack(self.needle,
                                   facet=self.category)

    @property
    def all_facets(self):
        return search.default_facets()

    def facet_selected(self, facet):
        return facet == self.category

    @property
    def needle(self):
        return self.form_attr('needle')

    @property
    def json(self):
        return self.form_attr('json')

    @property
    def category(self):
        return self.form_attr('category')

    def form_attr(self, attrid, raise_on_missing=False):
        if attrid in self.request.form:
            return self.request.form.get(attrid)
        if raise_on_missing:
            raise AttributeError
        return None

    @property
    def portal_url(self):
        return plone.api.portal.get().absolute_url()
