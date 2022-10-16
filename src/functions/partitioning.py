import shutil
import subprocess
from pprint import pprint

from ..utils.device import Device
from ..utils.command import CommandUtils
from ..utils.partition import PartitionUtils

class Partitioning():
    def __init__(self, config: dict):
        self.__device = config.get("device")
        self.__efi = config.get("efi")
        self.__mode = config.get("mode")
        self.__partitions = self.__parse_partitions(config.get("partitions", []))
        self.__do()

    def __parse_partitions(self, config: list) -> list:
        partitions = []

        for item in config:
            _partition, _mountpoint, _type = item.split(":")
            partitions.append({
                "partition": _partition,
                "mountpoint": _mountpoint,
                "type": _type
            })

        return partitions

    def __do(self):
        if self.__mode == "Auto":
            return self.__auto_partitioning()

        elif self.__mode == "Manual":
            return self.__manual_partitioning()

    def __format_sata(self):
        if self.__efi:
            PartitionUtils.format(disk=self.__disk+"1", filesystem="fat32")
        else:
            PartitionUtils.format(disk=self.__disk+"1", filesystem="ext4")

        PartitionUtils.format(disk=self.__disk+"2", filesystem="btrfs")
        PartitionUtils.mount(disk=self.__disk+"2", mountpoint="/mnt")
        CommandUtils.check_output(command=["btrfs", "subvol", "create", "/mnt/@"])
        CommandUtils.check_output(command=["btrfs", "subvol", "create", "/mnt/@home"])
        CommandUtils.check_output(command=["umount", "/mnt"])
        Partitioning.mount(disk=self.__disk+"2", mountpoint="/mnt", options="subvol=@,noatime,autodefrag,compression")
        Partitioning.mount(disk=self.__disk+"2", mountpoint="/mnt/home", options="subvol=@home,noatime,autodefrag,compression")

        if self.__efi:
            PartitionUtils.mount(disk=self.__disk+"1", mountpoint="/mnt/boot/efi", options="")
        else:
            PartitionUtils.mount(disk=self.__disk+"1", mountpoint="/mnt/boot", options="")


    def __format_nvme(self):
        if self.__efi:
            PartitionUtils.format(disk=self.__disk+"p1", filesystem="fat32")
        else:
            PartitionUtils.format(disk=self.__disk+"p1", filesystem="ext4")

        PartitionUtils.format(disk=self.__disk+"p2", filesystem="btrfs")
        PartitionUtils.mount(disk=self.__disk+"p2", mountpoint="/mnt")
        CommandUtils.check_output(command=["btrfs", "subvol", "create", "/mnt/@"])
        CommandUtils.check_output(command=["btrfs", "subvol", "create", "/mnt/@home"])
        CommandUtils.check_output(command=["umount", "/mnt"])
        Partitioning.mount(disk=self.__disk+"p2", mountpoint="/mnt", options="subvol=@,noatime,autodefrag,compression")
        Partitioning.mount(disk=self.__disk+"p2", mountpoint="/mnt/home", options="subvol=@home,noatime,autodefrag,compression")
        
        if self.__efi:
            PartitionUtils.mount(disk=self.__disk+"p1", mountpoint="/mnt/boot/efi", options="")
        else:
            PartitionUtils.mount(disk=self.__disk+"p1", mountpoint="/mnt/boot", options="")

    def __efi_create_partitions(self):
        device = Device(self.__device)
        print(f"Formatting device {self._device} for UEFI")
        CommandUtils.check_output(command=["parted", "-s", self.__device, "mklabel", "gpt"])
        print(f"Creating efi partition with size 512MB")
        CommandUtils.check_output(command=["parted", "-s", self.__device, "mkpart", "primary", "fat32", "1MIB", "512MIB"])
        print(f"Creating root partition with remaining disk space")
        CommandUtils.check_output(command=["parted", "-s", self.__device, "mkpart", "primary", "btrfs", "512MB", "100%"])
        if "nvme" in self.__device:
            self.__format_nvme()
        else:
            self.__format_sata()

    def __legacy_create_partitions(self):
        print(f"Formatting device {self.__device} for legacy bios")
        CommandUtils.check_output(command=["parted", "-s", self.__device, "mklabel", "msdos"])
        print(f"Creating boot partition with size 1gb")
        CommandUtils.check_output(command=["parted", "-s", self.__device, "mkpart", "primary", "ext4", "1MIB", "1024MIB"])
        print(f"Creating root partition with remaining disk space")
        CommandUtils.check_output(command=["parted", "-s", self.__device, "mkpart", "primary", "btrfs", "1024MIB", "100%"])
        if "nvme" in self.__device:
            self.__format_nvme()
        else:
            self.__format_sata()

    def __auto_partitioning(self) -> str:
        device = Device(self.__device)
        partitions = [
            {
                "label": "root",
                "mountpoint": "/mnt/",
                "type": "btrfs",
            },
            {
                "label": "boot",
                "mountpoint": "/mnt/boot",
                "type": "ext4",
            }
        ]
        device.new_virtual_partition("root", -1)
        device.new_virtual_partition("boot", 512)

        if self.__efi:
            partitions.apccpend({
                "label": "efi",
                "mountpoint": "/boot/efi",
                "type": "fat32",
            })
            device.new_virtual_partition("efi", 512)
            self.__efi_create_partitions()
        else:
            self.__legacy_create_partitions()
    
    def __manual_partitioning(self) -> None:
        """Only works because the lowest mountpoint can be /mnt and mountpoints never end with /"""
        def count_path_nesting(path):
            return path.mountpoint.count('/')
        self.__partitions.sort(key=count_path_nesting)
        for partition in self.__partitions:
            PartitionUtils.format(disk=partition.partition, filesystem=partition.type)
            PartitionUtils.mount(disk=partition.partition, mountpoint=partition.mountpoint, options="", filesystem=partition.type)