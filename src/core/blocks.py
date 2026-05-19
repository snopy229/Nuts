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
    preview_image = ImageChooserBlock()


class PhotoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    image = ImageChooserBlock()


class GardenInfoBlock(blocks.StructBlock):
    metric = blocks.IntegerBlock()
    unit = blocks.CharBlock()
    title = blocks.CharBlock()
