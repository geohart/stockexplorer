#import libraries and setup parser
from BeautifulSoup import BeautifulSoup,NavigableString
import urllib2, sys, datetime
from datetime import timedelta

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# get yesterday's date (runs at 9PM PT/4AM UTC)
myDate = datetime.date.today() - timedelta(1)

# get output file
fileDate = myDate.strftime("%m%d%Y")
f = open('/srv/web/ghart.org/stockexplorer/quotes/data/quotes_' + fileDate + '.csv', 'w')

for letter in alphabet:

	# set webpage address
	address = "http://wsj.com/mdc/public/page/2_3048-usmfunds_" + letter + "-usmfunds.html"

	print letter + ": " + address

	# get html from page
	html = urllib2.urlopen(address).read() 

	# parse
	soup = BeautifulSoup(html)

	# get all trs from closing price table
	quoteTable = soup.find('table', 'mdcTable')
	rows = quoteTable.findAll('tr')

	# Helper function to return concatenation of all character data in an element
	def parse_string(element):
		 text = ''.join(element.findAll(text=True))
		 return text.strip()
			 
	# get today's date
	today = myDate.strftime("%A %B %d %Y")
	numToday = myDate.strftime("%w %m %d %Y")

	# cycle through rows in table
	for row in rows[1:]:
		if len(row.contents) > 3:
			# get cells
			cells = row.findAll('td')

			# set variables
			name = cells[0].contents[1].string
			symbol = cells[1].contents[1].string
			nav = cells[2].string
			change = cells[3].string
			ytdReturn = cells[4].string
			threeYearPercentChange = cells[5].string

			# format change
			if change == "...":
				change = "0"

			# print in csv format
			result =  today + "," + numToday + "," + name + "," + symbol + "," + nav + "," + change + "," + ytdReturn + "," + threeYearPercentChange + "\n"
			f.write(result)
	f.flush()

print "...Done!"

f.close()
