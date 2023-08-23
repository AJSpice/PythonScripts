import os
import csv
from jinja2 import Template

#gets the current working directory
cwd = os.getcwd()
#syntax for a relative path -- file = os.path.join(cwd, folder, "filename.type")

#creates empty list for file names later in the combine files function
final_configs = []

#specifies path that working files should be placed
output_directory = os.path.join(cwd, "working_configs")

#defines the working configs, jinja and csv paths
working_configs_path = os.path.join ('.' , "working_configs")
csvs = os.path.join('.', "csv_files")
j2s = os.path.join('.', "jinja_templates")

#defines function to create switch vlan configs
def vlan_config(output_dir):

    #loads in the j2 and csv files
    vlans_j2 = os.path.join(cwd, j2s, "VLANS-template.j2")
    vlans_csv = os.path.join(cwd, csvs , "VLANS.csv")

    with open(vlans_j2) as f:
        vlans_template = Template(f.read(), keep_trailing_newline=True)

    with open(vlans_csv) as f:
        reader = csv.DictReader(f)
        #create a dictionary to store the interface configurations for each device
        device_configs = {}
        for row in reader:
            device = row["Device"]
            #create a new entry in the dictionary for each device, if it doesn't exist already
            if device not in device_configs:
                device_configs[device] = ""
            #generate the interface configuration for this row using the Jinja template
            vlans_config = vlans_template.render(
                vlan_id=row["vlan_id"],
                vlan_name=row["vlan_name"],
            )
            #append this interface configuration to the configuration for this device
            device_configs[device] += vlans_config

        #save the interface configurations for each device to a separate file
        for device, config in device_configs.items():
            output_path = os.path.join(output_dir, f"{device}_vlan_configs.txt")
            with open(output_path, "w") as f:
                f.write(config)

#defines the function to create switchport configs
def switchport_config(output_dir):

    # Loads in the j2 and csv files
    cwd = os.getcwd()  # Get the current working directory
    switchports_j2 = os.path.join(cwd, j2s, "switchport-interface-template.j2")
    switchports_csv = os.path.join(cwd, csvs, "switch-ports.csv")

    # Opens and parses the j2 file and assigns it to a new variable
    with open(switchports_j2) as f:
        interface_template = Template(f.read(), keep_trailing_newline=True)

    # Opens the CSV
    with open(switchports_csv) as f:
        # Uses DictReader class to parse through each row of the CSV
        switchports_csv = csv.DictReader(f)
        # Create an empty dictionary to store the interface configurations for each device
        device_configs = {}
        for row in switchports_csv:
            device = row["Device"]
            # Create a new entry in the dictionary for each device, if it doesn't exist already
            if device not in device_configs:
                device_configs[device] = ""
            # Generate the interface configuration for this row using the Jinja template
            interface_config = interface_template.render(
                interface=row["interface"],
                type=row["type"],
                vlan=row["vlan"],
                voice_vlan=row["voice_vlan"],
                native_vlan=row["native_vlan"],
                lag_number=row["lag_number"],
                description=row["description"],
            )
            # Append this interface configuration to the configuration for this device
            device_configs[device] += interface_config

        # Save the interface configurations for each device to a separate file in the specified output directory
        for device, config in device_configs.items():
            output_path = os.path.join(output_dir, f"{device}_interface_configs.txt")
            with open(output_path, "w") as f:
                f.write(config)

#defines function for base config of Aruba6100
def base_config_6100(output_dir):

    #loads in the j2 and csv files
    base_config_j2 = os.path.join(cwd, j2s, "6100-template.j2")
    base_config_csv = os.path.join(cwd, csvs, "device_info.csv")

    with open(base_config_j2) as f:
        config_template = Template(f.read(), keep_trailing_newline=True)

    with open(base_config_csv) as f:
        reader = csv.DictReader(f)
        #create a dictionary to store the interface configurations for each device
        device_configs = {}
        for row in reader:
            device = row["switch_hostname"]
            #create a new entry in the dictionary for each device, if it doesn't exist already
            if device not in device_configs:
                device_configs[device] = ""
            #generate the interface configuration for this row using the Jinja template
            base_config = config_template.render(
                switch_hostname=row["switch_hostname"],
                mgmt_vlan=row["mgmt_vlan"],
                mgmt_vlan_name=row["mgmt_vlan_name"],
                mgmt_ip=row["mgmt_ip"],
                mgmt_ip_cidr=row["mgmt_ip_cidr"],
                gateway_ip=row["gateway_ip"],            
                system_location=row["system_location"]
            )
            #append this interface configuration to the configuration for this device
            device_configs[device] += base_config

        #save the interface configurations for each device to a separate file
        for device, config in device_configs.items():
            output_path = os.path.join(output_dir, f"{device}_base_config.txt")
            with open(output_path, "w") as f:
                f.write(config)

#defines function for base config of Aruba6300
def base_config_6300(output_dir):
    
    #loads in the j2 and csv files
    base_config_j2 = os.path.join(cwd, j2s, "6300-template.j2")
    base_config_csv = os.path.join(cwd, csvs, "device_info.csv")

    with open(base_config_j2) as f:
        config_template = Template(f.read(), keep_trailing_newline=True)

    with open(base_config_csv) as f:
        reader = csv.DictReader(f)
        #create a dictionary to store the interface configurations for each device
        device_configs = {}
        for row in reader:
            device = row["switch_hostname"]
            #create a new entry in the dictionary for each device, if it doesn't exist already
            if device not in device_configs:
                device_configs[device] = ""
            #generate the interface configuration for this row using the Jinja template
            base_config = config_template.render(
                switch_hostname=row["switch_hostname"],
                mgmt_vlan=row["mgmt_vlan"],
                mgmt_vlan_name=row["mgmt_vlan_name"],
                mgmt_ip=row["mgmt_ip"],
                mgmt_ip_cidr=row["mgmt_ip_cidr"],
                gateway_ip=row["gateway_ip"],            
                system_location=row["system_location"]
            )
            #append this interface configuration to the configuration for this device
            device_configs[device] += base_config

        #save the interface configurations for each device to a separate file
        for device, config in device_configs.items():
            output_path = os.path.join(output_dir, f"{device}_base_config.txt")
            with open(output_path, "w") as f:
                f.write(config)

#defines function to combine files
def combine_files():

    #list of strings to match in the filenames in the desired order
    strings = ['_base_config.txt', '_vlan_configs.txt', '_interface_configs.txt']

    #loop over the strings in the desired order
    for string in strings:
        #loop over the files in the working configs directory
        for og_file_name in os.listdir(working_configs_path):
            
            #check if the filename contains the current match string
            if string in og_file_name:
                
                #if a dash is in the file name, them the outfile name is the first 13 characters of the og filename 
                if "-" in og_file_name:
                    final_file_name = og_file_name[:13]
                elif "." in og_file_name:
                    if "." in og_file_name[:6]:
                        final_file_name = og_file_name[:13]
                    else:
                        final_file_name = og_file_name[:11]
                else:
                    final_file_name = og_file_name[:11]
                
                #specify the output and input file path
                output_file_path = os.path.join('.' , 'final_configs' , final_file_name + '.txt')
                input_file_path = os.path.join(working_configs_path, og_file_name)

                #tries to open and write the files, throwing an error code if failing
                try:
                    with open(input_file_path, 'r') as in_file:
                        contents = in_file.read()

                    with open(output_file_path, 'a') as out_file:
                        out_file.write(contents)
                        #flush the buffer to ensure immediate writing
                        out_file.flush()
                    
                    #appends the file names to the final configs list for use later
                    final_configs.append(final_file_name)

                except Exception as e:
                    print("Error:", e)

#prompts user for which model aruba needs to be configured
aruba_model = input("Which model of aruba needs to be configured? (6100,6300): ")

#check if its a proper model
while aruba_model not in ('6100', '6300'):
    aruba_model = input("This is an invalid input, please enter your Aruba Model: ")

#based on user response, runs the base config for the model of aruba
if int(aruba_model) == 6100:
    base_config_6100(output_directory)
elif int(aruba_model) == 6300:
    base_config_6300(output_directory)
    
#specify the output directory and call functions
vlan_config(output_directory)
switchport_config(output_directory)

#final function to combine files
combine_files()
