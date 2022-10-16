from vanilla_os_jade.utils.command import CommandUtils

class PartitionUtils:
    def mount(disk: str, mountpoint: str, options, filesystem = None):
        if filesystem is not None:
            options = options+" -t "+filesystem
        CommandUtils.check_output(["mkdir", "-p", mountpoint])
        CommandUtils.check_output(["mount", "-o", options, disk, mountpoint])

    def format(disk: str, filesystem: str):
        if filesystem == "btrfs":
            CommandUtils.check_output("mkfs.btrfs -f "+disk)
        elif filesystem == "ext4":
            CommandUtils.check_output("mkfs.ext4 "+disk)
        elif filesystem == "xfs":
            CommandUtils.check_output("mkfs.xfs -f "+disk)
        elif filesystem == "fat32" or filesystem == "vfat":
            CommandUtils.check_output("mkfs.fat -F32 "+disk)
        elif filesystem == "f2fs":
            CommandUtils.check_output("mkfs.f2fs "+disk)
