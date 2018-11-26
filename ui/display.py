import curses


class Display(object):

    termWidth=None
    termLines=None
    stdscr = None

    def __init__(self):
        print("print screen")
        # self.draw_screen()

    def draw_screen(self):
        self.stdscr = curses.initscr()
        stdscr = self.stdscr
        k = 0
        cursor_x = 0
        cursor_y = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_color(0,0,0,0)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        whstr = "Width: {}, Height: {}".format(width, height)
        version = '0.1'

        statusbarstr = "Press 'q' to exit | press 'r' to refresh table | STATUS BAR | Pos: {}, {} | {}".format(cursor_x, cursor_y, whstr)
        headstr = "Prometheus v{}".format(version)

        # render the heading
        stdscr.attron(curses.color_pair(1))
        topbar = ((width//2)-len(headstr)//2)-2
        stdscr.addstr(0, 0, "┌" + "─" * topbar, curses.color_pair(4) )
        stdscr.addstr(0, topbar+2, headstr, curses.color_pair(6) | curses.A_BOLD)
        stdscr.addstr(0, topbar+len(headstr)+3, "─" * (topbar-1) +"┐", curses.color_pair(4) )

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 1, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr)+1, " " * (width - len(statusbarstr)-2))
        stdscr.attroff(curses.color_pair(3))

        # Refresh the screen
        stdscr.refresh()


    def getkey(self):
            return self.stdscr.getch()

    def end_display(self):
            curses.endwin()


    def drawTable(self,xstart, ystart, WIDTH, HEIGHT, cell_width):
        stdscr = self.stdscr
        retval = {}
        retval['X']=xstart
        retval['W']=WIDTH
        retval['Y']=ystart
        retval['H']=HEIGHT
        retval['cw']=cell_width

        # print the top line of the table
        stdscr.addstr(ystart, xstart, '┌' + '─'*(cell_width*WIDTH-1) + '┐')
        cell = ' '*(cell_width-1) + '│'

        for y in range(1, HEIGHT+1):

            ypos = ((y*2)-1)+ystart
            stdscr.addstr(ypos, xstart, '│' + cell * WIDTH )
            if y < HEIGHT:
                stdscr.addstr(ypos+1, xstart, '├' + '─'*(cell_width*WIDTH-1) + '┤')
            else:
                stdscr.addstr(ypos+1, xstart, '└' + '─'*(cell_width*WIDTH-1) + '┘')

        return retval

    def drawBox(self, x, y, w, h, format=curses.A_BLINK, label=None):
        stdscr = self.stdscr
        if label != None:
            top = "┌"+ "─"*( (w//2-1) - (len(label)//2) ) +' '+ label+' '
            end =  "─"*( w +1 - len(top) )+ "┐"
            top = top + end
            stdscr.addstr( y,     x,  top, format | curses.A_BOLD)
        else:
            stdscr.addstr( y,     x,  "┌"+ "─"*w  +"┐" , format)
        for ypos in range(0, h):
            stdscr.addstr(ypos+y+1, x,  "│"+ " "*w  +"│" , format)
        stdscr.addstr( y+h+1,   x,  "└"+ "─"*w  +"┘" , format)

        return {
            'X':x,
            'Y':y,
            'W':w,
            'H':h
        }

    def latencyWindow(self, up, down, info={"up":3, "down": 2, "rt":0}):
        stdscr = self.stdscr
        window = self.drawBox( 100, 2, 50, 10, label='latency')
        # draw labels
        up = self.drawBox(x=window['X']+7, y=window['Y']+1, w=40, h=1)
        down = self.drawBox(x=window['X']+7, y=window['Y']+4, w=40, h=1)

        stdscr.addstr(window['Y']+2, window['X']+1, 'UP: ', curses.color_pair(6) | curses.A_BOLD)
        stdscr.addstr(window['Y']+5, window['X']+1, 'Down: ', curses.color_pair(6) | curses.A_BOLD)

        # show latency
        stdscr.addstr(up['Y']+1, up['X']+1, '▒'*int(info['up']/10) + str(info['up']), curses.color_pair(3))
        stdscr.addstr(down['Y']+1, down['X']+1, '▒'*int(info['down']/10) + str(info['down']), curses.color_pair(3))


    def pop_table(self,tab, colx, coly, strInput, format=curses.A_BLINK):
        stdscr = self.stdscr
        strInput = str(strInput)[0:tab['cw']-1]

        if colx <= tab['W']-1 and coly <= tab['H']:
            stdscr.addstr((coly*2), (colx*tab['cw'])+1+tab['X'], strInput, format)
        else:
            stdscr.addstr((tab['H']*2)+2+tab['Y'], 0, 'out of bounds {}, {}'.format(self.termWidth, self.termLines), format)



        # return the cursor to the prompt position
    def prompt(self, strPrompt=':'):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height-2, 0, strPrompt)

    def statsTable(self, data):
        # create a table to hold the stats  @ 0,1
        tab = self.drawTable(1,1,len(data['heading']), len(data['entries'])+1, 15)

        for heading, pos in data['heading'].items():
            self.pop_table(tab, pos, 1, heading, curses.color_pair(6) | curses.A_BOLD)

        y=2 # 2 is the start position of the table so increment from here
        for asset in data['entries'].items():
            # populate the row label
            self.pop_table(tab, 0, y, asset[0], curses.A_BOLD)

            for key, value in asset[1].items():
                if value['change'] > 0:
                    self.pop_table(tab, data['heading'][key], y, value['value'], curses.color_pair(4))
                elif value['change'] < 0:
                    self.pop_table(tab, data['heading'][key], y, value['value'], curses.color_pair(5))
                else:
                    self.pop_table(tab, data['heading'][key], y, value['value'])

            y+=1

