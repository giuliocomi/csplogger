# csplogger
An endpoint to aggregate and analyze CSP violations across your infrastructure.
CSP logger is addressed to the ones that daily strive to implement a good CSP, free from 'unsafe-inline' and similar demons.
<br/>
<a href="https://raw.githubusercontent.com/empijei/wapty/master/LICENSE" rel="nofollow"><img src="https://camo.githubusercontent.com/dcb3a3de32cb31ae6a7edf80d88747f989878809/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d47504c76332d626c75652e737667" alt="License" data-canonical-src="https://img.shields.io/badge/license-GPLv3-blue.svg" style="max-width:100%;"></a>
<img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/giulio_comi?label=Follow&style=social">


## Why
Implementing a Content Security Policy free of issues and still secure is a pain.
Fortunately, the CSP can be configured in a "report only but do not block" mode (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only). With this modality and the directive 'report-uri', it is possible to plan a progressive CSP implementation hardening by monitoring the reports that the browsers of the employees send in the occasion of a violation. 

## Features
1) Essentiality and portability achieved with flask, sqlite and datastore
2) Dashboard that provides the capability for searching, filtering, ordering violations by type, timestamp, website, external resource, etc.
3) Configurable limits to prevent feature abuses (resource draining, unreliable results by spoofed/crafted logs)
4) Implemented with security in mind: hardened profiles for SECCOMP and Apparmor available.

Note: to successfully collect the violations occured from the browsers of the corporate users the endpoint must use a TLS certificate released by an internal Certificate Authority, otherwise the browsers will not send the violations automagically :-).

### How it (should) works

1) The endpoint is ideally reacheable from every network segment of the company
2) The intranet web applications or the corporate web proxies ensure that this header is set in HTTP responses:
```
    Content-Security-Policy-Report-Only: [HERE_THE_HARDENED_POLICY_TO_TEST]; report-uri https://[IP_OF_ENDPOINT]/log
```
3) Users daily navigate the intranet websites without any impact to their work while their browsers send "in background" the violations occured for every single resources loaded (js, css, image, etc.) that would be blocked by the desired CSP configuration.
4) Here comes the tricky part: make sense of all the data, addressing the violations per website, figure out if the policy should be deployed in a more permissive configuration or get rid of the resources in a way that ensures usability but also a more secure implementation.

### Installation
```
docker pull giuliocomi/csplogger
```
(https://cloud.docker.com/repository/docker/giuliocomi/csplogger/).

### Usage
This endpoint is best suited to run in a docker image deployed in the corporate intranet.

```
docker run -it -v [LOCAL_VOLUME]:/home/csplogger-agent/csplogger/databases/  giuliocomi/csplogger

```
Running the container with SECCOMP and Apparmor profiles enabled:
```
docker run --security-opt="apparmor:docker-csplogger-apparmor" --security-opt seccomp=seccomp-profile-csplogger.json  -v [LOCAL_VOLUME]:/home/csplogger-agent/csplogger/databases/ --cpus 1 --memory 512Mb giuliocomi/csplogger
```

#### Examples

(1) Dashboard

![alt text](https://i.imgur.com/te6WqwG.png)

(2) Simple demonstration of logging and analysing CSP violations across the intranet.

![alt text](https://i.imgur.com/rONO9sb.png)


## Issues
Spot a bug? Please create an issue here on GitHub (https://github.com/giuliocomi/csplogger/issues)

## License
This project is licensed under the  GNU general public license Version 3.
