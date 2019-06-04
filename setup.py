"""Setup for lti_consumer XBlock."""

import os
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


setup(
    name='edx-zoom',
    version='1.0.1',
    description='This XBlock implements the LTI interface for Zoom video conferencing.',
    packages=[
        'edx_zoom',
    ],
    install_requires=[
        'edx-opaque-keys',
        'django',
        'lti_consumer-xblock',
    ],
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
