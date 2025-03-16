from utils.file_handler import FileHandler
from utils.ip_to_location_parser import IPtoLocationParser
from utils.mongodb_handlers import MongoHandler


class IPProcessor:
    def __init__(self, logger, args, client):
        self.mongo_uri = args.mongo_uri
        self.database_name = args.database_name
        self.collection_name = args.collection_name
        self.unique_ips_file = args.unique_ips_file
        self.app_log = args.app_log
        self.processed_data_log = args.processed_data_log
        self.batch_size = args.batch_size
        self.last_batch_num = args.last_batch_num
        self.first_num = args.first_num
        self.last_num = args.last_num
        self.client = client
        self.file_handler = FileHandler(
            logger=logger,
            unique_ips_file=self.unique_ips_file,
            processed_data_log=self.processed_data_log,
        )
        self.mongo_handler = MongoHandler(
            logger=logger,
            client=self.client,
            database_name=self.database_name,
            collection_name=self.collection_name,
        )
        self.ip_to_location_parser = IPtoLocationParser(logger=logger)
        self.logger = logger

    def process_ips(self):
        try:
            last_batch_num, first_num, last_num = (
                self.last_batch_num,
                self.first_num,
                self.last_num,
            )
            uniq_ips = list(self.file_handler.read_unique_ips())
            if not uniq_ips:
                uniq_ips = self.mongo_handler.get_unique_ips()
                self.file_handler.write_unique_ips(uniq_ips)
            batch = []
            for i, ip in enumerate(uniq_ips, start=1):
                if i <= last_num:
                    continue
                location_info = self.ip_to_location_parser.get_location(ip)
                batch.append(location_info)

                if len(batch) == self.batch_size:
                    last_batch_num += 1
                    first_num = last_num + 1
                    last_num = last_num + self.batch_size
                    self.logger.info(
                        f"Processed batch {last_batch_num} - documents: {first_num} - {last_num} successfully."
                    )
                    self.mongo_handler.insert_locations(batch)
                    batch = []
            if batch:
                last_batch_num += 1
                first_num = last_num + 1
                last_num = last_num + len(batch)
                self.logger.info(
                    f"Processed batch {last_batch_num} - documents: {first_num} - {last_num} successfully."
                )
                self.mongo_handler.insert_locations(batch)
        except Exception as e:
            self.logger.error(e)
            raise
