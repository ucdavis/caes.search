from setuptools import setup, find_packages

version = '1.0'

setup(name='caes.search',
      version=version,
      description="",
      long_description=open("README.rst").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='custom caes search behaviors and results',
      author='eleddy',
      author_email='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['caes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.namedfile',
          'plone.formwidget.namedfile',
      ],
      extras_require={
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[],
      )
