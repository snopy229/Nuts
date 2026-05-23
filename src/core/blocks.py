from wagtail import blocks
from wagtail.blocks import StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


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


class TabBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.RichTextBlock()
    image = ImageChooserBlock()


class TwoColumnsBlock(blocks.StructBlock):
    first_block = blocks.RichTextBlock()
    second_block = blocks.RichTextBlock()


class ListForTabBlock(blocks.StructBlock):
    icon = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()


class PhotoWithoutDescriptionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()


class VideoWithPreviewBlock(blocks.StructBlock):
    preview_image = ImageChooserBlock()
    video = VideoChooserBlock()


class TabListBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = StreamBlock(
        [
            ("Paragraph", ListForTabBlock()),
        ]
    )
    image = ImageChooserBlock()
