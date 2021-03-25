import argparse
import json
import subprocess

import requests

GOOGLE_API_DASHBOARDS = 'https://monitoring.googleapis.com/v1/projects'


def main(project):
    command = ['gcloud', 'auth', 'print-access-token']
    access_token = subprocess.check_output(command).decode("utf-8")
    access_token = access_token.replace('\n', '')

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{GOOGLE_API_DASHBOARDS}/{project}/dashboards",
                            headers=headers)
    response.raise_for_status()

    dashboards = response.json()['dashboards']
    for dashboard in dashboards:
        delete_project_specific_keys(dashboard)
        sort_dashboard_by_widget_title(dashboard)
        file_name = f"{dashboard['displayName']}.json"
        with open(file_name, 'w') as export_file:
            json.dump(dashboard, export_file, indent=4)


def sort_dashboard_by_widget_title(dashboard):
    if 'mosaicLayout' in dashboard:
        dashboard['mosaicLayout']['tiles'] = sorted(dashboard['mosaicLayout']['tiles'],
                                                    key=lambda widget: widget['widget']['title'].lower())
    elif 'gridLayout' in dashboard:
        dashboard['gridLayout']['widgets'] = sorted(dashboard['gridLayout']['widgets'],
                                                    key=lambda widget: widget['title'].lower())


def delete_project_specific_keys(dashboard):
    del dashboard['etag']
    del dashboard['name']


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Script to dump dashboards (sorted by "title") to individual JSON files')
    parser.add_argument('project', help='Project', type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.project)
