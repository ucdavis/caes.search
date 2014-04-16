from plone import api
from caes.search.splash import ISplashU
from caes.contact.contact import Contact
from plone.dexterity.interfaces import IDexterityContent


def default_facets():
    # TODO: make a configuration panel for these
    return {'Faculty': {},
            'Department': {},
            'Major': {},
            'Center': {},
            'News Item': {},
            'Group': {},
            'Other': {},
            }


def haystack(needle, facet=None):
    """
    Given a keyword, return the right results.
    These should be ordered by type.

    @category means to only include a certain category (aka type)
    this is complicated by the fact that we always want to know the
    size of other categories on the front end.
    """
    categories = default_facets()

    catalog = api.portal.get_tool(name='portal_catalog')
    limit = 10
    if facet:
        limit = 50

    for category in categories.keys():
        """
        We need to make sure we aren't adding things in multiple times
        if they show up in multiple results
        """
        uid_results = []
        cat_results = {'splash': [],
                       'tags': [],
                       'other': [],
                       'num_results': 0,
                       }
        include_full_results = (facet and category == facet) or not facet
        """
        Look for Splashes
        """
        contentFilter = {'splash_keywords': needle, 'Type': category}
        for brain in catalog.searchResults(contentFilter)[:limit]:
            if include_full_results:
                cat_results['splash'].append(marshall_brain(brain))
            uid_results.append(brain.UID)

        """
        Look for Keywords
        """
        for brain in catalog.searchResults(Subject=needle,
                                           Type=category)[:limit]:
            if brain.UID not in uid_results:
                uid_results.append(brain.UID)
                if include_full_results:
                    cat_results['tags'].append(marshall_brain(brain))

        """
        Look for Other Searchable text
        """
        for brain in catalog.searchResults(SearchableText=needle,
                                           Type=category)[:limit]:
            if brain.UID not in uid_results:
                uid_results.append(brain.UID)
                if include_full_results:
                    cat_results['other'].append(marshall_brain(brain))

        cat_results['num_results'] = len(uid_results)
        categories[category] = cat_results

    return categories


def marshall_brain(brain):
    result = {}
    sobj = brain.getObject()
    result['banner'] = ''
    if ISplashU.providedBy(sobj):
        if sobj.banner:
            result['banner'] = "%s/@@download/banner/%s" % (brain.getURL(),
                                                            sobj.banner.filename)
    result['type'] = brain.portal_type
    result['url'] = brain.getURL()
    result['title'] = brain.Title
    result['summary'] = brain.Description
    result['keywords'] = brain.Subject
    result['contact'] = ""
    if IDexterityContent.providedBy(sobj):
        result['contact'] = Contact(sobj).contact
    return result

