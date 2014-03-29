from plone import api


def haystack(needle, category=None):
    """
    Given a keyword, return the right results.
    These should be ordered by type. Will need to figure that out
    for long term workings because category need not
    100% be mapped to certain types

    @category means to only include a certain category
    """
    results = {'Other': [] } 
    categories = ['Faculty',
                  'Departments',
                  'Majors',
                  'Centers',
                  'News',
                  'Groups',
                  ]
    if category:
        categories = [category, ]

    catalog = api.portal.get_tool(name='portal_catalog')

    contentFilter = {'splash_keywords': needle}
    # XXX: maybe switch away from JSON. THis is too much stuff
    for brain in catalog.searchResults(contentFilter):
        sobj = brain.getObject()
        banner_url = "%s/@@download/banner/%s" % (brain.getURL(),
                                                  sobj.banner.filename)
        results['Other'].append({'banner': banner_url,
                                 'type': brain.portal_type,
                                 'url': brain.getURL(),
                                 'title': brain.Title,
                                 'summary': brain.Subject,
                                 })

    return results
