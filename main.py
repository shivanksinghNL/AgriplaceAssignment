import json
import re
class PackageManager:

    def __init__(self):
        self.status_file_path = 'status'
        self.json_output_path = 'packages.json'
        self.packages_list, self.package_dict = self.create_package_from_file()

    def create_package_from_file(self):
        packages_list = []
        package_dict = {}
        with open(self.status_file_path, 'r') as file:
            package_data = {}
            for line in file:
                line = line.strip()
                if line == "":
                    if package_data:
                        packages_list.append(package_data)
                        package_dict[package_data['Package']] = package_data
                        package_data = {}
                else:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        if key in ['Package', 'Description', 'Depends']:
                            if key == 'Depends':
                                package_data[key.strip()] = [ dep.split()[0] for dep in re.split(r'[,\|]',value)]
                            else:
                                package_data[key.strip()] = value.strip()
                    else:
                        if 'Description' in package_data:
                            package_data['Description'] += '\n' + line
                        else:
                            pass
            if package_data:  # last line of the file
                packages_list.append(package_data)
                package_dict[package_data['Package']] = package_data

        return packages_list, package_dict

    def convert_to_json(self, data):
        with open(self.json_output_path, 'w') as file:
            json.dump(data, file, indent=2)


if __name__ == '__main__':
    package_manager = PackageManager()
    print(package_manager.packages_list[0])
    package_manager.convert_to_json(package_manager.package_dict)



