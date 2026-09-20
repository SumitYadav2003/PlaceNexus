from .software import software_roles
from .data import data_roles
from .cloud import cloud_roles
from .security import security_roles
from .testing import testing_roles
from .networking import networking_roles
from .fresher import fresher_roles
from .aliases import career_aliases

career_guides = {}

career_guides.update(software_roles)
career_guides.update(data_roles)
career_guides.update(cloud_roles)
career_guides.update(security_roles)
career_guides.update(testing_roles)
career_guides.update(networking_roles)
career_guides.update(fresher_roles)