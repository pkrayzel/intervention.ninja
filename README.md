# intervention.ninja

The purpose of this project is to help people deal with difficult announcements to their friends / coworkers.

It uses multiple AWS resources.  

## Architecture overview

TBD

## Deployment


0) Prerequisies
    * already created AWS HostedZone with working name servers for the domain name and your domain register
    * terminal session with environment variables (KEY, TOKEN, ...) to work with AWS through aws cli (TBD how to)

1) Deploy CloudFormation stack https://github.com/pkrayzel/aws-static-site/blob/master/static_site.json
    * <strong>AcmCertificateArn</strong> -> ARN of your certificate in AWS Certificate Manager (in our case for domain names www.intervention.ninja, *.intervention.ninja and intervention.ninja)
    * <strong>DomainName</strong> -> intervention.ninja   
 
2) Run <strong>python deploy.py</strong> script from utils directory to deploy static content to target bucket
    

3) Deploy CloudFormation stack intervention_ninja.json