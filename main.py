import json

class Transform:

    def __init__(self):
        self.status_file_path = 'status'
        self.json_output_path = 'packages.json'
        self.packages_list = []
        self.package_dict = {}

    def create_package_from_file(self):

        with open(self.status_file_path, 'r') as file:
            package_data = {}
            for line in file:
                line = line.strip()
                if line == "":
                    if package_data:
                        self.packages_list.append(package_data)
                        self.package_dict[package_data['Package']] = package_data
                        package_data = {}
                else:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        if key in ['Package', 'Description', 'Depends']:
                            if key == 'Depends':
                                package_data[key.strip()] = list(set(dep.split()[0] for dep in value.split(', ')))
                            else:
                                package_data[key.strip()] = value.strip()
                    else:
                        if 'Description' in package_data:
                            package_data['Description'] += '\n' + line
                        else:
                            print(f"Warning: unexpected format in line: {line}")
            if package_data:  # last line of the file
                self.packages_list.append(package_data)
                self.package_dict[package_data['Package']] = package_data

        return self.packages_list, self.package_dict

    def convert_to_json(self, data):
        with open(self.json_output_path, 'w') as file:
            json.dump(data, file, indent=2)


if __name__ == '__main__':

    transform = Transform()
    packages_list, package_dict = transform.create_package_from_file()
    transform.convert_to_json(package_dict)



