import argparse

from googleapiclient import discovery


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tool to whitelist an IP address for WFH access to concourse')
    parser.add_argument('ip', help='IP Address', type=list)
    parser.add_argument('project', help='Project name', type=str)

    return parser.parse_args()


def whitelist_security_list(project, authorized_networks):
    # We get the number of IPs and split them into chunks. Similar to how they'll be in the security policy rules
    ips_split_into_chunks = [authorized_networks[i:i + 10] for i in range(0, len(authorized_networks), 10)]
    compute_service = discovery.build('compute', 'v1')
    security_policies = compute_service.securityPolicies()
    concourse_policy = security_policies.get(project=project, securityPolicy='concourse-policy').execute()

    # Don't need the deny rule so we grab all the rules that have a policy action of allow
    allowed_rules = [policy for policy in concourse_policy['rules'] if policy['action'] == 'allow']

    allowed_rules_counter = 1

    # if len(allowed_rules) == len(ips_split_into_chunks): Checks to see if theres the same amount
    # of rules as IP chunks. If there is we don't have to do any editing of rules.
    # Just need to patch the rules with the IPs
    if len(allowed_rules) == len(ips_split_into_chunks):
        patching_allowed_rules(allowed_rules, allowed_rules_counter, project, security_policies,
                               ips_split_into_chunks)

    # len(ips_split_into_chunks) > len(allowed_rules): If there's more ip chunks then allowed rules, then add an
    # additional rule and put the ips in there.
    elif len(ips_split_into_chunks) > len(allowed_rules):
        allowed_rules_counter = patching_allowed_rules(allowed_rules, allowed_rules_counter, project, security_policies,
                                                       ips_split_into_chunks)
        for index, networks in enumerate(ips_split_into_chunks):
            body = {
                'kind': 'compute#securityPolicyRule',
                'priority': allowed_rules_counter,
                'action': 'allow',
                'preview': False,
                'match': {
                    'config': {
                        'srcIpRanges': networks
                    },
                    'versionedExpr': 'SRC_IPS_V1'
                }
            }
            security_policies.addRule(project=project, securityPolicy='concourse-policy',
                                      body=body).execute()
            allowed_rules_counter += 1

    # len(allowed_rules) > len(ips_split_into_chunks): If theres more allowed rules than ip chunks, then patch the
    # one rules with the IPs and remove the rule that isn't needed
    elif len(allowed_rules) > len(ips_split_into_chunks):
        for index, rule in enumerate(allowed_rules):
            if index > len(ips_split_into_chunks):
                break
            rule['match']['config']['srcIpRanges'] = ips_split_into_chunks[index]
            ips_split_into_chunks.pop(index)

            security_policies.patchRule(project=project, securityPolicy='concourse-policy',
                                        body=rule, priority=rule['priority']).execute()
            allowed_rules.pop(index)

        if len(ips_split_into_chunks) == 0:
            for rule in allowed_rules:
                security_policies.removeRule(project=project, securityPolicy='concourse-policy',
                                             priority=rule['priority']).execute()


def patching_allowed_rules(allowed_rules, allowed_rules_counter, project, security_policies, split_ips):
    for index, networks in enumerate(allowed_rules):
        networks['match']['config']['srcIpRanges'] = split_ips[index]
        split_ips.pop(index)
    for rule in allowed_rules:
        security_policies.patchRule(project=project, securityPolicy='concourse-policy',
                                    body=rule, priority=rule['priority']).execute()
        allowed_rules_counter += 1
    return allowed_rules_counter


def main():
    args = parse_arguments()
    whitelist_security_list(f'{args.project}', f'{args.ip}')


if __name__ == '__main__':
    main()
