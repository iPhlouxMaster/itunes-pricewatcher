import datetime
import urllib.request
import json
import smtplib
from email.mime.text import MIMEText
import time

#Create timestamp, open logfile
print('Initializing...')
timestamp = datetime.datetime.now().strftime('%Y-%m-%d @ %H:%M:%S')
log = open('log.txt', 'a')      

#Create dictionary of record upcs + pricing from file
records = {}
with open('records.txt') as f:
        for line in f:
                line = line.rstrip()
                (key, val) = line.split()
                records[int(key)] = val

#Call iTunes API to check pricing on items
print('Connecting to iTunes...')

for key in records:

        #Build query by concatenating url + record id, trigger api call
        query = 'https://itunes.apple.com/lookup?id={}'.format(key)
        response = json.loads(urllib.request.urlopen(query).read().decode('utf-8'))['results']

        #Parse JSON, compare price
        if response:
                title = response[0]['collectionName']
                old_price = float(records[key])
                new_price = float(response[0]['collectionPrice'])

                if old_price > new_price:
                        print('Change to {}! [{} > {}]'.format(title, old_price, new_price))
                        log.write(timestamp + ': Change to {} [{} > {}]'.format(title, old_price, new_price))

##                        sms = MIMEText('iTunes price drop detected!')
##                        sms['From'] = 'sender@domain.com'
##                        sms['To'] = 'recipient@domain.com'
##
##                        s = smtplib.SMTP('smtp.gmail.com', 587)
##                        s.ehlo()
##                        s.starttls()
##                        s.login('username', 'password')
##                        s.sendmail('sender@domain.com', 'recipient@domain.com', sms.as_string())
##                        s.quit()
                
                else:
                        print('No change to {}'.format(title))
                        log.write(timestamp + ': No change to {}\n'.format(title))
        else:
                log.write(timestamp + ': No match for {}\n'.format(key)) 

print('Finalizing...')
log.write('-' * 25 + '\n')
log.close()
f.close()

print('Complete!')
time.sleep(2)

exit
