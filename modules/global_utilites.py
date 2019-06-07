import pickle
import os
import time


# Changes CWD to where this script is located.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
#time = time.strftime("%m-%d-%Y_%H-%M")

"""if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from . import backup
    else:
        from . import backup
else:
    from . import backup

back_up = backup.Backup()"""

# Global Utilities
class Global_Utilities:

    def initial_setup(self, banner):
        settings = {"uuid-path": "../vm_data/", "uuid-filename": "vm-uuids.txt", "backup-path": ""}
        # Establish where the vm-uuid file goes.
        while True:
            os.system("clear")
            print(banner)
            print("Where would you like to store the UUID file? (default: ../vm_data/)\nLeave empty for default.")
            uuid_path = raw_input(": ")
            if uuid_path == "":
                break
            else:
                test = os.path.exists("{}".format(uuid_path))
                if test == True:
                    settings["uuid-path"] = uuid_path
                    break
                else:
                    print("This directory doesn't exist!")
                    raw_input(" ")

        # Establishes backup path.
        while True:
            os.system("clear")
            print(banner)
            print("Where would you like the vm's to be backed up?\n"
                  "(A network file share or off site file share is recommended for this)")
            backup_path = raw_input(": ")
            if backup_path == "":
                break
            else:
                test = os.path.exists("{}".format(backup_path))
                if test == True:
                    settings["backup-path"] = backup_path
                    break
                else:
                    print("This directory doesn't exist!")
                    raw_input(" ")

        # Creates initial vm-uuid file.
        try:
            # Gets raw UUID and label info for all VMs.
            os.system("touch {}vm-uuids.txt".format(settings["uuid-path"]))
            os.system("xe vm-list is-control-domain=false is-a-snapshot=false | grep uuid | cut -d':' -f2 > {}{}"
                      .format(settings["uuid-path"], settings["uuid-filename"]))
            # Creates lists from data.
            uuids = open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "r")
            uuids = uuids.read().split("\n")
            os.system("xe vm-list is-control-domain=false is-a-snapshot=false | grep label | cut -d':' -f2 > {}{}"
                      .format(settings["uuid-path"], "tmp.txt"))
            labels = open("{}tmp.txt".format(settings["uuid-path"]), "r")
            labels = labels.read().split("\n")
            # Pairs UUIDs with appropriate labels
            pairs = []
            for i in range(len(labels)):
                labels[i] = labels[i].replace(" ", "")
                uuids[i] = uuids[i].replace(" ", "")
                pairs.append("{}:{}".format(labels[i], uuids[i]))

            # Removes an empty list entry that always seems to be there.
            if pairs[-1] == ":" or pairs[-1] == ": " or pairs[-1] == " :" or pairs[-1] == " : ":
                del pairs[-1]

            # Writes pairs list to file.
            with open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "w") as f:
                for i in pairs:
                    f.write("%s\n" % i)

            # Cleans up the operation
            os.system("rm -f {}tmp.txt".format(settings["uuid-path"]))

        except:
            os.system("clear")
            print(banner)
            print("Something went wrong - failed to create UUID list!\nAre you sure XCP-ng is installed?")

        # Saves settings
        with open("settings.pickle", "wb") as f:
            pickle.dump(settings, f)

        os.system("clear")
        print(banner)
        print("Initial setup complete!")

    def gather_uuids(self):
        settings = self.load_settings()
        # Gets raw UUID and label info for all VMs.
        os.system("touch {}vm-uuids.txt".format(settings["uuid-path"]))
        os.system("xe vm-list is-control-domain=false is-a-snapshot=false | grep uuid | cut -d':' -f2 > {}{}"
                  .format(settings["uuid-path"], settings["uuid-filename"]))
        # Creates lists from data.
        uuids = open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "r")
        uuids = uuids.read().split("\n")
        os.system("xe vm-list is-control-domain=false is-a-snapshot=false | grep label | cut -d':' -f2 > {}{}"
                  .format(settings["uuid-path"], "tmp.txt"))
        labels = open("{}tmp.txt".format(settings["uuid-path"]), "r")
        labels = labels.read().split("\n")
        # Pairs UUIDs with appropriate labels
        pairs = []
        for i in range(len(labels)):
            labels[i] = labels[i].replace(" ", "")
            uuids[i] = uuids[i].replace(" ", "")
            pairs.append("{}:{}".format(labels[i], uuids[i]))

        # Removes an empty list entry that always seems to be there.
        if pairs[-1] == ":" or pairs[-1] == ": " or pairs[-1] == " :" or pairs[-1] == " : ":
            del pairs[-1]

        # Writes pairs list to file.
        with open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "w") as f:
            for i in pairs:
                f.write("%s\n" % i)

        # Cleans up the operation
        os.system("rm -f {}tmp.txt".format(settings["uuid-path"]))

    def load_settings(self):
        try:
            settings = open("settings.pickle", "rb")
            settings = pickle.load(settings)
            return settings
        except:
            return "no"

    def load_menu(self, banner):
        settings = self.load_settings()
        while True:
            os.system("clear")
            print(banner)
            print("Current UUID file: {}{}".format(settings["uuid-path"], settings["uuid-filename"]))
            print("Current backup path: {}".format(settings["backup-path"]))
            print("\n* The following VMs have been found and are ready to be backed up!\n")
            settings = self.load_settings()
            with open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "r") as f:
                pairs = f.read().split("\n")

            for p in pairs:
                print(p)

            print("1. Backup All VM's (takes a hot minute)\n"
                  "2. Backup Specific VM\n"
                  "Q. Exit")
            q = raw_input(": ")

            if q == str(1):
                self.backup_all(time)

            elif q == str(2):
                self.backup_single(banner, time)

            elif str(q).upper() == str("Q"):
                quit()

    def check_bkup_dir(self, vm_name):
        settings = self.load_settings()

        test = os.path.exists("{}{}".format(settings["backup-path"], vm_name))
        if test == True:
            return True
        else:
            os.system("mkdir {}{}".format(settings["backup-path"], vm_name))
            return False

    def backup_all(self, time):
        settings = self.load_settings()

        with open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "r") as f:
            pairs = f.read().split("\n")

        for p in pairs:
            p = p.split(":")
            print("Backing up...")
            time = time.strftime("%m-%d-%Y_%H-%M")
            print("Creating a snapshot of {}...".format(p[0]))
            os.system(
                "xe vm-snapshot uuid={} new-name-label='SNAPSHOT-{}-{}' > /tmp/tmp-uuid.txt".format(p[1], p[0], time))
            print("Prepping the snapshots UUID...".format(p[0]))
            with open("/tmp/tmp-uuid.txt", "r") as f:
                snapuuid = f.read()

            snapuuid = snapuuid.replace("\n", "")
            print("Done...")
            print("Creating a VM from {}'s snapshot...".format(p[0]))
            os.system("xe template-param-set is-a-template=false ha-always-run=false uuid={}".format(snapuuid))
            print("Done...")
            print("Exporting the created VM to the specified backup-path (this takes a while)...")
            test = self.check_bkup_dir(p[0])
            if test == True:
                pass
            else:
                print("New directory for {} backups created...".format(p[0]))
            os.system('xe vm-export vm={} filename="{}{}/{}-{}.xva"'
                      .format(snapuuid, settings["backup-path"], p[0], p[0], time))
            print("Done...")
            print("Destroying exported VM (don't freak out, it's normal)...")
            os.system("xe vm-uninstall uuid={} force=true".format(snapuuid))
            print("Done...")
            print("{} has been backed up!".format(p[0]))
        print("All backups complete! Returning to main menu.")
        raw_input(" ")

    def backup_single(self, banner, time):
        settings = self.load_settings()
        with open("{}{}".format(settings["uuid-path"], settings["uuid-filename"]), "r") as f:
            pairs = f.read().split("\n")

        while True:
            os.system("clear")
            print(banner)
            print("Select which VM you wish to backup.\n")
            counter = 0
            for p in pairs:
                if p == ":" or p == ": " or p == " :" or p == " : " or p == "":
                    del p
                else:
                    print("{}. {}".format(counter, p))
                    counter += 1
            counter += 1
            print("{}. Main Menu".format(counter))
            target = raw_input(": ")
            if int(target) == counter:
                break

            elif str(target).isdigit():
                target = int(target)
                os.system("clear")
                print(banner)
                print("Are you sure you want to backup this VM?\n")
                print(pairs[target])
                a = raw_input("Y/N: ")
                if str(a).upper() == "N":
                    break
                elif str(a).upper() == "Y":
                    p = pairs[target].split(":")
                    print("Backing up...")
                    time = time.strftime("%m-%d-%Y_%H-%M")
                    print("Creating a snapshot of {}...".format(p[0]))
                    test = self.check_bkup_dir(p[0])
                    if test == True:
                        pass
                    else:
                        print("New directory for {} backups created...".format(p[0]))
                    os.system(
                        "xe vm-snapshot uuid={} new-name-label='SNAPSHOT-{}-{}' > /tmp/tmp-uuid.txt".format(p[1], p[0],
                                                                                                            time))

                    print("Done...")
                    print("Prepping the snapshots UUID...".format(p[0]))
                    with open("/tmp/tmp-uuid.txt", "r") as f:
                        snapuuid = f.read()

                    snapuuid = snapuuid.replace("\n", "")
                    print("Done...")
                    print("Creating a VM from {}'s snapshot...".format(p[0]))
                    os.system("xe template-param-set is-a-template=false ha-always-run=false uuid={}".format(snapuuid))
                    print("Done...")
                    print("Exporting the created VM to the specified backup-path (this takes a while)...")
                    os.system(
                        'xe vm-export vm={} filename="{}{}/{}-{}.xva"'.format(snapuuid, settings["backup-path"], p[0], p[0],
                                                                           time))
                    print("Done...")
                    print("Destroying exported VM (don't freak out, it's normal)...")
                    os.system("xe vm-uninstall uuid={} force=true".format(snapuuid))
                    print("Done...")
                    print("{} has been backed up!".format(p[0]))
                    raw_input(" ")
                    break

            else:
                print("Please enter the number next to the desired VM.")
                raw_input(" ")
