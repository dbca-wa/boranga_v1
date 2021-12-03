import os
import sys
import django
proj_path='/var/www/boranga'
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boranga.settings")
django.setup()


from boranga.components.proposals.models import Proposal

p=Proposal.objects.last()

print(p.__dict__)

