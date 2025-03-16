from configs.configs import UNIQUE_IPS_FILE_LOCATION, PROCESSED_DATA_LOG


class FileHandler:
    def __init__(
        self,
        logger,
        unique_ips_file=UNIQUE_IPS_FILE_LOCATION,
        processed_data_log=PROCESSED_DATA_LOG,
    ):
        self.unique_ips_file = unique_ips_file
        self.processed_data_log = processed_data_log
        self.logger = logger

    def read_unique_ips(self):
        try:
            with open(self.unique_ips_file, "r") as f:
                for line in f:
                    yield line.strip()
            self.logger.info(
                f"Successfully read unique IPs from {self.unique_ips_file}"
            )
        except FileNotFoundError as e:
            self.logger.error(
                f"Failed to read unique IPs from {self.unique_ips_file}: {e}"
            )
            return []

    def write_unique_ips(self, ips):
        try:
            with open(self.unique_ips_file, "a+", buffering=1024 * 1024) as f:
                f.writelines(f"{ip}\n" for ip in ips)
            self.logger.info(
                f"Wrote {len(ips)} unique IPs into {self.unique_ips_file} successfully."
            )
        except Exception as e:
            self.logger.error(
                f"Failed to write unique IPs into {self.unique_ips_file}: {e}"
            )
            raise
