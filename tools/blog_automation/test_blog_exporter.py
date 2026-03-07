import pytest
from blog_exporter import drive_connection, download_image_and_copy_to_repo
import os
from pathlib import Path

@pytest.mark.parametrize(
    "example_image", 
    [
        "https://drive.google.com/open?id=1o4byZahHg6KpqvKlJU_IJ0RKZ-nmcMnw",
        "https://drive.google.com/file/d/1o4byZahHg6KpqvKlJU_IJ0RKZ-nmcMnw/view",
        "https://drive.google.com/open?id=1DF08PAjvFPBv8ZGigjwiaFn1JP8TUHg7"
    ]
)
def test_download_image_and_copy_to_repo(example_image):
    blog_filename = "test_blog_image"
    blog_assets_dir = Path(__file__).resolve().parent.parent.parent / 'assets' / 'images' / 'blog'
    # if ../assets/images/blog/{blog_filename}.png exists, then remove it
    if os.path.exists(blog_assets_dir / f'{blog_filename}.png'):
        os.remove(blog_assets_dir / f'{blog_filename}.png')

    drive = drive_connection()

    image_path_relative = download_image_and_copy_to_repo(
        image_link=example_image, blog_filename=blog_filename, drive=drive)
    
    assert image_path_relative == f"/assets/images/blog/{blog_filename}.png"
    
    # assert that blog_filename exists
    os.remove(blog_assets_dir / f'{blog_filename}.png')