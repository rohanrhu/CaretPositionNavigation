# CaretPositionNavigation (Sublime Text Plugin) (https://github.com/rohanrhu/CaretPositionNavigation)
# 
# Navigate prev-next over cursor position history in Sublime Text!
# 
# Copyright (C) 2017 Oğuzhan Eroğlu <rohanrhu2@gmail.com>
# 
# The MIT License (MIT)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sublime
import sublime_plugin

HISTORY_LENGTH = 50
THRESHOLD = 20

last_pos = (0, 0)
diff = 0
is_first_pos = True

def add_pos(history, pos, ind):
    global HISTORY_LENGTH
    global THRESHOLD

    global last_pos
    global diff
    global is_first_pos

    (ny, nx) = (pos[0], pos[1])
    if history.__len__() > 0:
        (py, px) = (last_pos[0], last_pos[1])
    else: (py, px) = (0, 0)

    diff += (ny - py)
    if is_first_pos or ((diff >= THRESHOLD) or (diff <= (THRESHOLD*-1))):
        if ind < -1:
            if ind == (history.__len__()*-1):
                history = []
            else:
                history = history[:ind+1]

        history.append(pos)
        diff = 0
        nind = -1
    else: nind = ind
    if history.__len__() > HISTORY_LENGTH:
        history.pop(0)

    is_first_pos = False

    return (history, nind)

def plugin_loaded():
    global HISTORY_LENGTH
    global THRESHOLD

    settings = sublime.load_settings('Prefences.sublime-settings')

    HISTORY_LENGTH = settings.get('history_length', 50)
    THRESHOLD = settings.get('threshold', 20)

class CaretPosNavCommand(sublime_plugin.TextCommand):
    def run(self, edit, nav):
        view = self.view
        if not view:
            view = self.window.active_view()
            if view is None:
                return

        if not view.settings().has('caret_pos_history'):
            return

        if not view.settings().has('history_indicator'):
            return

        global diff

        history = view.settings().get('caret_pos_history')
        ind = view.settings().get('history_indicator')

        if nav == 'prev':
            if ind > history.__len__()*-1:
                ind -= 1
            else: return
        elif nav == 'next':
            if ind < -1:
                ind += 1
            else: return

        view.settings().set('is_event', True)

        region = view.sel()[0]
        point = region.begin()
        pos = view.rowcol(point)
        npos = history[ind]
        npoint = view.text_point(npos[0], npos[1])
        nregion = sublime.Region(npoint, npoint)
        if point != npoint:
            view.sel().add(nregion)
            view.sel().subtract(region)

        view.show_at_center(npoint)

        view.settings().set('history_indicator', ind)

class CaretPosClearHistoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global is_first_pos
        
        self.view.settings().set('caret_pos_history', [])
        self.view.settings().set('history_indicator', -1)

        diff = 0
        is_first_pos = True
        on_caret_move(self.view)

def on_caret_move(view):
    global last_pos
    global is_first_pos

    if view.settings().get('is_widget') or view.settings().get('command_mode'):
        return

    if not view.settings().get('caret_pos_history'):
        view.settings().set('caret_pos_history', [])

    if not view.settings().get('history_indicator'):
        view.settings().set('history_indicator', -1)

    if not view.settings().has('is_event'):
        view.settings().set('is_event', False)

    pos = view.rowcol(view.sel()[0].begin())

    if view.settings().get('is_event'):
        view.settings().set('is_event', False)
        last_pos = pos
        return

    if is_first_pos:
        last_pos = pos
    add_result = add_pos(view.settings().get('caret_pos_history'), pos, view.settings().get('history_indicator'))
    
    view.settings().set('caret_pos_history', add_result[0])
    view.settings().set('history_indicator', add_result[1])
    
    last_pos = pos

class CaretPosNavListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        on_caret_move(view)