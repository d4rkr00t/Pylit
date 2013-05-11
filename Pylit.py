# coding: utf-8
"""
Pylit - Pylint and PEP8 Sublime Text integration
"""

# result = output_title(str(self.cur_view.file_name()))
# view = self.window.new_file()
# edit = view.begin_edit()
# view.insert(edit, 0, replace_line_too_long(result))

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

        if "py" in self.cur_view.syntax_name(self.cur_view.sel()[0].b):

            settings = sublime.load_settings('Pylit.sublime-settings')

            try:
                result = pep8(settings, self.cur_view, settings.get('remove_line_to_long'))
                self.recomendations = gen_recomendation_list(result)

                result = pylint(settings, self.cur_view, settings.get('remove_line_to_long'))
                self.recomendations += gen_recomendation_list(result)

                self.window.show_quick_panel(self.recomendations, self.selected, sublime.MONOSPACE_FONT)

            except Exception, error:
                print error

        else:
            sublime.error_message("File must be .py")
            raise Exception("File must be .py")

        return True

    def selected(self, item):
        """
        Call show line recomendations when user select line in sublime quick panel
        """
        show_line_recomendations(self.cur_view, self.recomendations, item)


def pep8(settings, view, line_to_long, title=False):
    """Check file with pep8 and process output"""
    result = ""

    proccess = subprocess.Popen(settings.get('pep8')[sublime.platform()]+" \""+str(view.file_name())+"\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = proccess.communicate()
    del err

    if title:
        result += section_title("PEP8")

    result += out.replace(str(view.file_name())+":", "")

    if line_to_long:
        result = remove_line_too_long(result)

    return result


def pylint(settings, view, line_to_long, title=False):
    """Check file with pylint and process output"""
    result = ""

    proccess = subprocess.Popen(settings.get('pylint')[sublime.platform()]+" \""+str(view.file_name())+"\"",
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = proccess.communicate()
    del err

    if title:
        result += section_title("PyLint")
    else:
        result = re.sub(r"\*\*\*\*\*\*\*\*\*\*\*\*\* Module .+\n", "", out).split("Report")
        if result[0]:
            result = result[0]
            result = result.replace('\n', '')
            result = result.replace('C:', '\nC:').replace('W:', '\nW:').replace('E:', '\nE:').replace('F:', '\nF:')

    if line_to_long:
        result = remove_line_too_long(result)

    return result


def show_line_recomendations(view, rec_list, item):
    """Move cursor to line where need fixes and show fix missage in status bar"""
    print rec_list[item]
    line, column = False, False

    match = re.search(r"(\d+[\:|,]\d+)\:", rec_list[item])
    if match:
        line, column = re.findall(r"[\d]+", match.groups()[0])

    if line and column:
        point = view.text_point(int(line)-1, int(column)-1)

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


def remove_line_too_long(line):
    """Remove line to long message"""
    line = re.sub(r".+line too long.+\n", "", line)
    return re.sub(r".+Line too long.+\n", "", line)


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
