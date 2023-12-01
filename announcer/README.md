# expen-announcer

[![Build Status](https://drone.sw.bthstudent.se/api/badges/SmoxBoye/expen-announcer/status.svg)](https://drone.sw.bthstudent.se/SmoxBoye/expen-announcer)

A Flask app that displays a simple Yes or No screen when expen is open.
This is done by having a WiFi enabled arduino module on site that polls a magnet reed switch on the shutter door. When a change is detected the Arduino sends a POST request to the Flask server.
The Arduino sends a heartbeat every X minutes to tell the server that it's alive.