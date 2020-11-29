from urllib.request import urlopen as open
import requests
from bs4 import BeautifulSoup as soup
import xlrd
import xlwt 
from xlwt import Workbook
import time
import random


def getLocation(url):


	if url.startswith('https://'):

		USER_AGENT = headers_list[random.randint(0, 18)]
		session = requests.Session()
		session.headers = {'user-agent': USER_AGENT}
		session.headers.update({'Referer': url}) 
		# user_agent = random.choice(user_agent_list)
		# headers = {'User-Agent': user_agent}
		req=session.get(url)
		if req.status_code==200:

			page_html=req.content

			page_soup=soup(page_html,"html.parser")

			profile_list=page_soup.findAll('li',{'class':'grid--cell ow-break-word'})

			loc_exists=profile_list[0].findAll('svg',{'class':'svg-icon iconLocation'})
			if loc_exists:
				location=profile_list[0].div.text.strip()
				locations.append(location)
			else:
				locations.append("No Location")
		else:
			locations.append("No Location")
	else:
		locations.append("No Location")




# url="https://stackoverflow.com/users/10306469/gian-luca-spadafora"
# getLocation(url)



headers_list = [
    "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
    " Firefox/41.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
    " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
    " Safari/601.3.9",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
    " Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
    " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
    " Edge/12.246",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "BrightSign/8.0.69 (XT1143)Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.11.2 Chrome/65.0.3325.230 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/41.0.2272.118 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 12871.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.103 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS armv7l 12371.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.146.3-Gen4_12000410) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true"

    ]



excel_path="dataset.xlsx"
inputWorkbook=xlrd.open_workbook(excel_path)
inputWorksheet=inputWorkbook.sheet_by_index(0)

timestamps=[]
owner_id=[]
tags=[]
votes=[]
views=[]
question_id=[]
question_body=[]

for i in range(1,inputWorksheet.nrows): 
	timestamps.append(inputWorksheet.cell_value(i,1))
	owner_id.append(inputWorksheet.cell_value(i,2))
	tags.append(inputWorksheet.cell_value(i,3))
	votes.append(inputWorksheet.cell_value(i,4))
	views.append(inputWorksheet.cell_value(i,5))
	question_id.append(inputWorksheet.cell_value(i,6))
	question_body.append(inputWorksheet.cell_value(i,7))


locations=[]
title="Locations"
locations.append(title)
counter=1

for id in owner_id:
	if counter>=150 and counter%150==0:
		time.sleep(200)
	getLocation(id)
	print(counter,"  ",id,"  ",locations[counter])
	counter=counter+1
	

wb=Workbook()
sheet1=wb.add_sheet('Sheet 1')
style=xlwt.easyxf('font: bold 1') 
sheet1.write(0,1,"Timestamp",style)
sheet1.write(0,2,"Owner Id",style)
sheet1.write(0,3,"Tags",style)
sheet1.write(0,4,"Votes",style)
sheet1.write(0,5,"Views",style)
sheet1.write(0,6,"Question Id",style)
sheet1.write(0,7,"Question Body",style)
sheet1.write(0,8,locations[0],style)

for i in range(1,len(timestamps)):
	sheet1.write(i,0,i)
	sheet1.write(i,1,timestamps[i])
	sheet1.write(i,2,owner_id[i])
	sheet1.write(i,3,tags[i])
	sheet1.write(i,4,votes[i])
	sheet1.write(i,5,views[i])
	sheet1.write(i,6,question_id[i])
	sheet1.write(i,7,question_body[i])
	sheet1.write(i,8,locations[i])

wb.save('dataset_with_locations.xlsx')
