import json
import datetime
from Products.Five.browser import BrowserView
from caes.search import search


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
        if not self.needle:
            results = {}
        else:
            results = search.haystack(self.needle,
                                      category=self.category)
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')

        return json.dumps(results, default=dt_handler)

    @property
    def needle(self):
        return self.form_attr('needle')

    @property
    def category(self):
        return self.form_attr('category')

    def form_attr(self, attrid, raise_on_missing=False):
        if attrid in self.request.form:
            return self.request.form.get(attrid)
        if raise_on_missing:
            raise AttributeError
        return None
