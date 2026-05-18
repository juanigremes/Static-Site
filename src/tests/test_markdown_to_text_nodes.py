import unittest
from src.markdown_to_text_nodes import *

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
    

class TestMarkdownToBlocks(unittest.TestCase):
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_01(self):
        md = """
This is __italic__ paragraph




This is another paragraph with **bold** text and `code` here
This is the same paragraph on a new line

- This is a list



- this is another list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is __italic__ paragraph",
                "This is another paragraph with **bold** text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list",
                "- this is another list",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        block = "this is just paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    

    
    def test_heading_1(self):
        block = "# this is heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_2(self):
        block = "## this is heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_3(self):
        block = "### this is heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_4(self):
        block = "#### this is heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_5(self):
        block = "##### this is heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_6(self):
        block = "###### this is heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_paragraph_not_heading_1(self):
        block = "####### this is just paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_not_heading_2(self):
        block = "###this is just paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    

    
    def test_code(self):
        block = """```
this is multiline code
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
 
    def test_code_1(self):
        block = """```
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
 
    def test_paragraph_not_code_1(self):
        block = "```this is just paragraph```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
 
    def test_paragraph_not_code_2(self):
        block = """```
this is just paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
 
    def test_paragraph_not_code_3(self):
        block = """``
this is just paragraph```"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    

    
    def test_quote1(self):
        block = ">this is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
 
    def test_quote2(self):
        block = "> this is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_3(self):
        block = ">"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
 


    
    def test_unordered_list_1(self):
        block = """- this
- is
- unordered
- list"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
 
    def test_paragraph_not_unordered_list_1(self):
        block = "-there is no spacte after the \"-\""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
 



    def test_ordered_list_1(self):
        block = """1. this
2. is
3. ordered
4. list"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
 
    def test_paragraph_not_ordered_list_1(self):
        block = """2. this is just paragraph
3. because it does not have a 1"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
 
    def test_paragraph_not_ordered_list_2(self):
        block = "1.this is just paragraph beacause there is no space after the number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


