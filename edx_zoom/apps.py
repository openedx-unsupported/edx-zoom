"""
edx_zoom Django application initialization.
"""

from django.apps import AppConfig



class XBlockZoomApp(AppConfig):
    """
    Configuration for the edx_zoom Django application.
    """

    name = 'edx_zoom'
    plugin_app = {}

    def ready(self):
        """
        Monkeypatch the course metadata
        """
        from .utils import add_to_course_fields
        add_to_course_fields()
