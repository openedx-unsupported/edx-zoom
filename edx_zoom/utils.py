from xmodule.course_module import CourseFields, Dict, Scope
from django.utils.translation import ugettext as _


def add_to_course_fields():
    CourseFields.zoom_settings = Dict(
            display_name=_("Zoom LTI settings"),
            help=_('Create an object with "key", "secret" and optional "url"'),
            scope=Scope.settings
        )
