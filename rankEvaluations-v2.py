from __future__ import division
from ranking import Ranking
from mx.DateTime import *
from scipy.stats import chisquare
from scipy.stats import f_oneway
import os
import getopt
import csv
import sys


def usage(): 
	help = ''
	help = """ 
	This is the help docstring of RankEvaluation. This is a very simple (and sometimes even candid) Python script that perform a ranking of evaluations expressed in an ordinal scale.

	Requirements: Python 2.7, scipy, ranking and mx packages. 
	Input options: 
		-h :: to display this help
		-i :: to specify the input file
		-d :: to set the debug mode ON (default is OFF)
		
	Inputs: The script takes in input a CSV with header which represents ordinal evaluations on n items (from 1, lowest to m, highest value); 
	Outputs: According to single evaluations and corresponding rankings, the script provides a global ranking for the items.
	
	Released under the Creative Commons License 2013 by F Cabitza
	"""
	print help
	
def main():
	starttime= now()
	classifica = [0]
	#vittorie = [0]
	unsorted_scores = [0]
	numerovalutazioni = [0]
	#true_ranking = [0]
	medie = [0.00]
	input = ''
	path = './%s' % (input)
	outputfile = ''
	newrow = ''
	logfile= ''
	singololog = ''
	righe = 0
	nomefile = ''
	debugmode = False
	
	try:
		options, remainder = getopt.getopt(sys.argv[1:], 'hi:d', ["help", "input=", "debug"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	for o, a in options:
		#print 'o : %s; a: %s' % (o, a)
		if o in ("-i", "--input"):
			nomefile = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-d", "--debug"):
			debugmode = True
		else:
			assert False, "unhandled option"
	
	if debugmode:
		print singololog 
	logfile = logfile + singololog
	singololog = "Script started! (v. 3)\n\n"
	print singololog 
	logfile = logfile + singololog
	if nomefile =='':
		nomefile= sys.argv[1]
	with open(nomefile, 'rb') as csvfile:
		voti = csv.reader(csvfile, delimiter=',', quotechar='|')
		items=voti.next()
		numeroItem = len(items)
		for elem in items:
			parola = str(elem)
			outputfile = outputfile + parola.strip(' []\'\"') + ','
		outputfile = outputfile.strip(',') +'\n'
		singololog= "Number of items: %d; Items: %s \n" %(numeroItem, outputfile) 
		if debugmode:
			print singololog 
		logfile = logfile + singololog

		i=0
		while (i < (numeroItem-1)):
			classifica.append(0)
			unsorted_scores.append(0)
			medie.append(0.00)
			numerovalutazioni.append(0)
			i+=1
		podio = [[0, 0, 0] for i in range(numeroItem)]
		fasce = [[0, 0] for i in range(numeroItem)]
		true_ranking = [0 for i in range(numeroItem)]
		true_vittorie = [0 for i in range(numeroItem)]
		vittorie = [0 for i in range(numeroItem)]
		margini = [0 for i in range(numeroItem)]
		
		for row in voti:
			singololog = "About to process row no. %d , that is: %s \n" % (righe, row)
			if debugmode:
				print singololog
			logfile = logfile + singololog
			j = 0
			indice = 0
			for elem in row:
				#print "gestisco %s \n" % elem
				if ((elem != '') and (elem != '.')): 
					unsorted_scores[j] = int(elem)
					numerovalutazioni[j] += 1
					#confronti per l'R2
					for secondelem in row:
						if ((secondelem != '') and (secondelem != '.')):
							if(j != indice):
								margine = int(elem) - int(secondelem)
								if(margine > 0):
									vittorie[j] += 1
								margini[j] = margini[j] + margine
							indice += 1 
						
				else:
					unsorted_scores[j] = None
				j += 1
			
			singololog = '====Evaluations: ' + str(unsorted_scores) + '=======\n'
			if debugmode:
				print singololog 
			logfile = logfile + singololog
			input = sorted(unsorted_scores, reverse=True)
			singololog =  'Ordered evaluations: ' + str(input) + '\n'
			if debugmode:
				print singololog 
			logfile = logfile + singololog
			classifica_parziale = {}
			for rank, score in Ranking(input, no_score=''):
				singololog = 'rank: %s, score %s \n' % (rank, score)
				if debugmode:
					print singololog
				logfile = logfile + singololog
				if rank != None:
					classifica_parziale[score] = rank + 1
				else:
					classifica_parziale[score] = 0
			singololog = 'Partial classification: ' + str(classifica_parziale) + '\n'
			if debugmode:
				print singololog 
			logfile = logfile + singololog
			singololog = 'Old classification: ' + str(classifica) + '\n'
			if debugmode:
				print singololog
			logfile = logfile + singololog
			newrow = ''
			for variabile in range(numeroItem):
				valutazione = unsorted_scores[variabile]
				if valutazione in classifica_parziale:
					if valutazione != None:
						posizione = classifica_parziale[valutazione]
						classifica[variabile] = classifica[variabile] + posizione
						singololog = 'New position (variabile): ' + str(posizione) + '(' + str((variabile+1)) + 'a)' + '\n'
						if debugmode:
							print singololog
						logfile = logfile + singololog
						newrow = newrow + str(posizione) + ','
						if posizione == 1:
							podio[variabile][0] += 1
							fasce[variabile][0] += 1
						if posizione == 2:
							podio[variabile][1] += 1
							fasce[variabile][0] += 1
						if posizione == 3:
							podio[variabile][2] += 1
							fasce[variabile][0] += 1
						if posizione >3:
							fasce[variabile][1] += 1
					else:
						newrow = newrow + ','
				else:
					newrow = newrow + ',' 
			singololog = 'New classification: ' + str(classifica) +'\n'
			if debugmode:
				print singololog
			logfile = logfile + singololog
			newrow = newrow.strip(',')
			outputfile = outputfile + newrow + '\n'
			righe += 1
	numerocasi = righe 
	singololog = str(numerovalutazioni) + '\n'
	if debugmode:
				print singololog
	logfile = logfile + singololog
	for i in range(numeroItem):
		#print "%d ) %d fratto %d" %(i, classifica[i], numerovalutazioni[i])
		if numerovalutazioni[i] != 0:
			medie[i] = round((classifica[i] / numerovalutazioni[i]), 2)
		#else:
			#medie[i] = 0

	summary = ''

	singololog = '\n**********\n\n'
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	singololog= "Cases processed: %d \n" % numerocasi
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	singololog = "Items: " + str(items) + '\n' + 'Final Ranking: ' + str(classifica) + '\n' + 'Mean rankings: ' + str(medie) + '\n' 
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	
	singololog= "Items: " + str(items) + '\n' + 'Cumulated Margins: ' + str(margini) + '\n'
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	
	singololog = "Items: " + str(items) + '\n' + 'Final Number of victories: ' + str(vittorie) + '\n' 
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	
	medie_ordinate = sorted(medie, reverse=False) 
	vittorie_ordinate = sorted(vittorie, reverse=True)
	singololog = 'Ordered means of rankings: ' + str(medie_ordinate) + '\n'
	singololog = singololog + 'Ordered set of victories: ' + str(vittorie_ordinate) + '\n'
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	kappa = -1
	for value in medie_ordinate:
		#print "**** il valore da cercare = " + str(value)
		iter = -1
		entrato = False
		for media in medie:
			#print "sto valutando la media: " + str(media)
			iter += 1
			#print "posizione = " + str(iter)
			#print entrato
			if (media == value) and not(entrato):
				#print "entrato"
				kappa += 1
				#print "kappa = " + str(kappa)
				#print "iter = " + str(iter)
				#print "true_ranking before= " + str(true_ranking)
				true_ranking[kappa] = items[iter]
				#print "true_ranking after= " + str(true_ranking)
				entrato = True

	singololog = 'True ranking of items (according to relative rankings): ' + str(true_ranking) + '\n\n' 
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog
	
	kappa = -1			
	for value in vittorie_ordinate:
			#print "**** il valore da cercare = " + str(value)
			iter = -1
			entrato = False
			for vittoria in vittorie:
				#print "sto valutando la vittoria: " + str(vittoria)
				iter += 1
				#print "posizione = " + str(iter)
				#print entrato
				if (vittoria == value) and not(entrato):
					#print "entrato"
					kappa += 1
					#print "kappa = " + str(kappa)
					#print "iter = " + str(iter)
					true_vittorie[kappa] = items[iter]
					entrato = True				
				
	singololog = 'True ranking of items (according to number of victories): ' + str(true_vittorie) + '\n\n' 
	if debugmode:
		print singololog
	logfile = logfile + singololog
	summary = summary + singololog

	k = 0
	for variabile in podio:
		chipodio, pvaluepodio = chisquare(variabile)
		chifasce, pvaluefasce = chisquare(fasce[k])
		singololog = str(k+1) + ') Analysis for ' + str(items[k]) + '\n\t' + 'No. of cases: ' + str(numerovalutazioni[k]) + '\n\t' + 'Mean position: ' + str(medie[k]) + '\n\t' + 'Distribution in the first 3 ranks: ' + str(variabile) + '\n\t' + 'Distribution in the 2 priority levels: ' + str(fasce[k]) + '\n\t' + " The analysis of uniformity bwt ranks is: Chi Square: %.4f, P-value: %.4f " % (chipodio, pvaluepodio) + '\n\t' + "The analysis of uniformity bwt rank levels is: Chi Square: %.4f, P-value: %.4f " % (chifasce, pvaluefasce) + '\n\n'
		if debugmode:
				print singololog
		logfile = logfile + singololog
		summary = summary + singololog
		#singololog =  
		#print singololog if not debugmode
		#logfile = logfile + singololog
		#summary = summary + singololog
		k +=1
	#k = 0
	#for variabile in fasce:
	#	singololog = str(k) + ') Analysis for ' + str(items[k]) + '\n'
	#	print singololog if not debugmode
	#	logfile = logfile + singololog
	#	summary = summary + singololog
	#	chi, pvalue = chisquare(variabile)
	#	singololog = "On input: " + str(variabile) + " the analysis of uniformity bwt rank levels is: \n Chi Square: %.4f, P-value: %.4f \n" % (chi, pvalue) 
	#	print singololog if not debugmode
	#	logfile = logfile + singololog
	#	summary = summary + singololog
	#	k +=1

	endtime= now()
	executiontime = endtime - starttime
	timestamp = str(now())
	timestamp = timestamp.replace(' ', '-')
	timestamp = timestamp.replace(':', '')
	nomefile = nomefile.rstrip('.csv')
	singololog= 'Now writing the summary file... \n'
	if debugmode:
				print singololog
	logfile = logfile + singololog
	path = './' + nomefile + 'summary' + '-' + timestamp + '.txt'
	dataoutput = open(path,'w')
	dataoutput.write( summary )	
	dataoutput.close()
	singololog= 'Now writing the output file... \n'
	if debugmode:
				print singololog
	logfile = logfile + singololog
	path = './' + nomefile + 'piazzamenti' + '-' + timestamp + '.csv'
	dataoutput = open(path,'w')
	dataoutput.write( outputfile )	
	dataoutput.close()
	singololog= 'Now writing the log file... \n'
	if debugmode:
				print singololog
	logfile = logfile + singololog
	path = './' + nomefile + 'log' + '-' + timestamp + '.txt'
	dataoutput = open(path,'w')
	dataoutput.write( logfile )	
	dataoutput.close()

	singololog = 'End of computation after ' + str(executiontime) + '. Exit.'
	print singololog

if __name__ == "__main__":
	main()
