# Load test an oTree web app with Locust integrated Selenium

## Overview

This project aims to load/performance test an web experiment app developed by oTree framework. The web app can be deployed on Render or Heroku which is a one-stop web server supplier. Given oTree is a single-threaded framework, it appears that web apps based on that cannot be horizontally scaled up (I would be greatly aprreciated it If someone konws how to address the issue). Hence, I set up this project to load test my experimental web app (see [Conversation_experiment](https://github.com/GHCharlesLau/Conversation_experiment)) by vertically scaling up.

[Locust](https://locust.io/), as an open source load testing tool, is super user-friendly with pure python. We can define user behaviors with Python code rather than with complex UI-based tool such as JMeter. It is the biggest advantage of Locust that it can simulate thousands of simutaneous users within merely a single process becuase it is event-based (using gevent). Nevertheless, I have to give up this advantage and integrate driver-based [Selenium](https://www.selenium.dev/) in order to create bots that simulate real users as much as possible. After all, Selenium is quite resource-consuming.

## Descriptions

* `LocustSelenium.py` is the most useful to load test web experimental apps. The weakness is that it cannot test the response time of web servers exactly correctly because it does not exclude JS rendering time.
* `locustfile_new.py` is useful when we aim to test the capacity of handling Http request of the web server. It is completely written on top of Locust.

## How to use

## Conclusion
