import qrcode
from io import BytesIO
import base64

class GenerateQR:
    """
    Class to generate QR code images.

    Attributes:
        None
    """

    def generate_qr_code(self, data, *args, **kwargs):
        """
        Generate a QR code image in base64 format from the provided data.

        Args:
            data (str): The data to be encoded into the QR code.

        Returns:
            str: The base64 encoded image data of the generated QR code.
        """

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        base64_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return base64_image
