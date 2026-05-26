from wagtail import blocks
from wagtail.blocks import StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    description = blocks.CharBlock(label="Описание")
    video = VideoChooserBlock(label="Видео")
    preview_image = ImageChooserBlock(label="Превью")


class PhotoBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    description = blocks.CharBlock(label="Описание")
    image = ImageChooserBlock(label="Изображение")


class GardenInfoBlock(blocks.StructBlock):
    metric = blocks.IntegerBlock(label="Метрика")
    unit = blocks.CharBlock(label="Единица измерения")
    title = blocks.CharBlock(label="Заголовок")


class TabBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    description = blocks.RichTextBlock(label="Описание")
    image = ImageChooserBlock(label="Изображение")


class TwoColumnsBlock(blocks.StructBlock):
    first_block = blocks.RichTextBlock(label="Левая колонка")
    second_block = blocks.RichTextBlock(label="Правая колонка")


class ListForTabBlock(blocks.StructBlock):
    icon = ImageChooserBlock(label="Иконка")
    title = blocks.CharBlock(label="Заголовок")
    description = blocks.CharBlock(label="Описание")


class PhotoWithoutDescriptionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    image = ImageChooserBlock(label="Изображение")


class VideoWithPreviewBlock(blocks.StructBlock):
    preview_image = ImageChooserBlock(label="Превью")
    video = VideoChooserBlock(label="Видео")


class VideoWithoutDescriptionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    video = VideoChooserBlock(label="Видео")
    preview_image = ImageChooserBlock(label="Превью")


class TabListBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    content = StreamBlock(
        [
            ("Paragraph", ListForTabBlock()),
        ],
        label="Содержимое",
    )
    image = ImageChooserBlock(label="Изображение")
