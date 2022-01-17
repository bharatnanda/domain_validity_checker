import yaml

email_config = None
domain_config = None

with open('config.yaml', 'r') as file:
    configuration = yaml.safe_load(file)
    email_config = configuration['domain_validator']['configuration']['email']
    domain_config = configuration['domain_validator']['configuration']['domains']
    expiration = configuration['domain_validator']['configuration']['expiration']['days']
    job_schedule = configuration['domain_validator']['configuration']['job']['scheule_time']