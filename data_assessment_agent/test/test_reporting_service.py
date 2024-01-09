import unittest

from pathlib import Path

from data_assessment_agent.service.reporting_service import compress_zip_file


class TestPersistenceService(unittest.TestCase):
    def test_compress_zip_file(self):
        tmp_path = Path("/tmp")
        if not tmp_path.exists():
            tmp_path.mkdir()
        files = [tmp_path / "file_1.txt", tmp_path / "file_2.txt"]
        for f in files:
            f.write_text("This is a test")
        target_zip = tmp_path / "test.zip"
        compress_zip_file(target_zip, files)
        assert target_zip.exists()


if __name__ == "__main__":
    unittest.main()
