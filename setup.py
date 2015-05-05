import subprocess

print "Installing soundcloud api..."
subprocess.call("pip install soundcloud")

print "Installing google music api.."
subprocess.call("pip install gmusicapi")

print "Installing openSSL..."
subprocess.call("pip install pyopenssl ndg-httpsclient pyasn1")

print "Installing urllib3..."
subprocess.call("pip install urllib3")

print "Installing eyeD3..."
subprocess.call("pip install eyeD3-pip")

print "Installing PIL..."
subprocess.call("pip install pillow")

