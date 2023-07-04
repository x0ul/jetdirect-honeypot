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

# Testing IPP
Use `ipptool`, part of *cups*, to test IPP printing. Save the
following print job definition into a file. The `mimeMediaType` field
and the printer-uri may need to be modified to fit the printer. Play
around.

```
{
    VERSION 2.0
    OPERATION Print-Job
    REQUEST-ID 42

    GROUP operation-attributes-tag
    ATTR charset "attributes-charset" "utf-8"
    ATTR naturalLanguage "attributes-natural-language" "en"
    ATTR uri "printer-uri" "ipp://printer.example.com/ipp/print"
    ATTR name "requesting-user-name" "John Doe"
    ATTR mimeMediaType "document-format" "application/postscript"

    FILE "testfile"
}
```
To send a job, run `ipptool http://<your-printer-here>:631/ipp/print <path-to-job-definition>`. You may also need/want to modify the `/ipp/print` part of the URI.

# Testing JetDirect
Simply use `nc` to send a file, eg. `nc -N <host> 9100 < some_file`.
The `-N` flag causes `nc` to `shutdown` the socket before closing,
otherwise it may hang.
