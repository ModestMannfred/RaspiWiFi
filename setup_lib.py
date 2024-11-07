import os

def install_prereqs():
	os.system('apt update')
	os.system('apt install python3 python3-rpi.gpio python3-pip python3-flask -y')
#	print("Installing Flask web server...")
#	print()
#	os.system('pip3 install flask pyopenssl')

def configure_ap(entered_ssid, wpa_enabled_choice, wpa_entered_key):
	os.system('mkdir -p /usr/lib/raspiwifi')
	os.system('mkdir -p /etc/raspiwifi')
	os.system('cp -a libs/* /usr/lib/raspiwifi/')
# TODO(kem): add localization de?

	# Disable and deactive dnsmasq (probably disable is sufficient due to restart)
#	os.system('systemctl is-enabled --quiet dnsmasq && systemctl disable dnsmasq')
#	os.system('systemctl is-active --quiet dnsmasq && systemctl stop sndmasq')

	os.system('nmcli con add type wifi ifname wlan0 mode ap con-name wifi-hotspot ssid ' + entered_ssid + ' autoconnect true')
# TODO(kem): where is this stuff set?
#	os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
#	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')
# TODO(kem): missing, driver=n180211, wpa=2
# TODO(kem): extra, band=bg, group=ccmp
# TODO(kem): missing, dhcp-range=10.0.0.10,10.0.0.15,12h
#			dhcp-mac=...
#			dhcp-reply-delay=...
#			address=/raspiwifisetup.com/10.0.0.1
#			address=/idliketoconfigurethewifionthisdevicenowplease.com/10.0.0.1 

	os.system('nmcli con modify wifi-hotspot connection.autoconnect-priority -999')
	os.system('nmcli con modify wifi-hotspot wifi.band bg')
	os.system('nmcli con modify wifi-hotspot wifi.channel 1')

	if wpa_enabled_choice.lower() == "y":
		os.system('nmcli con modify wifi-hotspot wifi-sec.key-mgmt wpa-psk')
		os.system('nmcli con modify wifi-hotspot wifi-sec.auth-alg open')
		os.system('nmcli con modify wifi-hotspot wifi-sec.proto rsn')
		os.system('nmcli con modify wifi-hotspot wifi-sec.group ccmp')
		os.system('nmcli con modify wifi-hotspot wifi-sec.pairwise ccmp')
		os.system('nmcli con modify wifi-hotspot wifi-sec.psk "' + wpa_entered_key + '"')
	
	os.system('nmcli con modify wifi-hotspot ipv4.method shared ipv4.address 10.0.0.1/24')
	os.system('nmcli con modify wifi-hotspot ipv6.method disabled')

	os.system('mkdir /etc/cron.raspiwifi')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/ap_bootstrapper /etc/cron.raspiwifi')
	os.system('chmod +x /etc/cron.raspiwifi/ap_bootstrapper')
	os.system('echo "# RaspiWiFi Startup" >> /etc/crontab')
	os.system('echo "@reboot root run-parts /etc/cron.raspiwifi/" >> /etc/crontab')
	os.system('mv /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf /etc/raspiwifi')

def update_main_config_file(ssl_enabled_choice, server_port_choice):
	if ssl_enabled_choice.lower() == "y":
		os.system('sed -i \'s/ssl_enabled=0/ssl_enabled=1/\' /etc/raspiwifi/raspiwifi.conf')
	if server_port_choice != "":
		os.system('sed -i \'s/server_port=80/server_port=' + server_port_choice + '/\' /etc/raspiwifi/raspiwifi.conf')
