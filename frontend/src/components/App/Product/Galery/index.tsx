import {SkuImageInterface} from "@/interfaces/Product";
import Image from "next/image";
import {Box} from "@chakra-ui/react";
import {ChevronLeftIcon, ChevronRightIcon} from '@chakra-ui/icons'
import {useKeenSlider} from "keen-slider/react";
import "keen-slider/keen-slider.min.css"
import {useState} from "react";

interface ProductGalleryInterface {
    images: SkuImageInterface[]
}

function ThumbnailPlugin(mainRef: any) {
    return (slider: any) => {
        function addClickEvents() {
            slider.slides.forEach((slide: any, idx: number) => {
                slide.addEventListener("click", () => {
                    if (mainRef.current) mainRef.current.moveToIdx(idx)
                })
            })
        }

        slider.on("created", () => {
            if (!mainRef.current) return
            addClickEvents()
            mainRef.current.on("animationStarted", (main: any) => {
                const next = main.animator.targetIdx || 0
                slider.moveToIdx(Math.min(slider.track.details.maxIdx, next))
            })
        })
    }
}


export const ProductGallery = ({images}: ProductGalleryInterface) => {
    const [currentSlide, setCurrentSlide] = useState(0)
    const [sliderRef, instanceRef] = useKeenSlider({
        initial: 0,
        loop: true,
        slideChanged(s) {
            setCurrentSlide(s.track.details.rel)
        },
    })
    const [thumbnailRef] = useKeenSlider(
        {
            initial: 0,
            slides: {
                perView: 6,
                spacing: 10,
            },
        },
        [ThumbnailPlugin(instanceRef)]
    )

    const handleSlideLeft = () => {
        if (instanceRef.current) {
            instanceRef.current.prev();
        }
    };

    const handleSlideRight = () => {
        if (instanceRef.current) {
            instanceRef.current.next();
        }
    };

    return <Box w='100%' overflow={'hidden'}>
        <Box ref={sliderRef} className="keen-slider">
            <ChevronLeftIcon
                onClick={handleSlideLeft}
                position='absolute'
                w={12}
                h={12}
                left={0}
                top='calc(50% - 24px)'
                cursor='pointer'
                zIndex={1000}
            />
            <ChevronRightIcon
                onClick={handleSlideRight}
                position='absolute'
                w={12}
                h={12}
                right={0}
                top='calc(50% - 24px)'
                cursor='pointer'
                zIndex={1000}
            />
            {images.map((image, key) =>
                <Box
                    className={`keen-slider__slide number-slide-` + key}
                    position='relative'
                    display='block'
                    key={key}
                    w='100%'
                    h='auto'
                    pt='66%'
                >
                    <Image style={{objectFit: 'cover'}} unoptimized fill src={image.image} alt={'img-' + key}/>
                </Box>
            )}
        </Box>
        <Box position='relative' mt='2' ref={thumbnailRef} className="keen-slider thumbnail">
            {images.map((image, key) =>
                <Box key={key}>
                    <Box
                        className={`keen-slider__slide number-slide-` + key}
                        position='relative'
                        display='block'
                        w='100%'
                        h='auto'
                        pt='66%'
                        border='2px solid'
                        borderColor={currentSlide === key ? 'orange.500' : 'brown.500'}
                        _hover={{
                            borderColor: 'orange.400',
                            cursor: 'pointer'
                        }}
                    >
                        <Image style={{objectFit: 'cover'}} unoptimized fill src={image.image} alt={'img-' + key}/>
                    </Box>
                </Box>
            )}
        </Box>
    </Box>
}