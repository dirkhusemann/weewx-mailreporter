# weewx-mailreporter

`weewx-mailreporter` is a [weewx](https://www.weewx.com) generator that reports weather reports through email.
It runs as report generator as part of the standard report generation process.

## Installation (zip)

Download the latest release from [weewx-mailreporter github repository](https://github.com/dirkhusemann/weewx-mailreporter).
Next, install using `wee_extension`:

    $ sudo wee_extension --install weewx-mailreporter.zip

## Installation (git clone)

Alternatively, you can clone [weewx-mailreporter github repository](https://github.com/dirkhusemann/weewx-mailreporter) and directly install from the clone:

    $ sudo wee_extension --install /path/to/weex-mailreporter/clone-directory

## Configuration

You need to obtain a Mastodon access token from the Mastodon account that you are using to toot the weather reports. 

Next, configure the `[[mastodon]]` subsection in the `[StdReport]` section:

    [[mastodon]]
        skin = mastodon

        HTML_ROOT = /var/mastodon
        access_token = insert your mastodon access token here
        api_base_url = the base api url of your mastodon instance; e.g., https://troet.cafe

		# I'm using metrics
        unit_system = metricwx
        enable = true

With that configuration `weex-mastodon` will post a status update every time your weewx instance does an archive run --- which might be a bit too chatty. 
You can change that by using the `report_timing` option:

    [[mastodon]]
        skin = mastodon

        HTML_ROOT = /var/mastodon
        access_token = insert your mastodon access token here
        api_base_url = the base api url of your mastodon instance; e.g., https://troet.cafe

		# I'm using metrics
        unit_system = metricwx
        enable = true

	    # Only report every 30 min
        report_timing = */30 * * * *
		
The `report_timing` option uses the crontab format and is described in [the weewx customization guide in more detail](https://www.weewx.com/docs/customizing.htm#customizing_gen_time).

## License

`weewx-mastodon` is distributed under the GPL3 License. 
The weewx installer code is based on `install.py` from [John A Kline's weewx-weatherboard repository](https://github.com/chaunceygardiner/weewx-weatherboard).