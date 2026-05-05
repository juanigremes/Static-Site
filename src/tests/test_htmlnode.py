import unittest

from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_h1_vacio_repr(self):
        node = HTMLNode("h1")
        rep = "tag = h1, value = None, children = None, props = "
        self.assertEqual(node.__repr__(), rep)

    def test_parrafo_repr(self):
        node = HTMLNode("p", "this is a paragraph")
        rep = "tag = p, value = this is a paragraph, children = None, props = "
        self.assertEqual(node.__repr__(), rep)

    def test_link_repr(self):
        node = HTMLNode("a", "this is a link", None, {"href": "algun.link"})
        rep = "tag = a, value = this is a link, children = None, props =  href=\"algun.link\""
        self.assertEqual(node.__repr__(), rep)

    if __name__ == "__main__":
        unittest.main()



class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_bold(self):
       self.assertRaises(ValueError, LeafNode, None, None)


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_link_with_children(self):
        child = LeafNode("h1", "Click me!")
        parent = ParentNode("a", [child], {"href": "https://www.google.com"})
        self.assertEqual(parent.to_html(), "<a href=\"https://www.google.com\"><h1>Click me!</h1></a>")
