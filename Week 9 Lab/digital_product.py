from product import Product


class DigitalProduct(Product):
    """
    A product that is delivered digitally through a download.
    Does not implement CanBeShipped since it is never physically shipped.
    """

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        """
        Display the common product details, then the digital-specific details.
        """
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return f"'{self.get_name()}' is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
