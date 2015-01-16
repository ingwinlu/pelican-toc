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

    def test_toc_generation(self):
        article_with_headers_path = "test_data/article_with_headers.md"
        article_with_headers_toc_path = "test_data/article_with_headers_toc.html"
        article_with_headers = self._handle_article_generation(
           article_with_headers_path)
        toc.generate_toc(article_with_headers)
        with open(article_with_headers_toc_path, 'r') as f:
            test_toc = f.read()
            self.assertEqual(
                article_with_headers.toc,
                test_toc,
                "bad toc generated")

    def test_no_toc_generation(self):
        article_without_headers_path = "test_data/article_without_headers.md"
        article_without_headers = self._handle_article_generation(
            article_without_headers_path)
        toc.generate_toc(article_without_headers)
        with self.assertRaises(AttributeError):
            self.assertIsNone(article_without_headers.toc)

if __name__ == "__main__":
    unittest.main()