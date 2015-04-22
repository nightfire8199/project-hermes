def Print_Banner():
	
	print "   ___           _           _                        "                    
	print "  / _ \\_ __ ___ (_) ___  ___| |_       /\\  /\\___ _ __ _ __ ___   ___  ___" 
	print " / /_)/ '__/ _ \\| |/ _ \\/ __| __|____ / /_/ / _ \\ '__| '_ ` _ \\ / _ \\/ __|"
	print "/ ___/| | | (_) | |  __/ (__| ||_____/ __  /  __/ |  | | | | | |  __/\__ \\"
	print "\\/    |_|  \\___// |\\___|\\___|\\__|    \\/ /_/ \\___|_|  |_| |_| |_|\\___||___/"
	print "              |__/   \n"                                                     

def Print_Results(Artists, Albums, Tracks):

	R_Art = []
	R_Alb = []
	R_Tra = []

	if len(Artists) > 0:
		AR = 0
		print "\n...ARTISTS..............."
		for [artist] in Artists:
			print "AR" + str(AR), '\t', artist.encode("utf-8")
			R_Art.append(artist.encode("utf-8"))
			AR += 1
	if len(Albums) > 0:
		AL = 0
		print "\n...ALBUMS..............."
		for [album] in Albums:
			print "AL" + str(AL), '\t', album.encode("utf-8")
			R_Alb.append(album.encode("utf-8"))
			AL += 1
	if len(Tracks) > 0:
		T = 0
		print "\n...TRACKS..............."
		for [ident,artist,album,track,tracknum] in Tracks:
			print "T" + str(T), '\t', artist.encode("utf-8"), ' - ', album.encode("utf-8"), ' - ', track.encode("utf-8")
			R_Tra.append(ident)
			T += 1

	return [R_Art, R_Alb, R_Tra]

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
