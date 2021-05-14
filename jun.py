import mainconnect

w1 = 0
w2 = 0

for i in range(100):
	res = mainconnect.game(False, "srh", "srh", "test")
	w1 += res['w1']
	w2 += res['w2']

print("1st inn is", w1, "2nd inn is", w2)
