import shutil
import subprocess
import math


class Device:

    def __init__(self, device: str):
        self.__device = device
        self.__virtual_partitions = {}
        self.__device_size = self.__get_device_size()

    def __get_device_size(self) -> int:
        _device = subprocess.check_output(("lsblk", "--nodeps", "--output",
                                           "size", "--bytes", self.__device, "-n"), text=True)
        return int(_device.encode("utf-8"))

    def new_virtual_partition(self, n, size: int):
        size = int(size * 1024 * 1024)
        if size > self.__device_size:
            raise ValueError(f"The partition: `{n}` has a size of `{size}` that exceeds the devices size of `{self.__device_size}`")

        self.__virtual_partitions[n] = size
        self.__device_size -= size

    def get_partition_size(self, n: str) -> str:
        size = self.__virtual_partitions[n]
        if size == -1:
            size = self.__device_size

        size = math.ceil(size / 1024 / 1024)
        return f"{size}M"

