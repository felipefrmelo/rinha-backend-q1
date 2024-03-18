import re


class Router:

    def __init__(self, endpoint, method, handler):
        self.endpoint = mount(endpoint)
        self.method = method
        self.handler = handler

    def match(self, path, method):
        return method == self.method and self.endpoint(path)

    def get_params(self, path):
        return self.endpoint(path)


def mount(path):
    route_params = {}

    pattern = r'{([^{}]+):([^{}]+)}'

    matches = re.findall(pattern, path)

    for match in matches:
        param_name, param_type = match
        route_params[param_name] = param_type

    parsed_route = {
        'path': path,
        'params': route_params
    }

    def match_route(test_path):
        route_params = parsed_route['params']
        path_regex = parsed_route['path']
        for param_name, param_type in route_params.items():
            path_regex = path_regex.replace(
                f'{{{param_name}:{param_type}}}', f'(?P<{param_name}>\\d+)')

        pattern = re.compile('^' + path_regex + '$')

        match = pattern.match(test_path.split('?')[0])

        if match:
            return {name: int(value)
                    for name, value in match.groupdict().items()}

    return match_route
