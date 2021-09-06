# ddnsdaemon

A simple python script that gathers data from the clients on which it is installed for monitoring purposes

# Crontab

## install the daemon

* clone the project `git clone https://github.com/takamaka-dev/ddnsdaemon.git'
* enter the project directory `cd ddnsaemon`
* setup the virtual env `python3.9 -m venv /home/ddns/ddnsdaemon/6FeetUnder`
* activate the env
* install the required packages:
  * `pip install wheel`
  * `pip install requests flask_restful http configparser waitress`
* Call `python main.py` The first call will fail by creating stubs of the configuration files
* update the `*.properties` files with the correct settings
* Call `python main.py` to run the server in foregroud

## run service-like

Assuming to you have downloaded the daemon in the following path `/home/ddns/ddnsdaemon` and the virtual env with name `6FeetUnder` inside the daemon folder


```bash
crontab -e
```

The call with execution every 5 minutes:

```crontab
*/5 * * * * cd /home/ddns/ddnsdaemon && screen -d -m /home/ddns/ddnsdaemon/6FeetUnder/bin/python main.py
```

## call update

The ddnsdaemon must be called periodically to collect data from the machine on which it is installed. This is a simple
example of a timed call that takes advantage of the crontab daemon.

I create a file with the curl call to the update route.

```bash
#!/bin/bash
curl -X GET 'http://localhost:13131/cronjob'
```
Assuming to have created the file with name `call.sh` in the path `/home/ddns/call.sh` I proceed to assign it the execution permissions:

```bash
chmod 755 /home/ddns/call.sh
```

To finish I set the crontab call with the command:

```bash
crontab -e
```

The call with execution every minute:

```crontab
* * * * * /home/ddns/call.sh
```


