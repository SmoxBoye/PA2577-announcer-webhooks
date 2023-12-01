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

### frontend
The frontend contains acts as both the API and frontend. It contains no real logic. It runs as a microservice in that it can run in parallell which is then managed by a LoadBalancer.

### message_handler
The message_handler manages the logic for the frontend. It makes the database calls and sends messages to the webhook_manager. Im quite sure this could also be run as a microservice but i decided to keep the complexity down.

### webhook_manager
The webhook manager is what takes the webhooks from the database and queues them up for the workers.

### rabbitmq
Is the queue software i use, they have a nice Python package that made it easy to use.

### webhook_worker
The webhook workers are a microservice that takes webhook urls from the queue and runs them. They can switch between running a normal webhook and webhooks specifically designed for Discord

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

## Benefits, challenges and security
Let's get this out of the way. Security was completely omitted in this implementation.
The API is completely unsecured (look at prevous code on how it should be implemented. such as
`/heartbeat` and `/update`)

There is also no ratelimiting or filtering.

I have a plan to implement that dead webhooks will get removed after a while but never got to that.

Also right now the frontend and API run on the same service. This could work but i don't like it. Flask is not made to work as an API as it's not async.

In general though i like my implementation
Running the frontend in parallell makes it more resilient to higher loads and the calls to the database though the `message_mananger` are relatively lightweight. Techncially i could use a Redis cache aswell but that would be overkill. 

Im also satisfied with running the webooks though a queue. It makes it very easy to scale it (almost linearly) with how many webhooks you have in your database. 

The thing i had most difficulty with this project is getting the Services working properly and routing the connections internally.



