from domain_info import Domain
import csv, json, whois
from config_reader import email_config, domain_config, expiration, job_schedule
from email_util import send_mail
from datetime import datetime
import time
import schedule

dateformat = "%b %d %Y %H:%M:%S"

def get_domain_json_info(domain_name):
    try:
        who = whois.whois(domain_name)
    except whois.parser.PywhoisError as err:
        if 'No match for' in str(err):
            domain = Domain(domain_name = domain_name, available = True)
            return json.loads(str(domain))
    else:
        domain = Domain(domain_name = who.domain_name, registrar = who.registrar, \
            creation_date = who.creation_date, updated_date = who.updated_date, \
            expiration_date = who.expiration_date, state = who.state, \
            country = who.country)
        return json.loads(str(domain))

def find_about_to_expire_domains(domains, expiration_threshold_days):
    about_to_expire_domains = list()
    for domain in domains:
        if not domain['available']:
            time_to_expiration = datetime.strptime(domain['expiration_date'], dateformat) - datetime.now()
            if time_to_expiration.days < int(expiration):
                about_to_expire_domains.append((domain['domain_name'], str(time_to_expiration.days) + ' days left for domain expiry.'))
        else:
            about_to_expire_domains.append((domain['domain_name'], 'is available for registeration.'))
    return about_to_expire_domains

def json_domain_info_to_csv(json_domain_data, csv_file_path):
    csv_file = csv.writer(open(csv_file_path, "w+"))
    csv_file.writerow(["domain_name","registrar","state","country", \
        "creation_date","updated_date","expiration_date"])
    for domain in json_domain_data:
        if not domain['available']:
            csv_file.writerow([
                domain['domain_name'], 
                domain['registrar'], 
                domain['state'], 
                domain['country'], 
                domain['creation_date'], 
                domain['updated_date'],
                domain['expiration_date']
            ])

def domain_validation_task():
    domain_infos = list()
    print("Running domain validation job at : " + str(datetime.now()))
    try:
        for domain in domain_config:
            domain_infos.append(get_domain_json_info(domain))
        domain_expiration_details = find_about_to_expire_domains(domain_infos, expiration)
        email_message = 'Please find attached the domain expiration report.\nDomain expirationd details: \n'
        for expiration_detail in domain_expiration_details:
            if expiration_detail[0]:
                email_message = email_message + expiration_detail[0] + ' ' + expiration_detail[1] + "\n"
        json_domain_info_to_csv(domain_infos, 'domain_expiry.csv')
        send_mail(email_config['from'], email_config['to'], 'Domain Validation', email_message, files=['domain_expiry.csv'],
                    server=email_config['smtp_server'], port=email_config['smtp_port'], username=email_config['username'], password=email_config['password'],
                    use_tls=True)
    except Exception as err:
        print(" Exception occured " + err)
        send_mail(email_config['from'], email_config['to'], 'Domain Validation', 'Domain Validation Job has failed. Check the server ' + err,
                    server=email_config['smtp_server'], port=email_config['smtp_port'], username=email_config['username'], password=email_config['password'],
                    use_tls=True)

try:
    schedule.every().day.at(job_schedule).do(domain_validation_task)
    #Loop so that the scheduling task
    #keeps on running all time.
    while True:
        #Check whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1) #it will refersh every second
except schedule.ScheduleValueError as err:
    print(f'Unable to schedule the job :  reason :  {err}')