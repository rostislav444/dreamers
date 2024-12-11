import {Box, IconButton} from "@chakra-ui/react";
import {DownloadIcon} from "@chakra-ui/icons";
import {GalleryArrowWrapper, MainImageWrapper} from "@/components/App/Product/Galery/style";
import {LazyImage} from "@/components/App/Product/Galery/components/LazyImage";
import {handleImageMergeAndDownload} from "@/components/App/Product/Galery/utils";
import Image from "next/image";
import {useEffect, useState} from 'react';

interface MainGalleryProps {
    images: string[];
    imagesAlt: string[];
    currentImage: number;
    handleArrowClick: (direction: number) => void;
    setIsModalOpen: (isOpen: boolean) => void;
}

const MainGallery = ({
                         images,
                         imagesAlt,
                         currentImage,
                         handleArrowClick,
                         setIsModalOpen
                     }: MainGalleryProps) => {
    const [isClient, setIsClient] = useState(false);

    useEffect(() => {
        setIsClient(true);
    }, []);

    return (
        <MainImageWrapper>
            <Box onClick={() => setIsModalOpen(true)}>
                {images.map((image: string, imageKey: number) =>
                    isClient ? (
                        <LazyImage
                            key={`lazy-${currentImage}-${imageKey}`}
                            lowResSrc={imagesAlt[imageKey]}
                            highResSrc={image}
                            alt='img'
                        />
                    ) : (
                    <img
                        key={`${currentImage}-${imageKey}`}
                        src={image}
                        alt='img'
                        style={{
                            position: 'absolute',
                            width: '100%',
                            height: '100%',
                            objectFit: 'contain',
                            top: 0,
                        }}
                    />
                ))}
            </Box>
            <GalleryArrowWrapper
                left={true}
                onClick={() => handleArrowClick(currentImage - 1)}
            >
                <Image width='16' height='16' src='/icons/arrow.svg' alt='<'/>
            </GalleryArrowWrapper>
            <GalleryArrowWrapper
                left={false}
                onClick={() => handleArrowClick(currentImage + 1)}
            >
                <Image
                    style={{transform: 'rotate(180deg)'}}
                    width='16'
                    height='16'
                    src='/icons/arrow.svg'
                    alt='<'
                />
            </GalleryArrowWrapper>
            <IconButton
                aria-label='download'
                icon={<DownloadIcon color='brown.500'/>}
                position='absolute'
                top='4'
                right='4'
                onClick={() => handleImageMergeAndDownload(images)}
                variant='ghost'
            />
        </MainImageWrapper>
    );
};

export default MainGallery;