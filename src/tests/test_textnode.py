import unittest
from src.nodes.textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimeter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # HACER MAS TESTS!!
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

class TestTextToHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "fake.link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), "<a href=\"fake.link\">This is a link</a>")

class TestSplitNodes(unittest.TestCase):
    
    def test_only_text(self):
        node = TextNode("this is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "_", TextType.TEXT)
        self.assertEqual(new_nodes, [node])

    def test_bold(self):
        node = TextNode("this is text with **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("this is text with ", TextType.TEXT), TextNode("bold", TextType.BOLD)])
 
    def test_italic(self):
        node = TextNode("this is text with _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("this is text with ", TextType.TEXT), TextNode("italic", TextType.ITALIC)])   
    
    def test_italic_and_bold(self):
        node = TextNode("this is text with _italic_ and **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("this is text with ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" and **bold**", TextType.TEXT)])   

    def test_italic_and_bold_1(self):
        node = TextNode("this is text with _italic_ and **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "_", TextType.ITALIC)
        final_nodes = split_nodes_delimeter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(final_nodes, [TextNode("this is text with ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" and ", TextType.TEXT), TextNode("bold", TextType.BOLD)])   
     

class TestExtractionOfImgAndLinks(unittest.TestCase):
    
    def test_exctract_nothing(self):
        matches = extract_markdown_images("just text")
        self.assertListEqual([], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://invented link)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_image_01(self):
        matches = extract_markdown_images(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_link_01(self):
        matches = extract_markdown_links(
                 "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_link_02(self):
        matches = extract_markdown_links(
                 "This is text with a link [to boot dev](https://www.boot.dev) and ![an image](invented image)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)


class TestSplitImagesAndLinks(unittest.TestCase):
    
    def test_split_00(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_keep_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [this is a link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [this is a link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_two_nodes_image(self):
        nodes = [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                ),
                TextNode(
                    "and another text",
                    TextType.TEXT,
                )]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                    TextNode("and another text", TextType.TEXT)
                ], new_nodes)


class TestTextToTextNodes(unittest.TestCase):

    def test_01(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)

    def test_02(self):
        text = "This is **text** with an _italic_ word and a `code block`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            ]
        self.assertListEqual(result, expected)

    def test_only_text(self):
        node = TextNode("this is plain text", TextType.TEXT)
        new_nodes = text_to_textnodes("this is plain text") 
        self.assertEqual(new_nodes, [node])

    def test_bold(self):
        new_nodes = text_to_textnodes("this is text with **bold**")
        self.assertEqual(new_nodes, [TextNode("this is text with ", TextType.TEXT), TextNode("bold", TextType.BOLD)])
 
    def test_italic(self):
        new_nodes = text_to_textnodes("this is text with _italic_")
        self.assertEqual(new_nodes, [TextNode("this is text with ", TextType.TEXT), TextNode("italic", TextType.ITALIC)])   
    




if __name__ == "__main__":
    unittest.main()
