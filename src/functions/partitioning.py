import shutil
import subprocess
from pprint import pprint

from ..utils.device import Device


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
            partitions.append({
                "label": "efi",
                "mountpoint": "/boot/efi",
                "type": "fat32",
            })
            device.new_virtual_partition("efi", 512)

        for partition in partitions:
            _size = device.get_partition_size(partition.get("label"))
            print(f"Creating partition: {partition.get('label')} with size: {_size}")
    
    def __manual_partitioning(self) -> None:
        """Not implemented yet"""
        pass
    