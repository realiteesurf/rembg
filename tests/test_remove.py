from io import BytesIO
from pathlib import Path

from imagehash import phash as hash_img
from PIL import Image

from rembg import new_session, remove

here = Path(__file__).parent.resolve()

def test_remove():
    kwargs = {
        "sam": {
            "car-1" : {
                "input_points": [[250, 200]],
                "input_labels": [1],
            },

            "cloth-1" : {
                "input_points": [[370, 495]],
                "input_labels": [1],
            }
        }
    }

    for model in [
        "u2net",
        "u2netp",
        "u2net_human_seg",
        "u2net_cloth_seg",
        "silueta",
        "isnet-general-use",
        "sam"
    ]:
        for picture in ["car-1", "cloth-1"]:
            image_path = Path(here / "fixtures" / f"{picture}.jpg")
            image = image_path.read_bytes()

            actual = remove(image, session=new_session(model), **kwargs.get(model, {}).get(picture, {}))
            actual_hash = hash_img(Image.open(BytesIO(actual)))

            expected_path = Path(here / "results" / f"{picture}.{model}.png")
            # Uncomment to update the expected results
            # f = open(expected_path, "ab")
            # f.write(actual)
            # f.close()

            expected = expected_path.read_bytes()
            expected_hash = hash_img(Image.open(BytesIO(expected)))

            print(f"image_path: {image_path}")
            print(f"expected_path: {expected_path}")
            print(f"actual_hash: {actual_hash}")
            print(f"expected_hash: {expected_hash}")
            print(f"actual_hash == expected_hash: {actual_hash == expected_hash}")
            print("---\n")

            assert actual_hash == expected_hash
