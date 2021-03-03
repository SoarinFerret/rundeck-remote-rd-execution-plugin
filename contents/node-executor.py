#!/usr/bin/env python -u
import logging
import sys
import os
import json
import time
from pyrundeck import Rundeck

logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                    format='%(levelname)s: %(name)s: %(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('pyrundeck').setLevel(logging.WARNING)

log = logging.getLogger('remote-rundeck-node-executor')

if os.environ.get('RD_JOB_LOGLEVEL') == 'DEBUG':
    log.setLevel(logging.DEBUG)

def main():

    url = None
    if os.environ.get('RD_CONFIG_URL'):
        url = os.environ.get('RD_CONFIG_URL')

    verify_ssl = None
    if os.environ.get('RD_CONFIG_VERIFY_SSL'):
        verify_ssl = os.environ.get('RD_CONFIG_VERIFY_SSL')

    token = None
    if os.environ.get('RD_CONFIG_TOKEN'):
        token = os.environ.get('RD_CONFIG_TOKEN')

    version = 18
    if os.environ.get('RD_CONFIG_VERSION'):
        version = os.environ.get('RD_CONFIG_VERSION')

    id = None
    if os.environ.get('RD_CONFIG_ID'):
        id = os.environ.get('RD_CONFIG_ID')

    rundeck = Rundeck(url,token=token,api_version=version)

    run_info = rundeck.run_job(id)
    # needs some time to get ready on rundeck, otherwise may return errors
    time.sleep(1)

    print("Streaming log output from remote server:\n\n")
    lineindex = 0
    while rundeck.execution_state(exec_id=run_info['id'])['executionState'] == 'RUNNING':
        job_output = rundeck.execution_output_by_id(exec_id=run_info['id'])
        for x in job_output['entries'][lineindex:]:
            print(x['time'] + ": " + x['log'])
            lineindex += 1
        time.sleep(1)
        
    job_output = rundeck.execution_output_by_id(exec_id=run_info['id'])
    for x in job_output['entries'][lineindex:]:
        print(x['time'] + ": " + x['log'])
    print("\n\nFinished streaming log output from remote server")

    # Print Summary
    info = rundeck.execution_info_by_id(run_info['id'])

    print("\nJob finished with status: " + info['status'].upper())

    if 'successfulNodes' in info:
        print("\nSuccessful Nodes:")
        for n in info['successfulNodes']:
            print("\t" + n)

    if 'failedNodes' in info:
        print("\nFailed Nodes:")
        for n in info['failedNodes']:
            print("\t" + n)

    return 0


if __name__ == '__main__':
    main()