import {SkuImageInterface} from "@/interfaces/Product";
import Image from "next/image";
import {Box, useMediaQuery} from "@chakra-ui/react";

import {useKeenSlider} from "keen-slider/react";
import "keen-slider/keen-slider.min.css"
import {useEffect, useRef, useState} from "react";
import {ChevronLeft, ChevronRight} from "@/components/App/Product/Galery/components";

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
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const mountedRef = useRef(false)
    const [imagesLoaded, setImagesLoaded] = useState(0);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [sliderRef, instanceRef] = useKeenSlider({
        initial: 0,
        loop: true,
        slideChanged(s) {
            setCurrentSlide(s.track.details.rel);
        },
    });

    const [thumbnailRef, thumbnailInstanceRef] = useKeenSlider(
        {
            initial: 0,
            slides: {
                perView: 6,
                spacing: 10,
            },
        },
        [ThumbnailPlugin(instanceRef)]
    );

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

    useEffect(() => {
        if (images.length - 1 === imagesLoaded && !mountedRef.current) {
            mountedRef.current = true
            instanceRef.current?.update()
            thumbnailInstanceRef.current?.update()
        }

    }, [imagesLoaded, mountedRef, instanceRef, thumbnailInstanceRef]);


    return (
        <Box w={mobile ? '100%' : '65%'} overflow="hidden">
            <Box ref={sliderRef} className="keen-slider">
                <ChevronLeft mobile={mobile} onClick={handleSlideLeft}/>
                <ChevronRight mobile={mobile} onClick={handleSlideRight}/>
                {images.map((image, key) => (
                    <Box
                        className={`keen-slider__slide number-slide-` + key}
                        position="relative"
                        display="block"
                        key={key}
                        w="100%"
                        h="auto"
                        pt="66%"
                    >
                        <Image
                            style={{objectFit: 'cover'}}
                            unoptimized
                            fill
                            src={image.image}
                            alt={'img-' + key}
                        />
                    </Box>
                ))}
            </Box>
            <Box position="relative" mt="2" ref={thumbnailRef} className="keen-slider thumbnail">
                {images.map((image, key) => (
                    <Box key={key}>
                        <Box
                            className={`keen-slider__slide number-slide-` + key}
                            position="relative"
                            display="block"
                            w="100%"
                            h="auto"
                            pt="66%"
                            border="2px solid"
                            borderColor={currentSlide === key ? 'orange.500' : 'brown.500'}
                            _hover={{
                                borderColor: 'orange.400',
                                cursor: 'pointer',
                            }}
                        >
                            <Image
                                style={{objectFit: 'cover'}}
                                unoptimized
                                fill
                                src={image.image}
                                alt={'img-' + key}
                                onLoad={() => setImagesLoaded(key)}
                            />
                        </Box>
                    </Box>
                ))}
            </Box>
        </Box>
    );
};


