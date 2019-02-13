#! /bin/bash

# Uninstalls everything that was installed with pyobjc
pip freeze | grep pyobjc | xargs pip uninstall -y