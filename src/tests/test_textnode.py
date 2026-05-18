import unittest
from src.textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq_code(self):
        node = TextNode("This is a text code", TextType.CODE)
        node2 = TextNode("This is a text code", TextType.CODE)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a link", TextType.LINK, "invented.link")
        node2 = TextNode("This is a link", TextType.LINK, "invented.link")
        self.assertEqual(node, node2)

    def test_eq_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "invented.link")
        node2 = TextNode("This is a text node", TextType.IMAGE, "invented.link")
        self.assertEqual(node, node2)

    def test_bold_not_eq_to_italic(self):
        node = TextNode("text node", TextType.ITALIC)
        node2 = TextNode("text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_bold_not_eq_to_code(self):
        node = TextNode("text node", TextType.CODE)
        node2 = TextNode("text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_italic_not_eq_to_code(self):
        node = TextNode("text node", TextType.CODE)
        node2 = TextNode("text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_link_not_eq_to_image(self):
        node = TextNode("description", TextType.LINK, "invented.link")
        node2 = TextNode("description", TextType.IMAGE, "invented.link")
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
