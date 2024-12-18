import subprocess

def get_installed_programs():
    # Define the registry keys where installed programs are listed

    registry_keys = [

        r'HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall',

        r'HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',

        r'HKU\S-1-5-18\Software\Microsoft\Windows\CurrentVersion\Uninstall',

        r'HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall'

    ]

    installed_programs = []

    for key in registry_keys:

        # Query each registry key to get installed programs

        try:

            process = subprocess.Popen(['reg', 'query', key], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()

            if stdout:

                # Decode and split the result to process it line by line

                lines = stdout.decode().splitlines()

                for line in lines:

                    if "HKEY" in line:

                        program_key = line.strip()

                        try:

                            # Query for the 'DisplayName' value in each program's registry entry

                            process_program = subprocess.Popen(['reg', 'query', program_key, '/v', 'DisplayName'],
                                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                            stdout_program, stderr_program = process_program.communicate()

                            if stdout_program:
                                program_info = stdout_program.decode().strip().split()

                                # The 'DisplayName' value will be the last in the line

                                program_name = ' '.join(program_info[program_info.index('DisplayName') + 2:])

                                installed_programs.append(program_name)



                        except Exception as e:

                            # If there's an error in querying a specific program entry, continue

                            continue



        except Exception as e:

            # If querying the registry key fails, skip it

            continue

    return installed_programs


# Call the function and print installed programs

if __name__ == '__main__':

    programs = get_installed_programs()

    print("Installed Programs:")
    for program in programs:
        print(program)
    #input("Press Enter to Exit")
