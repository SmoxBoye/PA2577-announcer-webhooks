# PA2577 assignment build something

## Intro
In this assignment I've added webhooks and a database to a previous project of mine.
The idea is to extend expen.bthstudent.se with webhooks.
expen.bthstudent.se (also called Announcer) is a project that i finished about a month ago.
It uses an arduio that uses a magnetic reedswitch to detect when Expen (the student cafeteria) has opened their shutter door (i.e when they're open) and displays it on a website.

For this project i've opened an unsecure API that let's use emulate the arduino and also add webhooks.

## Structure
The Service is built up of two microservices acting as the frontend and the webhook workers.
There are also two intermediate services that layer the responsibilities.
(These could technically be merged but i thought it was more interesting to add more layers).

Structure more visually

User <->[frontend, frontend, ..] <-> message_handler <-> webhook_handler --> rabbitmq --> webhook_worker

both the webhook_handler and message_handler talk to the database

## How to run
I wanted to try to selfhost my own image registry so the images are hosted on registry.smoxboye.com
With the handin i will provide a Makefile that sets everything up. 
The reason it's not in this repo is due to it containing the cedidentials for the PA2577 account on the registry.

First run
`make login-kube`
To login kubernetes to my registry.

If you're on Windows run
`make upw`
and if you're on Linux run
`make upl`

To turn everything off run
`make down`

The service should now be available at
http://localhost:3000

### To make it easy to interact with i compiled a few tools in Go.
**(I HAVE NOT TESTED ANYTHING THAT RUNS ON LINUX)**
To send a simulated API open call run
`make openw` on Windows
`make openl` on Linux

To send a simulated API close call run
`make closew` on Windows
`make closel` on Linux

To add a webhook run
`cd util_tool`
and run either
`./add_webhook.exe [webhook]`
or 
`add_webhook [webhook]`

example:
`./add_webhook https://www.example.com`

