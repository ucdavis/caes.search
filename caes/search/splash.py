from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from rwproperty import getproperty, setproperty
from caes.search import MessageFactory as _
from plone.namedfile.field import NamedBlobImage
from z3c.form.interfaces import IEditForm, IAddForm
from plone.z3cform.textlines.textlines import TextLinesFieldWidget


class ISplashU(form.Schema):
    """Marker/Form interface for splash behavior
    """

    form.fieldset('splash',
                  label=u"Splash Settings",
                  fields=['keywords', 'banner']
    )

    form.widget(keywords=TextLinesFieldWidget)
    form.omitted('keywords')
    form.no_omit(IEditForm, 'keywords')
    form.no_omit(IAddForm, 'keywords')
    keywords = schema.List(
        title=_(u'Keywords'),
        description=_(u'A list of search keywords that' +
           ' will return this item as a splash result.'),
        required=False,
        value_type=schema.TextLine()
    )

    form.omitted('banner')
    form.no_omit(IEditForm, 'banner')
    form.no_omit(IAddForm, 'banner')
    banner = NamedBlobImage(
        title=_(u"Banner image"),
        required=False,
    )


alsoProvides(ISplashU, IFormFieldProvider)


class Splash(object):
    implements(ISplashU)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    @getproperty
    def keywords(self):
        return getattr(self.context, 'keywords')

    @setproperty
    def keywords(self, value):
        setattr(self.context, 'keywords', value)

    @getproperty
    def banner(self):
        return getattr(self.context, 'banner')

    @setproperty
    def banner(self, value):
        setattr(self.context, 'banner', value)

