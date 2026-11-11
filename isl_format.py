"""ISL: Format and ISL: Lint -- run the bundled tools/isl.py.

With a non-empty selection, only the selected lines are formatted / reported.

Settings (ISL.sublime-settings): isl_tools_path (default: bundled tools/), isl_python,
isl_format_on_save.
"""

import os
import subprocess

import sublime
import sublime_plugin


BUNDLED_TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')


def _settings():
    return sublime.load_settings('ISL.sublime-settings')


def tool_path(name):
    return os.path.join(_settings().get('isl_tools_path') or BUNDLED_TOOLS, name)


def python():
    return _settings().get('isl_python') or 'python3'


def _format(view, text, lines=None):
    indent = str(view.settings().get('tab_size', 2))
    cmd = [python(), tool_path('isl.py'), 'fmt', '--indent', indent]
    if lines:
        cmd += ['--lines', '%d-%d' % lines]
    proc = subprocess.run(
        cmd + ['-'],
        input=text, capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'isl fmt failed')
    return proc.stdout


def selected_lines(view):
    """1-based (first, last) line span of the selection, or None if nothing is selected."""
    sels = [r for r in view.sel() if not r.empty()]
    if not sels:
        return None
    first = view.rowcol(min(r.begin() for r in sels))[0] + 1
    last_pt = max(r.end() for r in sels)
    last = view.rowcol(last_pt)[0] + 1
    if view.rowcol(last_pt)[1] == 0 and last > first:
        last -= 1          # selection ends at the start of a line: that line is not included
    return first, last


class IslFormatCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.match_selector(0, 'source.isl')

    def run(self, edit):
        view = self.view
        region = sublime.Region(0, view.size())
        old = view.substr(region)
        lines = selected_lines(view)
        try:
            new = _format(view, old, lines)
        except Exception as exc:  # surface problems in the status bar, never crash a save
            sublime.status_message('ISL format failed: %s' % exc)
            return
        if new != old:
            position = view.viewport_position()
            view.replace(edit, region, new)
            view.set_viewport_position(position, False)


class IslLintCommand(sublime_plugin.WindowCommand):
    """Build-system target: lints the active file into the build output panel."""

    def run(self, fix=False, **kwargs):
        view = self.window.active_view()
        if not view or not view.file_name():
            sublime.status_message('ISL lint: save the file first')
            return
        cmd = [python(), tool_path('isl.py'), 'lint']
        lines = selected_lines(view)
        if lines and not fix:
            cmd += ['--lines', '%d-%d' % lines]
        if fix:
            cmd.append('--fix')
        cmd.append(view.file_name())
        self.window.run_command('exec', {
            'cmd': cmd,
            'file_regex': r'^(.+?):(\d+):(\d+): (.*)$',
            'working_dir': os.path.dirname(view.file_name()),
        })


class IslFormatOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.match_selector(0, 'source.isl') and view.settings().get('isl_format_on_save'):
            view.run_command('isl_format')
