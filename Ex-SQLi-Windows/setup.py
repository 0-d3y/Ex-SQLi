import os
os.system("pip install pyarmor")
os.system("pip install aiohttp pyfiglet")
os.system("python -m pip install --upgrade pip")
os.system("curl -L -o sqlmap.zip https://github.com/sqlmapproject/sqlmap/zipball/master")
os.system("Expand-Archive -Path .\sqlmap.zip -DestinationPath .\sqlmap")
