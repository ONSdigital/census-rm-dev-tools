import argparse

from googleapiclient import discovery


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tool to whitelist an IP address for WFH access to concourse')
    parser.add_argument('ip', help='IP Address', type=list)
    parser.add_argument('project', help='Project name', type=str)

    return parser.parse_args()


def whitelist_security_list(project, whitelist):
    authorized_networks = whitelist
    split_ips = [authorized_networks[i:i + 10] for i in range(0, len(authorized_networks), 10)]
    compute_service = discovery.build('compute', 'v1')
    security_policies = compute_service.securityPolicies()
    concourse_policy = security_policies.get(project=project, securityPolicy='concourse-policy').execute()
    allowed_rules = [policy for policy in concourse_policy['rules'] if policy['action'] == 'allow']

    for index, networks in enumerate(allowed_rules):
        networks['match']['config']['srcIpRanges'] = split_ips[index]

    for rule in allowed_rules:
        security_policies.patchRule(project=project, securityPolicy='concourse-policy',
                                    body=rule, priority=rule['priority']).execute()


def main():
    args = parse_arguments()
    whitelist_security_list(f'{args.project}', f'{args.ip}')


if __name__ == '__main__':
    main()
