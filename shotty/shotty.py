import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2=session.resource('ec2')

def filter_instances(project):
    instances = []
    tags={}
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances=filter_instances(project)
    for i in instances:
        tags={t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no project>'))))

    return

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    instances=filter_instances(project)
    for i in instances:
        print("Stopping Instance {}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Starting EC2 Instances"
    instances=filter_instances(project)
    for i in instances:
        print("Starting Instance {}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    instances()
