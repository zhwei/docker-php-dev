import os
import json

nginx_config_dir = '/etc/nginx/conf.d'
current_dir = os.path.dirname(os.path.realpath(__file__))

def parse_sites() -> list:
    with open(os.path.join(current_dir, 'sites.json'), 'r') as f:
        sites = json.load(f)

    for site in sites:
        if 'secure' not in site:
            site['secure'] = True

    print(f"Found sites: {len(sites)}")
    return sites


def generate_nginx(sites: list, generated_prefix='generated.'):
    # cleanup generated files
    for file in os.listdir(nginx_config_dir):
        if file.endswith('.conf') and file.startswith(generated_prefix):
            os.remove(os.path.join(nginx_config_dir, file))
            print(f'Removed {file} from {nginx_config_dir}')

    # read secure template from current directory stubs/site.secure.valet.conf
    with open(os.path.join(current_dir, 'stubs/site.secure.valet.conf'), 'r') as f:
        secure_template = f.read()
    # read insecure template from current directory stubs/site.insecure.valet.conf
    with open(os.path.join(current_dir, 'stubs/site.valet.conf'), 'r') as f:
        insecure_template = f.read()

    for configs in sites:
        server_name = configs["domain"]
        root = configs['root']
        fpm = configs['fpm']
        if not os.path.exists(root):
            print(f'WARNING: {root} does not exist')
        
        _vars = {
            'VALET_SITE': ' '.join([server_name] + configs.get('aliases', [])),
            'VALET_ROOT_PATH': root,
            'VALET_FPM_HOST': fpm,
            'VALET_HOME_PATH': '/tmp/',
            'VALET_CERT': '/php-shared/certs/multiple-domain.crt',
            'VALET_KEY': '/php-shared/certs/multiple-domain.key',
        }
        file_content = secure_template if configs.get('secure', True) else insecure_template
        for _key, _value in _vars.items():
            file_content = file_content.replace(_key, _value)
        
        config_file_name = generated_prefix + server_name + '.conf'
        with open(os.path.join(nginx_config_dir, config_file_name), 'w') as f:
            f.write(file_content)
        print(f'Generated {config_file_name}, server_name={server_name}, root={root}')
    pass
    
    # generate site index
    with open(os.path.join(current_dir, 'stubs/index.html'), 'r') as f:
        index_template = f.read()
    with open(os.path.join(current_dir, '/usr/share/nginx/html/index.html'), 'w') as f:
        f.write(index_template.replace('sites = []', 'sites = ' + json.dumps(sites)))
    pass


def generate_certs(sites: list):
    if os.path.exists('/.dockerenv'):
        raise RuntimeError('Cert generation should be done on host machine')

    cmd = 'mkcert -install'
    print(f'> {cmd}')
    os.system(cmd)

    domains = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
    ]
    for configs in sites:
        domains.append(configs['domain'])
        if configs.get('aliases', None):
            domains.extend(configs['aliases'])
    if not domains:
        raise RuntimeError('No valid site found')

    crt_path = os.path.join(current_dir, 'certs/multiple-domain.crt')
    key_path = os.path.join(current_dir, 'certs/multiple-domain.key')
    cmd = f'mkcert -cert-file {crt_path} -key-file {key_path} ' + ' '.join(set(domains))
    print(f'> {cmd}')
    os.system(cmd)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        sites = parse_sites()

        if sys.argv[1] == '--nginx':
            generate_nginx(sites)
            sys.exit(0)

        elif sys.argv[1] == '--certs':
            generate_certs(sites)
            sys.exit(0)

    print('Invalid option')
    print('Usage: python3 generator.py --nginx')
    print('Usage: python3 generator.py --certs')
