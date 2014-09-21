from plone import api
from caes.search.splash import ISplashU
from caes.contact.contact import Contact
from plone.dexterity.interfaces import IDexterityContent
from collections import OrderedDict


def default_facets():
    # TODO: make a configuration panel for these
    return ['Faculty',
            'Department',
            'Major',
            'Center',
            'Group',
            'News Item',
            'Other',
            ]


def haystack(needle, facet=None):
    """
    Given a keyword, return the right results.
    These should be ordered by type.

    @category means to only include a certain category (aka type)
    this is complicated by the fact that we always want to know the
    size of other categories on the front end.
    """
    categories = OrderedDict({})

    catalog = api.portal.get_tool(name='portal_catalog')
    limit = 10
    if facet:
        limit = 50

    uid_results = []
    for category in default_facets():
        categories[category] = {}
        friendly_id = category.replace(" ", "").lower()

        """
        We need to make sure we aren't adding things in multiple times
        if they show up in multiple results
        """
        cat_results = {'splash': [],
                       'tags': [],
                       'other': [],
                       'num_results': 0,
                       'friendly_id': friendly_id
                       }
        include_full_results = (facet and category == facet) or not facet

        """
        Handle the "Other" Category. Basically, anything we may have missed.
        Note this must go last and is almost a special case at this point.
        """
        if category == 'Other':
            for brain in catalog.searchResults(SearchableText=needle)[:limit]:
                if brain.UID not in uid_results:
                    uid_results.append(brain.UID)
                    cat_results['num_results'] += 1
                    if include_full_results:
                        cat_results['other'].append(marshall_brain(brain))
            categories[category] = cat_results
            continue

        """
        Look for Splashes
        """
        contentFilter = {'splash_keywords': needle, 'Type': category}
        for brain in catalog.searchResults(contentFilter):
            if include_full_results:
                cat_results['splash'].append(marshall_brain(brain))
            uid_results.append(brain.UID)
            cat_results['num_results'] += 1

        """
        Look for Keywords
        """
        for brain in catalog.searchResults(Subject=needle,
                                           Type=category)[:limit]:
            if brain.UID not in uid_results:
                uid_results.append(brain.UID)
                cat_results['num_results'] += 1
                if include_full_results:
                    cat_results['tags'].append(marshall_brain(brain))

        """
        Look for Other Searchable text
        """
        for brain in catalog.searchResults(SearchableText=needle,
                                           Type=category)[:limit]:
            if brain.UID not in uid_results:
                uid_results.append(brain.UID)
                cat_results['num_results'] += 1
                if include_full_results:
                    cat_results['other'].append(marshall_brain(brain))

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
    elif brain.portal_type == 'News Item':
        result['banner'] = "%s/image_preview" % (brain.getURL())
    result['type'] = brain.portal_type
    result['url'] = brain.getURL()
    result['title'] = brain.Title
    result['summary'] = brain.Description
    result['keywords'] = brain.Subject
    result['author'] = brain.Creator
    result['modified'] = brain.ModificationDate
    result['effective'] = brain.EffectiveDate
    result['contact'] = ""
    if IDexterityContent.providedBy(sobj):
        result['contact'] = Contact(sobj).contact
    return result

