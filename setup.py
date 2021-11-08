"""Setup for lti_consumer XBlock."""

import os
import re
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, __, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = get_version("edx_zoom", "__init__.py")


setup(
    name='edx-zoom',
    version=VERSION,
    description='This XBlock implements the LTI interface for Zoom video conferencing.',
    packages=[
        'edx_zoom',
    ],
    install_requires=load_requirements('requirements/base.in'),
    entry_points={
        'xblock.v1': [
            'edx_zoom = edx_zoom:ZoomXBlock',
        ],
        'lms.djangoapp': [
            "edx_zoom = edx_zoom.apps:XBlockZoomApp",
        ],
        'cms.djangoapp': [
            "edx_zoom = edx_zoom.apps:XBlockZoomApp",
        ],

    },
    package_data=package_data("edx_zoom", ["static", "templates", "public", "translations"]),
)
