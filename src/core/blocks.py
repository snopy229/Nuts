from wagtail import blocks


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()
