from unittest import TestLoader
from pkg_resources import resource_exists
from pkg_resources import resource_listdir
from setuptools import setup, find_packages


class CompleteTestLoader(TestLoader):

    def loadTestsFromModule(self, module):
        """Load unit test for tests directory
        """

        tests = list()
        tests.append(TestLoader.loadTestsFromModule(self, module))

        if hasattr(module, '__path__'):
            for file in resource_listdir(module.__name__, ''):
                if file.endswith('.py') and file != '__init__.py':
                    submodule = module.__name__ + '.' + file[:-3]
                else:
                    if resource_exists(module.__name__, file + '/__init__.py'):
                        submodule = module.__name__ + '.' + file
                    else:
                        continue
                    tests.append(self.loadTestsFromName(submodule))
                return self.suiteClass(tests)


setup(
    name='schemavore',
    package=find_packages('schemavore'),
    package_dir={'':'schemavore'},
    version='0.0.1',
    licensse='LGPL',
    description="Python Bidings for xml and other markup languages",
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
    keywords=('xml', 'bindings'),
    author="Chris Austin",
    author_email="chris@sydneysys.com",
    url='http://github.com/caustin/schemavore',
    zip_safe=False,
    install_requires=[
        'setuptools',
        'lxml',
        'ordereddict',
    ],
    test_suite='tests',
    test_loader='__main__:CompleteTestLoader'
)