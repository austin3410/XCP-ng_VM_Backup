import os

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from . import global_utilites
    else:
        from . import global_utilites
else:
    from . import global_utilites

# Global variables
global_utilites = global_utilites.Global_Utilities()

# Global Utilities
class Backup:

    def backup_all(self):
        settings = global_utilites.load_settings()

        with open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "r") as f:
            pairs = f.read().split("\n")

        for p in pairs:
            print(p)
        #snapuuid = os.system("xe vm-snapshot uuid=$VMUUID new-name-label='SNAPSHOT-$VMUUID-$DATE'")