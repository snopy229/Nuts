from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    video = VideoChooserBlock()


class PhotoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    image = ImageChooserBlock()
