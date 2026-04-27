from pathlib import Path

import qrcode


def generate_worker_qr(worker_code: str, output_path: Path) -> str:
    """Generate a QR code that contains only worker_code."""
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(worker_code)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return str(output_path)
