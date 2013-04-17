# coding: utf-8
import sublime, sublime_plugin
import subprocess

class Pylit(sublime_plugin.WindowCommand):
    def run(self):
        cur_view = self.window.active_view()

        if "py" in cur_view.syntax_name(cur_view.sel()[0].b):

            settings = sublime.load_settings('Pylit.sublime-settings')

            try:
                p = subprocess.Popen(settings.get('pylint')[sublime.platform()]+" \""+str(cur_view.file_name())+"\"", \
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out, err = p.communicate()

                result = self.output_title(str(cur_view.file_name()))
                result += self.section_title("PyLint")
                result += out

                p = subprocess.Popen(settings.get('pep8')[sublime.platform()]+" \""+str(cur_view.file_name())+"\"", \
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out, err = p.communicate()

                result += self.section_title("PEP8")
                result += out.replace(str(cur_view.file_name())+":","")

                view = self.window.new_file()
                edit = view.begin_edit()
                view.insert(edit, 0, result)
            except Exception, e:
                print e

        else:
            sublime.error_message("File must be .py")
            raise Exception("File must be .py")
        
        return True

    def output_title(self, filename):
        result = "# "+str(filename)+" \n"
        result += "# ==================================== \n\n"

        return result

    def section_title(self, title):
        result = "# ==================================== \n"
        result += "# "+str(title)+" \n"
        result += "# ==================================== \n\n"

        return result
