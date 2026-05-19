from wagtail import blocks
from wagtailmedia.blocks import VideoChooserBlock


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    video = VideoChooserBlock()
