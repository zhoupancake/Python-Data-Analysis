import os
import subprocess
from scrapy import cmdline

# execute the command
os.chdir('source1')
cmdline.execute("scrapy crawl honor".split(" "))

# execute the command
os.chdir('..')
subprocess.run(['python', 'source2/dataAccess.py'])
