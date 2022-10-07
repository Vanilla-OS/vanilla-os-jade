from vanilla_os_jade.utils.command import  CommandUtils
import vanilla_os_jade.utils.partition.*

def install_base():
    '''Extracts the squashfs image on install root'''
    CommandUtils.check_output("unsquashfs -l")
    mount(
        disk="/cdrom/casper/filesystem.squashfs",
        mountpoint="/tmp/jade-squashfs/",
        options="loop",
        filesystem="squashfs"
    )
    CommandUtils.check_output("unsquashfs -l /cdrom/casper/filesystem.squashfs")
    CommandUtils.check_output("rsync -aHAXr --filter=-x trusted.overlay.* --exclude /proc/ --exclude /sys/ --exclude /dev/ --exclude /run/ --exclude /run/udev/ --exclude /run/systemd/resolve/ --progress /tmp/jade-sqaushfs/ /mnt")
