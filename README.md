# csplogger
An endpoint to aggregate and analyze CSP violations across your infrastructure.

CSP logger is addressed to the ones that daily strive to implement a good CSP, free from 'unsafe-inline' and similar demons.

## Why
Implementing a Content Security Policy free of issues and still secure is a pain.
Fortunately, the CSP can be configured in a "report only but do not block" mode (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only). With this modality and the directive 'report-uri', it is possible to plan a progressive CSP implementation hardening by monitoring the reports that the browsers of the employees send in the occasion of a violation. 

## Features
1) Essentiality and portability achieved with flask, sqlite and datastore
2) Dashboard that provides the capability for searching, filtering, ordering violations by type, timestamp, website, external resource, etc.
3) Configurable limits to prevent feature abuses (resource draining, unreliable results by spoofed/crafted logs)

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
docker pull giuliocomi/csplogger:latest
```
(https://cloud.docker.com/repository/docker/giuliocomi/csplogger/).

### Usage
This endpoint is best suited to run in a docker image deployed in the corporate intranet.

```
docker run giuliocomi/csplogger:latest
```
Running the container with a SECCOMP profile:
```
docker run --security-opt seccomp=seccomp-profile-csplogger.json giuliocomi/csplogger:latest
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
