from plone import api
from caes.search.splash import ISplashU
from caes.contact.contact import Contact
from plone.dexterity.interfaces import IDexterityContent


def haystack(needle, category=None):
    """
    Given a keyword, return the right results.
    These should be ordered by type. Will need to figure that out
    for long term workings because category need not
    100% be mapped to certain types

    @category means to only include a certain category (aka type)
    """
    # default categories
    categories = {'Faculty': {},
                  'Department': {},
                  'Major': {},
                  'Center': {},
                  'News Item': {},
                  'Group': {},
                  'Other': {},
                  }
    if category:
        categories = {category: {} }

    catalog = api.portal.get_tool(name='portal_catalog')

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
        """
        Look for Splashes
        """
        contentFilter = {'splash_keywords': needle, 'Type': category}
        for brain in catalog.searchResults(contentFilter):
            cat_results['splash'].append(marshall_brain(brain))
            uid_results.append(brain.UID)

        """
        Look for Keywords
        """
        for brain in catalog.searchResults(Subject=needle,
                                           Type=category):
            if brain.UID not in uid_results:
                cat_results['tags'].append(marshall_brain(brain))
                uid_results.append(brain.UID)

        """
        Look for Other Searchable text
        """
        for brain in catalog.searchResults(SearchableText=needle,
                                           Type=category):
            if brain.UID not in uid_results:
                cat_results['other'].append(marshall_brain(brain))
                uid_results.append(brain.UID)

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

