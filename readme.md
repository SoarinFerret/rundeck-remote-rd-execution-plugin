# Remote Rundeck Executor Plugin

Simple plugin to use the API of another Rundeck server to run a job. It then streams the output from the remote server back to your local server, and provides a summary of job run at the end.

## Requirements

* [pyrundeck](https://github.com/pschmitt/pyrundeck) - This plugin handles all the communication to the remote Rundeck server
  * To install `pip3 install pyrundeck`
