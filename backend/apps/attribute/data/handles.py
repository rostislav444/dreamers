from project.settings import STATICFILE_DIR
from django.conf.urls.static import static
import os


handles = [
    {'name': 'Крестообразная черная', 'price': 30, 'image': 'initialdata/hendles/FF-L-0580_16-Black.jpeg'},
    {'name': 'Крестообразная никелевая', 'price': 30, 'image': 'initialdata/hendles/FF-L-0580_16-Nickel.jpeg'},
    {'name': 'Крестообразная стальная', 'price': 30, 'image': 'initialdata/hendles/FF-L-0580_16-Steel.jpeg'},
    {'name': 'Накладная прямоугольная белая', 'price': 50,
     'image': 'initialdata/hendles/Marella-M-15224_100_32-White.jpeg'},
    {'name': 'Накладжная прямоугольная черная', 'price': 50,
     'image': 'initialdata/hendles/Marella-M-15224_100_32-Black.jpeg'},
    {'name': 'Накладная прямоуголная никеленвая', 'price': 50,
     'image': 'initialdata/hendles/Marella-M-15224_100_32-Nickel.jpeg'},
    {'name': 'Накладная прямугольная медная', 'price': 50,
     'image': 'initialdata/hendles/Marella-M-15224_100_32-Copper.jpeg'},
    {'name': 'Капля хромированная', 'price': 80,
     'image': 'initialdata/hendles/Marella-M-15244_160-Chromium.jpeg'},
    {'name': 'Капля черная матовая', 'price': 80,
     'image': 'initialdata/hendles/Marella-M-15244_160-Matt-black.jpeg'},
    {'name': 'Капля никелевая', 'price': 80, 'image': 'initialdata/hendles/Marella-M-15186_320-Nickel.jpeg'},
    {'name': 'Капля белый глянец', 'price': 80,
     'image': 'initialdata/hendles/Marella-M-15186_320-White-gloss.jpeg'},
    {'name': 'Трапеция хромированная', 'price': 40,
     'image': 'initialdata/hendles/Marella-M-15186_320-Chromium.jpeg'},
    {'name': 'Трапеция никелевая', 'price': 40, 'image': 'initialdata/hendles/Marella-M-15186_320-Nickel.jpeg'},
    {'name': 'Трапеция белый глянец', 'price': 40,
     'image': 'initialdata/hendles/Marella-M-15186_320-White-gloss.jpeg'},
    {'name': 'Трапеция никель темный', 'price': 40,
     'image': 'initialdata/hendles/Marella-M-15186_320-Nickel-dark.jpeg'},
    {'name': 'Лепесток хромированный', 'price': 90,
     'image': 'initialdata/hendles/Marella-M-15185_160-Chromium.jpeg'},
    {'name': 'Лепесток белый', 'price': 90, 'image': 'initialdata/hendles/Marella-M-15185_160-White-gloss.jpeg'},
    {'name': 'Скоба никелевая', 'price': 120, 'image': 'initialdata/hendles/FF-M-0030_160-Nickel.jpeg'},
    {'name': 'Скоба алюминиевая', 'price': 120, 'image': 'initialdata/hendles/FF-M-0030_160-Aluminum.jpeg'},
]