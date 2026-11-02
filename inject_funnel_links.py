import os
import subprocess
import sys

script = os.path.join(os.path.dirname(__file__), "15-DEPLOY-AND-FUNNEL-BRIDGE", "inject_funnel_links.py")
subprocess.run([sys.executable, script], check=True)
