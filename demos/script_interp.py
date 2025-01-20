import subprocess

# List of arguments to pass to the script
iterations = 21
args_list = []

for i in range(iterations):
	iteration = float(i) / (float(iterations) - 1)
	mesh_path = 'C:/Users/anshu/source/repos/Neural-TSpline/output_obj/interp/spot_cow_head_reconstructed' + str(iteration) + '.obj' # ogre_reconstructed
	output_path = 'C:/Users/anshu/source/repos/Neural-TSpline/output_obj/interp/png/spot_cow_head_reconstructed_' + str(str(i).zfill(4)) + '.png'
	args_list.append([mesh_path, output_path])

# Name of the Python script you want to run
script_name = "./demo_balloon.py"

# Loop through the list of arguments
for args in args_list:
	# Build the command with the script name and arguments
	command = ["python", script_name] + args
	
	# Run the command using subprocess.run
	print(f"Running: {command}")
	result = subprocess.run(command, capture_output=True, text=True)
	
	# Print the output (if any) of the command
	print(result.stdout)
	print(result.stderr)
