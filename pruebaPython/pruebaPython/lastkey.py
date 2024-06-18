import pynput.keyboard as pk, pynput, time

time.sleep(2)

idkL: list = []

controler = pk.Controller()

matches: dict[str, pynput.keyboard.Key] = {
	'left' : pynput.keyboard.Key.left,
	'right' : pynput.keyboard.Key.right,
	'up' : pynput.keyboard.Key.up,
	'down' : pynput.keyboard.Key.down,
	'tab' : pynput.keyboard.Key.tab,
	'caps_lock' : pynput.keyboard.Key.caps_lock,
	'shift' : pynput.keyboard.Key.shift,
	'shift_l' : pynput.keyboard.Key.shift_l,
	'shift_r' : pynput.keyboard.Key.shift_r,
	'ctrl' : pynput.keyboard.Key.ctrl,
	'ctrl_l' : pynput.keyboard.Key.ctrl_l,
	'ctrl_r' : pynput.keyboard.Key.ctrl_r,
	'alt' : pynput.keyboard.Key.alt,
	'alt_l' : pynput.keyboard.Key.alt_l,
	'alt_r' : pynput.keyboard.Key.alt_r,
	'alt_gr' : pynput.keyboard.Key.alt_gr,
	'space' : pynput.keyboard.Key.space,
	'home' : pynput.keyboard.Key.home,
	'page_up' : pynput.keyboard.Key.page_up,
	'page_down' : pynput.keyboard.Key.page_down,
	'end' : pynput.keyboard.Key.end,
	'enter' : pynput.keyboard.Key.enter,
	'insert' : pynput.keyboard.Key.insert,
	'backspace' : pynput.keyboard.Key.backspace,
	'cmd' : pynput.keyboard.Key.cmd,
	'cmd_l' : pynput.keyboard.Key.cmd_l,
	'cmd_r' : pynput.keyboard.Key.cmd_r,
	'delete' : pynput.keyboard.Key.delete,
	'print_screen' : pynput.keyboard.Key.print_screen,
	'scroll_lock' : pynput.keyboard.Key.scroll_lock,
	'f1' : pynput.keyboard.Key.f1,
	'f2' : pynput.keyboard.Key.f2,
	'f3' : pynput.keyboard.Key.f3,
	'f4' : pynput.keyboard.Key.f4,
	'f5' : pynput.keyboard.Key.f5,
	'f6' : pynput.keyboard.Key.f6,
	'f7' : pynput.keyboard.Key.f7,
	'f8' : pynput.keyboard.Key.f8,
	'f9' : pynput.keyboard.Key.f9,
	'f10' : pynput.keyboard.Key.f10,
	'f11' : pynput.keyboard.Key.f11,
	'f12' : pynput.keyboard.Key.f12,
	'f13' : pynput.keyboard.Key.f13,
	'f14' : pynput.keyboard.Key.f14,
	'f15' : pynput.keyboard.Key.f15,
	'f16' : pynput.keyboard.Key.f16,
	'f17' : pynput.keyboard.Key.f17,
	'f18' : pynput.keyboard.Key.f18,
	'f19' : pynput.keyboard.Key.f19,
	'f20' : pynput.keyboard.Key.f20,
	'f21' : pynput.keyboard.Key.f21,
	'f22' : pynput.keyboard.Key.f22,
	'f23' : pynput.keyboard.Key.f23,
	'f24' : pynput.keyboard.Key.f24,
	'menu' : pynput.keyboard.Key.menu,
	'media_volume_up' : pynput.keyboard.Key.media_volume_up,
	'media_volume_down' : pynput.keyboard.Key.media_volume_down,
	'media_volume_mute' : pynput.keyboard.Key.media_volume_mute,
	'media_next' : pynput.keyboard.Key.media_next,
	'media_previous' : pynput.keyboard.Key.media_previous,
	'media_play_pause' : pynput.keyboard.Key.media_play_pause,
	'pause' : pynput.keyboard.Key.pause,
	'num_lock' : pynput.keyboard.Key.num_lock,
	'\u0011' : 'q',
	'\u0017' : 'w',
	'\u0005' : 'e',
	'\u0012' : 'r',
	'\u0014' : 't',
	'\u0019' : 'y',
	'\u0015' : 'u',
	'\t' : 'i',
	'\u000f' : 'o',
	'\u0010' : 'p',
	'\u0001' : 'a',
	'\u0013' : 's',
	'\u0004' : 'd',
	'\u0006' : 'f',
	'\u0007' : 'g',
	'\b' : 'h',
	'\n' : 'j',
	'\u000b' : 'k',
	'\f' : 'l',
	'\u00f1' : 'ñ',
	'\u001a' : 'z',
	'\u0018' : 'x',
	'\u0003' : 'c',
	'\u0016' : 'v',
	'\u0002' : 'b',
	'\u000e' : 'n',
	'\r' : 'm'
}

#&  |
# key = "left"
# controler.press(matches[key])
# controler.release(matches[key])
# key = "page_down"
# controler.press(matches[key])
# controler.release(matches[key])
# key = "\r"
# controler.press(matches[key])
# controler.release(matches[key])
# key = "\u00f1"
# controler.press(matches[key])
# controler.release(matches[key])

# listener: pk.Listener
# idk = True
# def press(key):
# 	tecla = key.char if (type(key) == pk.KeyCode) else key.name
# 	print(tecla)
# 	idkL.append(tecla)

# 	if(key == pk.Key.esc):
# 		idk = False
# 		listener.stop()
# 		print("End")

# print("Start")
# listener = pk.Listener(on_press=press)
# listener.start()

# while idk:
# 	pass