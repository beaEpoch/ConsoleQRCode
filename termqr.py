#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import qr
import urwid



palette = [
    ('highlight', 'white', 'black'),
    ('bg', 'black', 'white'),
]

g_text =  [
	urwid.AttrMap(urwid.Text(u' '), 'bg'),
	urwid.AttrMap(urwid.Text(u' '), 'highlight'),
]

g_wraptext = {}
LINE_WIDTH = 0


def get_wraptext(cnt, mode):
	lst = []	
	key = '%d%s'%(cnt, mode)
	amap = g_wraptext.get(key, None)
	if not amap:
		for _ in xrange(cnt*2):
			g_wraptext.setdefault(key, []).append(g_text[mode])
	return g_wraptext[key]

def get_qr_layout(txt):
	digitqr = qr.qrcode(txt, format=qr.FMT_DIGIT, scale=1, separator=1)
	
        cnt = 0
        pc = None
        lst = digitqr.split(' ')
        lines = []
	global LINE_WIDTH
        LINE_WIDTH = len(lst)
        for row in lst:
                line = []
                for c in row:
                        if c != pc:
                                if pc:
                                        line.append((int(pc),cnt))
                                cnt = 0
                        cnt += 1
                        pc = c

                if cnt:
                        line.append((int(pc),cnt))
                        lines.append(line)
                        cnt = 0
	return lines	
	

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def main(argv):
	if len(argv) != 2:
		print './termqr.py \'qrcode context text\''
		return 0

	lines = get_qr_layout(argv[1])
	blocks = []
	for line in lines:
		lst = []
		for mode, cnt in line:
			lst.extend(get_wraptext(cnt, mode))
		blocks.append(urwid.GridFlow(lst, 1, 0, 0, 'left'))

	tail = u'press \'q\' to exit.'
	tailMap = urwid.AttrMap(urwid.Text(tail), 'highlight')
	blocks.append(urwid.GridFlow([g_text[1], tailMap], len(tail), (LINE_WIDTH-len(tail)) * 2, 0, 'left'))
	pl = urwid.Pile(blocks)
	last = urwid.Filler(pl, 'top')
	
	urwid.MainLoop(last, palette, unhandled_input=exit_on_q).run()

	return 0

if __name__ == '__main__':
	main(sys.argv)
