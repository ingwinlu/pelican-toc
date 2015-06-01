from io import open
import unittest
import toc

from pelican.readers import MarkdownReader
from pelican.contents import Article
from pelican.tests.support import get_settings


class TestToCGeneration(unittest.TestCase):
    settings = get_settings()
    md_reader = MarkdownReader(settings)

    def _handle_article_generation(self, path):
        content, metadata = self.md_reader.read(path)
        return Article(content=content, metadata=metadata)

    def _generate_toc(self, article_path, expected_path):
        result = self._handle_article_generation(article_path)
        toc.generate_toc(result)
        expected = ""
        with open(expected_path, 'r') as f:
            expected = f.read()
        return result, expected


    def test_toc_generation(self):
        result, expected = self._generate_toc(
                "test_data/article_with_headers.md",
                "test_data/article_with_headers_toc.html"
            )
        self.assertEqual(result.toc, expected)

    def test_toc_generation_nonascii(self):
        result, expected = self._generate_toc(
                "test_data/article_with_headers_nonascii.md",
                "test_data/article_with_headers_toc_nonascii.html"
            )
        self.assertEqual(result.toc, expected)

    def test_no_toc_generation(self):
        article_without_headers_path = "test_data/article_without_headers.md"
        article_without_headers = self._handle_article_generation(
            article_without_headers_path)
        toc.generate_toc(article_without_headers)
        with self.assertRaises(AttributeError):
            self.assertIsNone(article_without_headers.toc)

if __name__ == "__main__":
    unittest.main()

