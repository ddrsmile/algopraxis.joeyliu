# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.forms import Media, widgets
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static

class BaseWidget(widgets.Widget):
    def render_html(self, name, value, attrs):
        return super(BaseWidget, self).render(name, value, attrs)

    def render(self, name, value, attrs=None, **kwargs):
        try:
            id_ = attrs['id']
        except (KeyError, TypeError):
            raise TypeError("BaseWidget cannot be rendered without an 'id' attribute")

        widget_html = self.render_html(name, value, attrs)
        js = self.render_js_init(id_, name, value)
        output = '{widget_html}<script>{js}</script>'.format(widget_html=widget_html, js=js)
        return mark_safe(output)

    def render_js_init(self, id_, name, value):
        return ''

class CodeTextWidget(BaseWidget, widgets.Textarea):
    def render_js_init(self, id_, name, value):
        jsinit = """
            if (window.ACEInstances == null) {{
                window.ACEInstances = {{}};
            }}
            // get the information used to create ace editor for each block
            var code_value_id = "{id!s}"
            var mode_value_id = code_value_id.replace("code", "lang_mode");
            var code = document.getElementById(code_value_id);
            var mode = document.getElementById(mode_value_id).value;
            // mode_map is defined in aes/utils.jp
            mode = mode_map[mode];
            var code_panel = document.createElement("div");
            code.parentElement.appendChild(code_panel);
            code.style.display = "none";

            // create ace editor
            var _editor = ace.edit(code_panel);

            // setup editor
            _editor.$blockScrolling = Infinity;
            _editor.container.style.height = "300px";
            _editor.container.style.weight = "100%";
            _editor.resize();
            _editor.setTheme("ace/theme/chrome");
            _editor.setShowPrintMargin(false);
            _editor.setFontSize(13);
            _editor.setStyle("editor");

            // setup editor session
            _editor.getSession().setUseWorker(false);
            _editor.getSession().setUseSoftTabs(true);
            _editor.getSession().setValue(code.value);
            _editor.getSession().setMode("ace/mode/" + mode);

            // added event listener to update code textarea
            // pass session into the function to bind the corresponding textarea.
            _editor.getSession().on("change", function(e, _session) {{
                var code = document.getElementById("{id!s}");
                code.value = _session.getValue();
            }});

            window.ACEInstances[code_value_id] = _editor;
        """
        return jsinit.format(id=id_)

    @property
    def media(self):
        js = (
            static('parts/ace/ace.js'),
            static('parts/ace/utils.js'),
        )
        return Media(js=js)
