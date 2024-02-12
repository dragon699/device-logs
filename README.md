# device-logs

device-logs is an application that connects to a serial port provided by a specific device and monitors for log entries from that port. Logs are then saved to a log file, which is mounted on the host system.

## Deploy
#### Locally
To deploy locally, you can just do `$ ./run.sh` when inside repository's root directory. This will build and create a docker container with the application.
This deployment method can accept 2 inputs that can be configured inside `run.sh` itself:
- `LOG_FILE` - Filename to write incoming log entries to. Will be mounted in `./logs` in repository's root directory.
- `SOURCE` - Source to read data from. Could be either a physical serial port from a device, or a virtual serial port created by the `socat` utility. If `SOURCE` is left empty, the former (`socat`) will be used and 2 virtual serial ports will be created inside the container.
  - a. The `entrypoint.sh` script that is part of the container will start simulating fake messages and send them to the first virtual port
  - b. The first virtual port will transmit the messages to the second one
  - c. The python application will read the messages from the second virtual port and put them in the log file defined in `LOG_FILE`
  - d. After receiving 10 messages, the container will shut down

If using a physical serial port, a. and b. (`socat` way) are not relevant.

#### In GitLab
To deploy in a GitLab CI job, fork this repository into your GitLab server (instance) as a new repository and the deployment will start from `.gitlab-ci.yml`. Using this deployment method, the docker image was pre-built in advance in my personal DockerHub repository, so `run.sh` is not relevant in this case.

Currently I did not include `variables:` section in the top level of `.gitlab-ci.yml`, so this deployment method requires `SOURCE` and `LOG_FILE` to be manually adjusted in the `.gitlab-ci.yml` file.

## Set-up a runner in GitLab
If using the second deployment method, you'd need to setup a runner in your GitLab instance. I've tested this on the GitLab cloud (non self-hosted way), so I had to use their shared runners to execute that. But it's completely okay to use it in your own runners.
To setup a new GitLab runner, follow the steps under [Register with a runner authentication token](https://docs.gitlab.com/runner/register/). You'd also need to make sure you have [GitLab runner package](https://docs.gitlab.com/runner/install/linux-repository.html) installed (`gitlab-runner`) in advance on the machine you plan to use as a runner.
