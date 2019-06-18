#!/usr/bin/env python

# NEED TO CHANGE TERM CODE FOR IT TO WORK EACH TIME 
# SEEMS TO BE DROPPING COURSES FOR REASONS THAT AREN'T CLEAR; HAS MOST JRNL COURSES BUT ONLY ONE COMM COURSE
# FIXED BY GRABBING ALL ROWS ON THE PAGE INSTEAD OF TABLE FIRST, THEN ROWS. BECAUSE CHECK FOR CHECKBOX BEFORE ADDING TO TABLE, WORKS MORE SIMPLY
# https://stackoverflow.com/questions/15603561/how-can-i-debug-a-http-post-in-chrome
# Go to View>Developer Tools; Network; Filter to method:POST; Click on it and then Headers
# Also some instructions here: http://www.exegetic.biz/blog/2016/09/viewing-post-data/

import mechanize 
import lxml.html
import time
import urllib2
import scraperwiki
from datetime import datetime
from BeautifulSoup import BeautifulSoup


br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

departments = ['ACCT', 'AGRI', 'ANTH', 'CMNS', 'APSC', 'ARTH', 'ARTS', 'ASIA', 'ASTR', 'BIOL', 'BIOQ', 'HOPS', 'BUSI', 'BUQU', 'CCLS', 'CHEM', 'CHEQ', 'CADA', 'COMM', 'CAHS', 'CBSY', 'CPSC', 'CADD', 'COOP', 'CNPS', 'CRWR', 'CRIM', 'CUST', 'ECON', 'ECHS', 'EDUC', 'ENGL', 'ELST', 'ELSQ', 'ENGQ', 'ENTR', 'ENVI', 'EXCH', 'FASN', 'FMRK', 'FNSR', 'FINA', 'FIND', 'FREN', 'GEOG', 'GNIE', 'GNQU', 'GDMA', 'HCAP', 'HSCI', 'HAUC', 'HIST', 'HORT', 'HRMT', 'INFO', 'IDEA', 'IDSN', 'JAPN', 'JRNL', 'LGLA', 'LING', 'MAND', 'MRKT', 'MATQ', 'MATH', 'MUSI', 'NRSG', 'PHIL', 'PHYS', 'PHYQ', 'POST', 'POLI', 'DEPD', 'PSYN', 'PSYC', 'PRLN', 'PSCM', 'PUNJ', 'SOCI', 'SPAN', 'SETA', 'DETA', 'ZZZZ']

for department in departments:
    
#    try:

        url = "https://bweb.kwantlen.ca/pls/prodss/bwysched.p_select_term?wsea_code=ACAD"
        
        response = br.open(url)
        
        # response = br.open(url)
        
        # print response.read()
        
        # br.form = list(br.forms())[0]
        
        br.select_form(nr=0) # selects first form on the page
        
        for f in br.forms(): # these two lines show the form elements
            print f
        
        # br.form['term_code'] = '201520'
        
        br.form.set_all_readonly(False) # allow changing the .value of all controls
        
        name = ['201920',] # this is actual term code, should change this each term; will be 201530 for Fall 2015; need to change dummy below too
        
        for control in br.form.controls:
            if control.name == 'term_code':
                control.value = name
                name = '201910' # this is dummy term code, but seems to change (was 201510; not 201530); check POST form fields; doesn't seem to matter
        
        response = br.submit()
        
        html = response.read()
        
        # print html
        
        br.select_form(nr=0)
        
        for f in br.forms(): # these two lines show the form elements
            print f
        
        br.form.set_all_readonly(False) # allow changing the .value of all controls
        
        name = 'dummy'
        
        for control in br.form.controls:
            if control.name == 'sel_subj':
                control.value = name
                name = [department]
        
        response = br.submit()
        
        html = response.read()
        
        print html
        
        
        soup = BeautifulSoup(html)
                
        tables = soup.findAll("table", {"class" : "dataentrytable"})
        
        print 'Here are the tables'
        
        rows = soup.findAll("tr")
        
        for row in rows:
            
            cells = row.findAll("td")
            
            try:
                if "checkbox" in str(cells[0]):
                    
                    print 'NEW ROW'
                    
                    record = {}
                    record["department"] = department
                    record["uniqueid"] = str(datetime.now())
                    record["course"] = cells[1].text
                    record["CRN"] = cells[2].text
                    record["title"] = cells[3].text
                    record["credits"] = cells[4].text
                    record["campus"] = cells[5].text
                    record["instructor"] = cells[6].text
                    record["link"] = cells[7].text
                    record["max"] = cells[9].text
                    record["enrolled"] = cells[10].text
                    record["available"] = cells[11].text
                    record["waitlisted"] = cells[12].text
                    
                    print record
                    
                    scraperwiki.sqlite.save(['CRN'], record, table_name="data") # this should overwrite the CRN; if want discrete time entries should do it on uniqueid
                    scraperwiki.sqlite.save(['uniqueid'], record, table_name="overtime") # this should save, in a separate table, a new entry for every time it searches
                    
                else:
                    print 'No course data in this row'
                        
            except:
                print 'No course data in this row*'

#    except:
#        print "*** Didn't work for Department: " + department + " ***"
'''

print tables[1]

for table[1] in tables:
    print table
'''  
