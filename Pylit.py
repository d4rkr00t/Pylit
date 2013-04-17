# coding: utf-8
"""
Pylit - Pylint and PEP8 Sublime Text integration
"""

import sublime
import sublime_plugin
import subprocess
import re

class Pylit(sublime_plugin.WindowCommand):
    """
    Pylit command class
    """
    def run(self):
        """
        Runing file analyze with pylint and pep8
        """
        cur_view = self.window.active_view()

        if "py" in cur_view.syntax_name(cur_view.sel()[0].b):

            settings = sublime.load_settings('Pylit.sublime-settings')

            try:
                proccess = subprocess.Popen(settings.get('pep8')[sublime.platform()]+" \""+str(cur_view.file_name())+"\"",
                                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out, err = proccess.communicate()
                del err

                result = output_title(str(cur_view.file_name()))
                result += section_title("PEP8")
                result += out.replace(str(cur_view.file_name())+":", "")+"\n\n\n"

                proccess = subprocess.Popen(settings.get('pylint')[sublime.platform()]+" \""+str(cur_view.file_name())+"\"",
                                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out, err = proccess.communicate()
                del err

                result += section_title("PyLint")
                result += out

                view = self.window.new_file()
                edit = view.begin_edit()
                view.insert(edit, 0, replace_line_too_long(result))

            except Exception, error:
                print error

        else:
            sublime.error_message("File must be .py")
            raise Exception("File must be .py")

        return True


def replace_line_too_long(s):
    s = re.sub(r".+line too long.+\n","",s)
    return re.sub(r".+Line too long.+\n","",s)


def output_title(filename):
    """ Generate output titlt """
    result = "# "+str(filename)+" \n"
    result += "# ==================================== \n\n"

    return result


def section_title(title):
    """ Generate section titlt """
    result = "# ==================================== \n"
    result += "# "+str(title)+" \n"
    result += "# ==================================== \n\n"

    return result
