def Print_Banner():
	
	print "   ___           _           _                        "                    
	print "  / _ \\_ __ ___ (_) ___  ___| |_       /\\  /\\___ _ __ _ __ ___   ___  ___" 
	print " / /_)/ '__/ _ \\| |/ _ \\/ __| __|____ / /_/ / _ \\ '__| '_ ` _ \\ / _ \\/ __|"
	print "/ ___/| | | (_) | |  __/ (__| ||_____/ __  /  __/ |  | | | | | |  __/\__ \\"
	print "\\/    |_|  \\___// |\\___|\\___|\\__|    \\/ /_/ \\___|_|  |_| |_| |_|\\___||___/"
	print "              |__/   \n"                                                     

def Print_Results(Artists, Albums, Tracks):

	print "\n...ARTISTS..............."
	for [artist] in Artists:
		print artist.encode("utf-8")
	print "\n...ALBUMS..............."
	for [album] in Albums:
		print album.encode("utf-8")
	print "\n...TRACKS..............."
	for [ident,artist,album,track] in Tracks:
		print ident, '\t', artist.encode("utf-8"), ' - ', album.encode("utf-8"), ' - ', track.encode("utf-8")

def intersect(res, inp):
	if(len(res) == 0):
		for row in inp:
	    		 res.add(row)
	else:
		temp = set()
		for row in inp:
	    		 temp.add(row)
		res = res.intersection(temp)
	return res
