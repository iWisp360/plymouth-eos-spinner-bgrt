import os
import csv
import pathlib

if os.getuid() != 0:
    print("You have to run the script as superuser...")
    exit(1)

theme_dir = "contents/spinner-endeavouros"
os_release_path = pathlib.Path("/etc/os-release")
with open(os_release_path) as stream:
    reader = csv.reader(stream, delimiter="=")
    os_release = dict(reader)
    os_name = os_release["NAME"]

if os_name != "EndeavourOS" or os_name != "Archlinux":
    print("OS is not EndeavourOS or Archlinux, script may not work as intended...\n")

dracut_dir = "/bin/dracut"
mkinitcpio_dir = "/bin/mkinitcpio"
endeavouros_regen_init_command = "/bin/dracut-rebuild"

print("\nIMPORTANT NOTE:\nThe script will install plymouth if it's not yet, but you have to configure "
      "it to run at early boot, follow the \nguide at "
      "https://forum.endeavouros.com/t/guide-how-to-install-and-use-plymouth/51363\n")

print("You are about to make changes into your system, proceed? (y/n) ")
option = input()
if option.lower() != "y":
    exit(0)

os.system("pacman -S --noconfirm --needed plymouth")

print("\nCopying the theme to /usr/share/plymouth/themes/...\n")

os.system(f"cp -r {theme_dir} /usr/share/plymouth/themes/")

print("\nChanging theme...\n")

os.system("plymouth-set-default-theme spinner-endeavouros")

print("\nNow the theme is installed and set as default.\nIf you configured plymouth already in initramfs you can\n"
      "rebuild the initramfs in this script, proceed?(y/n) ")
option = input()

if option.lower() == "y":
    if os_name == "EndeavourOS":
        os.system(f"{endeavouros_regen_init_command}")

    else:
        if os.path.exists(f"{dracut_dir}"):
            print("Rebuilding initramfs using dracut...")
            os.system(f"{dracut_dir} -f")
            exit(0)

        elif os.path.exists(f"{mkinitcpio_dir}"):
            print("Rebuilding initramfs using mkinitcpio...")
            os.system(f"{mkinitcpio_dir} -P")
            exit(0)

        else:
            print("initramfs builder is not dracut or mkinitcpio, use your own...")
            exit(0)
