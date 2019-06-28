
__version__ = 'v1.0'


from setuptools import setup, find_packages

from distutils.command.build_py import build_py

import os

with open('README.md') as file:
    long_description = file.read()

with open('custom_plots/__init__.py', 'r') as f:
    exec(f.readline())


print(find_packages())
# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

def _get_requirements_from_files(groups_files):
    groups_reqlist = {}

    for k,v in groups_files.items():
        with open(v, 'r') as f:
            pkg_list = f.read().splitlines()
        groups_reqlist[k] = pkg_list

    return groups_reqlist

def setup_package():
    # get all file endings and copy whole file names without a file suffix
    # assumes nested directories are only down one level
    example_data_files = set()
    for i in os.listdir("custom_plots/Tests/"):
        if i.endswith(('py', 'pyc')):
            continue
        if not os.path.isdir("custom_plots/Tests/" + i):
            if "." in i:
                glob_name = "Tests/*." + i.split(".")[-1]
            else:
                glob_name = "Tests/" + i
        else:
            glob_name = "Tests/" + i + "/*"

        example_data_files.add(glob_name)
    _groups_files = {
        'base': 'requirements.txt',
        'plus': 'requirements_plus.txt',
        'dev': 'requirements_dev.txt',
        'docs': 'requirements_docs.txt'
    }

    reqs = _get_requirements_from_files(_groups_files)
    install_reqs = reqs.pop('base')
    extras_reqs = reqs
    setup(
        name='fancy_spatial_geometries_plot',
        version=__version__,
        description="A library for custom plots using geopandas, geopy, cartopy and matplotlib.",
        long_description=long_description,
        maintainer="Philipe Riskalla leal developer",
        maintainer_email='leal.philipe@gmail.com',
        url='https://github.com/PhilipeRLeal/fancy_spatial_geometries_plot',
        download_url='TODO',
        license='TODO',
        packages=find_packages(),
        python_requires='>3.5',
        test_suite='TODO',
        tests_require=['TODO'],
        keywords='fancy spatial geometries plot',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: GIS',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        package_data={'fancy_spatial_geometries_plot': list(example_data_files)},
        install_requires=install_reqs,
        extras_require=extras_reqs,
        cmdclass={'build_py': build_py}
    )


if __name__ == '__main__':
    setup_package()