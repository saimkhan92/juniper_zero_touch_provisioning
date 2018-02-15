#!/usr/bin/python

# Import the necessary modules
import csv
import sys
from jinja2 import Template
from subprocess import call
import os
from shutil import copyfile

# Note: Junos image files and configuration files reside in the default apache2 directory /var/www/html
csv_filename="saim_device_data.csv"
conf_path="/var/www/html/"
device_data = csv.DictReader(open(csv_filename))
dhcpd_file="dhcpd.conf"
cwd=os.getcwd()
temp_dhcp_file_location=cwd+"/saim_dhcp_file/base_dhcpd.conf"
final_dhcp_file_location="/etc/dhcp/dhcpd.conf"
dhcpd_restart_command="sudo /etc/init.d/isc-dhcp-server restart"

# Remove existing dhcpd.conf and copy the base dhcp template text
try:
	os.remove("dhcpd.conf")
except OSError:
	pass
print("existing dhcpd.conf removed")

#copy base_dhcpd template to the newly created dhcpd.conf file
with open("base_dhcp/base_dhcpd.conf") as base_fh:
	base_dhcp_text=base_fh.read()
with open("dhcpd.conf","w+") as fh:
	fh.write(base_dhcp_text)
print("created new dhcpd.conf temp file")

# Parse csv file and perform required operation
for row in device_data:
	data=row
	
	# generate config files
	conffilename =  conf_path + row["hostname"] + ".conf"
	with open("saim_junos_conf_template.j2") as t_fh:
		t_format = t_fh.read()
	template = Template(t_format)
	
	fout = open(conffilename, 'w')
	print (fout)
	fout.write((template.render(data)))
	os.chmod(conffilename,0o777)
	
	# operation on dhcpd.conf file
	with open("saim_isc-dhcpd_template.j2") as t2_fh:
		t2_format = t2_fh.read()
	template2 = Template(t2_format)
	
	with open(dhcpd_file, "a") as dhcpdconf:
		dhcpdconf.write(template2.render(data))

print("dhcpd.conf file and configuration files created")
	
os.chmod(dhcpd_file,0o777)
copyfile(dhcpd_file,final_dhcp_file_location)
dhcpd_return_code = call(dhcpd_restart_command, shell=True)
	
	

