from logic.textnode import TextNode, TextType
from logic.markdown_to_html import text_node_to_html_node  # o de donde sea que la importes

node = TextNode("didn't ruin it", TextType.ITALIC)
html = text_node_to_html_node(node)
print(html.to_html())
