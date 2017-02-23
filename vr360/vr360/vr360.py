"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from django.template import Template, Context


class Vr360XBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    display_name = String(display_name="Display Name",
        default="360 Degree Video",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="Video URL",
        default="https://s3.amazonaws.com/vids.slawrence.io/bears.mp4",
        scope=Scope.content,
        help="The URL for your video.")

    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.resource_string(template_path)
        return Template(template_str).render(Context(context))

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the Vr360XBlock, shown to students
        when viewing courses.
        """
        domain = 'cloudfront.net'
        if domain in self.url:
            url = self.url
        else:
            url = self.url
        static_context = {
            "simple360_css":self.runtime.local_resource_url(self, 'public/css/simple-360.css'),
            "glmatrix_js":self.runtime.local_resource_url(self, 'public/js/gl-matrix.js'),
            "simple360_js":self.runtime.local_resource_url(self, 'public/js/simple-360.js'),
            "controls_js":self.runtime.local_resource_url(self, 'public/js/controls.js'),
            "menu_js":self.runtime.local_resource_url(self, 'public/js/menu.js'),
            "url":url,
        }

        html = self.render_template("static/html/vr360.html",static_context)
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/vr360.css"))
        frag.add_javascript(self.resource_string("static/js/src/vr360.js"))
        frag.initialize_js('Vr360XBlock')
        return frag

    def studio_view(self, context=None):
        context = {
            'unique_id': unicode(self.course_id),
            'display_name': self.display_name,
            'url': self.url
        }
        html = self.render_template('static/html/vr360_edit.html', context)
        
        frag = Fragment(html)
        frag.add_javascript(self.resource_string("static/js/src/vr360_edit.js"))
        frag.initialize_js('Vr360XBlockInitStudio')
        return frag

    @XBlock.json_handler
    def save_videojs(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        
        return {
            'result': 'success',
        }
    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Vr360XBlock",
             """<vr360/>
             """),
            ("Multiple Vr360XBlock",
             """<vertical_demo>
                <vr360/>
                <vr360/>
                <vr360/>
                </vertical_demo>
             """),
        ]
