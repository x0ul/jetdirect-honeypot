# IPP Setup
* Get a PPD file for a generic color postscript printer and copy to `/usr/share/ppd/custom/color-postscript.ppd` ([arbitrarily using this one](https://www.openprinting.org/printer/Generic/Generic-PostScript_Printer))
* Add and enable the "printer" using the command `/sbin/lpadmin -p color-laser -v socket://localhost:12000 -P /usr/share/ppd/custom/color-postscript.ppd -E`
* Listen to port 12000 with some program, done!

# JetDirect Setup
* Even easier than the IPP setup, merely listen on TCP port 9100

# systemd setup template
```
$ cat /etc/systemd/system/jetdirect-honeypot.service
[Unit]
Description=JetDirect honeypot server
After=network.target

[Service]
ExecStart=/home/faxspam/jetdirect-honeypot/jetdirect-honeypot.py -o /home/faxspam/jetdirect
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
```

```
$ cat /etc/systemd/system/ipp-honeypot.service
[Unit]
Description=IPP honeypot server
After=network.target

[Service]
ExecStart=/sbin/ippeveprinter -p 631 -r off --no-web-forms --no-website -v -P /usr/share/ppd/custom/HP-Color_LaserJet_9500.ppd -c /home/faxspam/ipp.py printer

[Install]
WantedBy=default.target
```

Remember to run `start` and `enable`
