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
    recomendations = []
    cur_view = None

    def run(self):
        """
        Runing file analyze with pylint and pep8
        """
        self.cur_view = self.window.active_view()

        if "py" in self.cur_view.scope_name(self.cur_view.sel()[0].b):

            settings = sublime.load_settings('Pylit.sublime-settings')

            try:
                result = pep8(settings, self.cur_view,
                              settings.get('remove_line_to_long'))

                self.recomendations = gen_recomendation_list(result)

                result = pylint(settings, self.cur_view,
                                settings.get('remove_line_to_long'))

                self.recomendations += gen_recomendation_list(result)

                self.window.show_quick_panel(self.recomendations,
                                             self.selected,
                                             sublime.MONOSPACE_FONT)

            except Exception as error:
                print(123)
                print(error)

        else:
            sublime.error_message("File must be .py")
            raise Exception("File must be .py")

        return True

    def selected(self, item):
        """
        Call show line recomendations when user
        select line in sublime quick panel
        """
        show_line_recomendations(self.cur_view, self.recomendations, item)


class PylitReport(sublime_plugin.WindowCommand):
    """
    Pylit command class for pylit report command
    """
    recomendations = []
    cur_view = None

    def run(self):
        """
        Runing file analyze with pylint and pep8
        """
        self.cur_view = self.window.active_view()

        if "py" in self.cur_view.scope_name(self.cur_view.sel()[0].b):

            settings = sublime.load_settings('Pylit.sublime-settings')

            result = output_title(str(self.cur_view.file_name()))

            try:
                result += pep8(settings, self.cur_view,
                               settings.get('remove_line_to_long'), True)

                result += pylint(settings, self.cur_view,
                                 settings.get('remove_line_to_long'), True)

                print(result)

            except Exception as error:
                print(error)

        else:
            sublime.error_message("File must be .py")
            raise Exception("File must be .py")

        return True


class PylitSave(sublime_plugin.EventListener):
    """Pylit on save event listner"""

    def on_post_save(self, view):
        """Remove pylit message after save the view"""
        view.erase_status("Pylint")


# COMMON FUNCTIONS
def pep8(settings, view, line_to_long, title=False):
    """Check file with pep8 and process output"""
    result = ""

    proccess = subprocess.Popen(settings.get('pep8')[sublime.platform()] + " --ignore E501 \"" + str(view.file_name()) +
                                "\"",
                                shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = proccess.communicate()
    # del err

    if title:
        result += section_title("PEP8")

    result += out.decode().replace(str(view.file_name()) + ":", "")

    if line_to_long:
        result = remove_line_too_long(result, True)

    return result


def pylint(settings, view, line_to_long, title=False):
    """Check file with pylint and process output"""
    result = ""

    proccess = subprocess.Popen(settings.get('pylint')[sublime.platform()] + " \"" + str(view.file_name()) + "\"",
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    out, err = proccess.communicate()
    del err

    if title:
        result += section_title("PyLint")
        result += out.decode()
    else:
        regexped = re.sub(r"\*\*\*\*\*\*\*\*\*\*\*\*\* Module .+\n",
                          "", out.decode()).split("Report")
        if regexped[0]:
            result = regexped[0]
            result = result.replace('\n', '')
            result = result.replace('C:', '\nC:').replace('W:', '\nW:').replace('E:', '\nE:').replace('F:', '\nF:')

    if line_to_long:
        result = remove_line_too_long(result, True)

    return result


def show_line_recomendations(view, rec_list, item):
    """Move cursor to line where need fixes and
    show fix missage in status bar"""
    if item >= 0:
        print(rec_list[item])
        line, column = False, False

        match = re.search(r"(\d+[\:|,]\d+)\:", rec_list[item])
        if match:
            line, column = re.findall(r"[\d]+", match.groups()[0])

        if line and column:
            point = view.text_point(int(line) - 1, int(column) - 1)

            view.sel().clear()
            view.sel().add(sublime.Region(point))

            view.show(sublime.Region(point))

            view.erase_status("Pylint")
            view.set_status("Pylint", rec_list[item])
        else:
            sublime.error_message("No line founded!")
            raise Exception("No line founded!")


def gen_recomendation_list(output):
    """Generate list of recomendations"""
    result = []

    output = output.split("\n")

    for line in output:
        if len(line) > 0:
            result.append(line)

    return result


def remove_line_too_long(line, remove):
    """Remove line to long message"""
    if remove:
        line = re.sub(r".+line too long.+\n", "", line)
        return re.sub(r".+Line too long.+\n", "", line)

    return line


def output_title(filename):
    """ Generate output titlt """
    result = "# " + str(filename) + " \n"
    result += "# ==================================== \n\n"

    return result


def section_title(title):
    """ Generate section titlt """
    result = "\n\n# ==================================== \n"
    result += "# " + str(title) + " \n"
    result += "# ==================================== \n\n"

    return result
