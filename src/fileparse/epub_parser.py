from typing import Optional, List
from collections import OrderedDict
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


class EpubParser:
    def __init__(self, epub_file: str):
        self.update_book(epub_file)

    def _read_epub(self):
        return epub.read_epub(self.epub_file)

    def update_book(self, epub_file: str):
        """Updates the book

        Args:
            epub_file (str): path to the epub file
        """
        self.epub_file = epub_file
        self.book = self._read_epub()
        self.contents = self._parse_contents()

    def _parse_contents(self, verbose=False) -> dict[str, str]:
        """Parses and saves the book contents as a dictionary"""
        contents = OrderedDict()
        for item in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text().strip()
            text = text.replace('\r\n', '')
            if text:
                chapter_title = text.split('\n')[0]
                contents[chapter_title] = text 
        if verbose:
            print('The parsed table of contents as follows')
            print(f'\n'.join(contents.keys()))
        return contents 

    def get_title(self):
        """Returns the book title"""
        return self.book.title

    def get_chapter_names(self) -> List[str]:
        """Gets a list of chapter names

        Returns:
            List[str]: list of chapter names
        """
        return list(self.contents.keys())

    def get_chapter(self, chapter_name: str):
        """Gets contents of the specified chapter

        Args:
            chapter_name (str): name of the chapter
        """
        return self.contents[chapter_name]
            
