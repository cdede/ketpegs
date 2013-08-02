import urwid
import pickle
import queue

class BaseUi:
    def __init__(self,client, queue,h = 3, w = 4):
        self.client = client
        self.queue = queue
        self.h = h
        self.w = w
        self.grid = []
        a1 =[]
        palette = [
            ('default', 'light green', 'black'),
            ('exposed', 'black', 'dark blue'),]
        for y in range(self.h):
            a2 = []
            for x in range(self.w):
                sei1 = urwid.SelectableIcon( 'a')
                map1 =  urwid.AttrMap(sei1, 'default')
                self.grid.append(sei1)
                a2.append(map1)
            tmp = urwid.GridFlow(a2, 3, 0, 0, 'left')
            a1.append(tmp)
        txt = urwid.Text("")
        self.statusline = txt
        footer =  urwid.AttrMap(txt, 'exposed')
        txt1 = urwid.Text("")
        a1.append(txt1)
        self.tipline = txt1
        display_widget = urwid.Pile(a1)
        self.p1 = display_widget
        ww = urwid.WidgetWrap(display_widget)
       
        edit_widget = urwid.Text("Type anything or press q to exit:")
        frame_widget = urwid.Frame(
            header=edit_widget,
            body=urwid.Filler(ww, valign='bottom'),
            footer = footer,
            focus_part='body'
        )
        loop = urwid.MainLoop(frame_widget, palette, unhandled_input=self.exit_on_enter)
        self.loop = loop

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                msg = pickle.loads(msg)
                self.render(msg)
            except queue.Empty:
                pass

    def render(self,msg):
        statusline = msg.statusline
        self.statusline.set_text(statusline)
        tipline = msg.tipline
        self.tipline.set_text(tipline)
        cells = msg.cells
        for x in range(self.h*self.w):
            g1 = cells[x]
            g2 = self.grid[x]
            gt1 = g2.get_text()
            if gt1 != g1:
                g2.set_text(g1)

    def exit_on_enter(self,key):
        self.client.queue.put(key)
        if key == 'q': 
            raise urwid.ExitMainLoop()

    @property
    def _cur_x(self):
        return self.p1.get_focus().focus_position

    @property
    def _cur_y(self):
        return self.p1.focus_position

