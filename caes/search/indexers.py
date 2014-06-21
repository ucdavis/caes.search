from plone.indexer.decorator import indexer
from caes.search.splash import ISplashU
import logging
import re


@indexer(ISplashU)
def splash_keywords(object):
    try:
        final = []
        # handle poorly entered keywords
        for keyword in object.keywords:
            multiple = re.split('[,.:;]', keyword)
            if len(multiple) > 1:
                final += multiple
                continue
            final.append(keyword)
        return final
    except AttributeError, e:
        logging.errror("Tried to index an object with ISplashU interface,'+ \
                      ' but no keywords item - %s: %s" % (object.absolute_url(),
                                                          e))
    except:  # should never fail save because of this
        logging.error("Could not index for splash inclusion - %s: %s" % (object.absolute_url(),
                                                                         e))
