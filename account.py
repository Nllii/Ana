from playbooks.backend import connection
from playbooks.backend import extras


inventory_path = f'{extras.main_directory}/inventory.ini'
conn = connection.cluster(inventory=f'{inventory_path}')


conn.ansible(script='git_push')







